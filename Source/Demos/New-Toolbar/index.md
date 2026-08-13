---
layout : Default
---

# Demo : New Toolbar

An addon that adds a new toolbar, holding several buttons, to a workbench it does not own. It defines no workbench of its own, contributes no menu, and appears in the user's FreeCAD only as a toolbar in the Part workbench.

This is the counterpart to the [Extend Toolbar][ExtendToolbar] demo, which adds a single command to a toolbar that already exists. Creating a whole toolbar takes a different technique, described under [How the toolbar is built](#how) below.

Every file in this demo is dedicated to the public domain under [CC0-1.0][CC0]. Copy and adapt freely.


## Contents

* TOC
{:toc}


## Result

Switching to the Part workbench shows a three-button Calvinball toolbar. Each button prints to the Report view. Switching to any other workbench hides the toolbar again, exactly as though it belonged to Part all along.

<img alt = 'The three-button Calvinball toolbar' src = './Media/Toolbar.webp' />


## Directory layout

```
Calvinball/
├─ package.xml
├─ Resources/
│  └─ Icons/
│     ├─ Logo.svg
│     ├─ Calvinball_Score.svg
│     ├─ Calvinball_Rule.svg
│     └─ Calvinball_Mask.svg
└─ freecad/
   └─ Calvinball/
      ├─ __init__.py
      ├─ init_gui.py
      ├─ Manipulator.py
      └─ Commands.py
```

The layout is the ordinary Modern namespaced one described in [Structuring][Structuring]. Nothing about a workbench-less addon changes it.


## The files

### `package.xml`

The [Addon Manifest][Manifest]. Because the addon ships no workbench, no macro, and no preference pack, its content item is `<other/>`:

```xml
<content>
    <other/>
</content>
```

`<content>` is required and cannot be empty, so `<other/>` is what an addon of this kind declares. Note that the Addon Manager only recognized `<other/>` from FreeCAD 1.1 onward, which is why the manifest sets `<freecadmin>1.1.0</freecadmin>` even though the manipulator API itself dates back to 1.0. See [feature availability by FreeCAD version][ManifestAvailability].

Source: [`package.xml`][Source-pkg]

### `freecad/Calvinball/init_gui.py`

The file FreeCAD runs when starting the GUI. FreeCAD imports `init_gui.py` for every installed addon regardless of what the addon contains, which is what makes a workbench-less addon possible at all.

It registers the icons directory and the manipulator, and that is all. There is no `FreeCADGui.addWorkbench()` call.

Source: [`init_gui.py`][Source-gui]

### `freecad/Calvinball/Manipulator.py`

The interesting file. It defines the [workbench manipulator][Manipulators] that builds the toolbar, plus the helper that works out which workbench is being set up.

Source: [`Manipulator.py`][Source-manip]

### `freecad/Calvinball/Commands.py`

Three ordinary [commands][Commands]. Nothing here is specific to toolbars or to manipulators; these are the same command classes any workbench would use.

Source: [`Commands.py`][Source-cmds]


## How the toolbar is built {#how}

`modifyToolBars()` offers `append`, `insert`, and `remove`, and none of them creates a toolbar. The trick is that toolbars live in a tree whose root node has no name, and every direct child of that root becomes a toolbar. Appending to the empty name therefore adds a toolbar rather than a button:

```python
changes = [{"append": _TOOLBAR, "toolBar": ""}]
changes += [{"append": command, "toolBar": _TOOLBAR} for command in _COMMANDS]
```

Order matters. The first dictionary creates the toolbar; the rest fill it, and cannot run until the toolbar exists as a named child. Reversing the two steps produces no error and no toolbar.


## Restricting the toolbar to one workbench

A manipulator runs on **every** workbench activation, so the code above by itself would put the Calvinball toolbar in every workbench in FreeCAD. Confining it to Part means knowing which workbench is being set up, and the obvious way to ask fails:

```python
FreeCADGui.activeWorkbench().name()   # AttributeError, sometimes
```

During a core workbench's first activation the handler object does not yet carry the attribute that `name()` delegates to, and the call raises. On every later activation it works. An addon that gets this wrong therefore behaves correctly for the developer who switches back and forth while testing, and fails for the user whose FreeCAD opens in Part.

The handler object itself is correct even on first activation, so the demo recovers the name by identity:

```python
def active_workbench_name():
    active = FreeCADGui.activeWorkbench()
    for name, handler in FreeCADGui.listWorkbenches().items():
        if handler is active:
            return name
    return ""
```

Returning an empty list from `modifyToolBars()` for every other workbench gives the toolbar the same treatment core toolbars get: hidden, along with its entry in the toolbar visibility menu.

`Manipulator.py` also defers importing `Commands` until the manipulator has decided it is in the right workbench. Since there is no workbench class here, there is no `Initialize()` to defer that import into, and importing at the top of `init_gui.py` would put it on the startup path of every FreeCAD user who installs the addon. See [keeping startup fast][WorkbenchStartup].


## Trying it out

1.  Install the addon by downloading [`Calvinball.zip`][Zip] and extracting it into your FreeCAD user `Mod/` directory. To install from source instead, or to symlink for live edits, follow [Installing your addon locally][LocalInstall] using the [`Source/`][Source-root] directory next to this page.
2.  Start FreeCAD and switch to the Part workbench. A three-button Calvinball toolbar appears.
3.  Click the buttons and watch the Report view.
4.  Switch to another workbench. The toolbar disappears, and reappears on returning to Part.

To put the toolbar in a different workbench, change `_TARGET_WORKBENCH` at the top of `Manipulator.py` to that workbench's internal name, or set it to `None` to add the toolbar everywhere.


## Where to go next

-   [Workbench manipulators][Manipulators] for the full protocol: menus, context menus, removal, and the pitfalls of addressing things by name.
-   [Extend Toolbar][ExtendToolbar] for the simpler case of adding one command to an existing toolbar.
-   [Gui Commands][Commands] for more on the command classes this demo registers.
-   [Icons & resources][Icons] for how `Pixmap` filenames are resolved against the registered icon path.


[Manifest]: ../../Topics/Structuring/Manifest
[ManifestAvailability]: ../../Topics/Structuring/Manifest#availability
[Structuring]: ../../Topics/Structuring
[LocalInstall]: ../../Guides/Developing/Local-Install
[Manipulators]: ../../Guides/Code/Manipulators
[Commands]: ../../Guides/Code/Commands
[Icons]: ../../Guides/Code/Icons
[WorkbenchStartup]: ../../Guides/Code/Workbench#keeping-startup-fast

[ExtendToolbar]: ../Extend-Toolbar

[CC0]: https://creativecommons.org/publicdomain/zero/1.0/

[Source-root]: ./Source/
[Source-pkg]: ./Source/package.xml
[Source-gui]: ./Source/freecad/Calvinball/init_gui.py
[Source-manip]: ./Source/freecad/Calvinball/Manipulator.py
[Source-cmds]: ./Source/freecad/Calvinball/Commands.py
[Zip]: ./Calvinball.zip
