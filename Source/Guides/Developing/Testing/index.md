---
layout : Default
---

# Testing

This section describes automated testing strategies for your Addon. Most of them run within FreeCAD itself and use the Test workbench, but it is possible in some cases to do some external testing of certain types of addons, depending on exactly which features you provide.

## Testing with the Test Workbench

The [Test Workbench][wiki-testing] within FreeCAD is a Python [`unittest`][py-unittest]-based test runner. If you structure your tests to register themselves with it then a) your tests will appear in the Test Runner GUI in the FreeCAD Test Workbench (for manually-run testing), and b) you can run FreeCADCmd and FreeCAD on the command-line with an argument to run just *your* tests. Then your CI system can use FreeCAD as its test-runner, and you will have access to the full FreeCAD environment during the test runs. This is the path that most addons take.

### Creating a test framework

Your tests should derive from [`unittest.TestCase`][py-testcase], part of the Python-standard [`unittest`][py-unittest] package:
```
import unittest

import FreeCAD

from freecad.Midvale import School, DoorException, Door

class TestMidvale(unittest.TestCase):

    def setUp(self):
        """Runs at the beginning of every single test invocation."""

        # Put code here that sets up a clean test environment. If you have to
        # access the filesystem, make sure you use a *unique* temporary directory,
        # and delete it when you are done.

    def tearDown(self):
        """Runs after the completion of each test."""

        # Clean up after yourself. Good developer.

    def test_entering_school(self):
        """Make sure the door swings the right way"""
        with self.assertRaises(DoorException):
            School.enter("Push")
```

### Writing tests

This really represents general test-writing advice, it's not specific to FreeCAD. But in order for your tests to be at their most useful, it's better to have *lots* of *small* tests, rather than a few big, complex ones. Think of structuring your tests so that each one verifies one specific behavior, or exercises one specific branch of code that wasn't being tested before. Think adversarially! Don't try to write tests to verify the behavior you know is right: instead, try to think of edge cases. **Try** to break your code in the tests! That's when they are at their most useful.

Within the context of FreeCAD, there are a few particular things that are useful to test. For example, if your Addon generates geometry, then you probably want to verify that a) it generates the expected geometry *today*, but also that b) if FreeCAD changes at some point, you catch the change and can update your Addon ASAP. Two good tests of this are to check the bounding box of an expected bit of geometry (because it's cheap to calculate, though of somewhat limited accuracy), and to check the volume of the resulting shape. This is a more expensive, but more accurate, check. Both properties are exposed on every `Part.Shape`; see the FreeCAD wiki's [Topological data scripting][wiki-topo] page for the Part shape API, and the [Scripted objects][wiki-scripted] page for the `Part::FeaturePython` proxy pattern used in the examples below.

To check the bounding box, use [`assertAlmostEqual`][py-assertalmostequal] with a loose tolerance:
```
def test_door_bounding_box(self):
    """The Midvale standard door is 900 x 2100 x 40 mm."""
    doc = FreeCAD.newDocument("MidvaleBBoxTest")
    try:
        door = doc.addObject("Part::FeaturePython", "Door")
        Door(door)
        door.Width     =  900.0
        door.Height    = 2100.0
        door.Thickness =   40.0
        doc.recompute()

        bbox = door.Shape.BoundBox
        self.assertAlmostEqual(bbox.XLength,  900.0, delta=0.1)
        self.assertAlmostEqual(bbox.YLength,   40.0, delta=0.1)
        self.assertAlmostEqual(bbox.ZLength, 2100.0, delta=0.1)
    finally:
        FreeCAD.closeDocument(doc.Name)
```

To check the volume you can use a tighter tolerance, but still make sure to use *some* tolerance, since floating point numbers are complex beasts and you can't really expect a full every-bit-equality.
```
def test_door_volume(self):
    """A 900 x 2100 x 40 mm slab has a volume of 75,600,000 mm^3."""
    doc = FreeCAD.newDocument("MidvaleVolumeTest")
    try:
        door = doc.addObject("Part::FeaturePython", "Door")
        Door(door)
        door.Width     =  900.0
        door.Height    = 2100.0
        door.Thickness =   40.0
        doc.recompute()

        expected = 900.0 * 2100.0 * 40.0
        self.assertAlmostEqual(door.Shape.Volume, expected, delta=1.0)
    finally:
        FreeCAD.closeDocument(doc.Name)
```

### Registering your tests

Tests are registered in two different places, depending on whether they need the GUI to be running (really, whether they need a Qt event loop, for example because they use Qt's threading mechanism), or whether they are CLI-only. Generally speaking you should work to divide your Addon into GUI and non-GUI code, in part because testing non-GUI code is typically *much* easier than testing the GUI.

So for example, your __init__.py file might contain
```
import FreeCAD

# All test modules that do not require a running Qt event loop go here.
# The Test workbench reads this list to populate its test runner, and the
# `--run-test` command-line flag iterates the same list.

FreeCAD.__unit_test__ += [
    "freecad.Midvale.tests.test_door",
    "freecad.Midvale.tests.test_school",
]
```

Your init_gui.py might contain:
```
import FreeCADGui

# Test modules that need a Qt event loop (dialogs, signals, threading) go
# here instead. These will only be discoverable when FreeCAD is run with
# its GUI, and must be invoked via `FreeCAD --run-test`, not `freecadcmd`.

FreeCADGui.__unit_test__ += [
    "freecad.Midvale.tests.test_door_dialog",
]
```

### Running your tests on the command line

Once your tests are registered, FreeCAD can run them from the command line and exit with a status code suitable for use in CI. The headless build, `freecadcmd`, is the right choice for tests that do not need the GUI:

```
freecadcmd --run-test 0
```

The numeric `0` argument runs every module that has been added to `FreeCAD.__unit_test__`. To run a single module, pass its dotted module name in place of the number:

```
freecadcmd --run-test freecad.Midvale.tests.test_door
```

Tests that require a Qt event loop, those registered via `FreeCADGui.__unit_test__`, must instead be run through the GUI build. The same flag is accepted, and FreeCAD will exit when the test run completes:

```
FreeCAD --run-test freecad.Midvale.tests.test_door_dialog
```

In both cases the process exits with status 0 if every test passed and a non-zero status otherwise, which is the behaviour CI runners need in order to fail a build on a broken test. A minimal GitHub Actions step looks like this:

```
-   name : Run Midvale tests
    run  : freecadcmd --run-test 0
```

## Testing outside FreeCAD

Another approach to testing is to write a dedicated test app of your own that imports pieces of your addon that *don't* require FreeCAD at all (eliminating the need to install FreeCAD in your test environment, which can be quite slow). This is a much more advanced testing mechanism, and is limited to testing things that don't interact with FreeCAD, or to interactions that you create **test mocks** for. Again, this is a more advanced testing mechanism, so if the word **test mock** doesn't mean anything to you, this probably isn't the path you want to take. Python's [`unittest.mock`][py-mock] module is the standard tool for this.


[py-unittest]:          https://docs.python.org/3/library/unittest.html
[py-testcase]:          https://docs.python.org/3/library/unittest.html#unittest.TestCase
[py-assertalmostequal]: https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
[py-mock]:              https://docs.python.org/3/library/unittest.mock.html

[wiki-testing]:         https://wiki.freecad.org/Testing
[wiki-scripted]:        https://wiki.freecad.org/Scripted_objects
[wiki-topo]:            https://wiki.freecad.org/Topological_data_scripting