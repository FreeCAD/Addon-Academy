---
layout : Default
---

# Workbench manipulators

A workbench manipulator is an object that edits FreeCAD's toolbars, menus, and context menus as each workbench is set up. It is the mechanism used for contributing user interface elements to workbenches your addon does not own, including the case of an addon that defines no [workbench][Workbench] at all.

Manipulators are available beginning in FreeCAD 1.0.

For complete working examples, see the [Extend Toolbar demo][ExtendToolbar], which adds one command to an existing toolbar, and the [New Toolbar demo][NewToolbar], which builds a new toolbar in an existing workbench.


## Contents

* TOC
{:toc}


## Registering a manipulator

A manipulator is a plain Python object, not a subclass of anything. FreeCAD looks up its methods by name and skips any that are absent, so implement only the ones you need:

```python
import FreeCADGui


class Manipulator:

    def modifyToolBars(self):
        return [{"append": "MyAddon_Hello", "toolBar": "File"}]


FreeCADGui.addWorkbenchManipulator(Manipulator())
```

`FreeCADGui.removeWorkbenchManipulator(obj)` unregisters a manipulator again, matching on object identity, so keep a reference to the instance if you intend to remove it later.

Four methods are recognized:

| Method                           | Purpose                                                      |
|----------------------------------|--------------------------------------------------------------|
| `modifyToolBars()`               | Add or remove toolbars and toolbar buttons.                  |
| `modifyMenuBar()`                | Add or remove menu entries.                                  |
| `modifyContextMenu(recipient)`   | Add or remove right-click menu entries.                      |
| `modifyDockWindows()`            | Reserved. Currently does nothing, see below.                 |


## When manipulators run

Every registered manipulator runs on **every workbench activation** (*not* e.g. once at startup, or only for your own workbench). For example, switching from Part to Sketcher and back runs your manipulator three times, and the toolbar and menu trees it edits are rebuilt from scratch each time.

This leads to three guidelines about how manipulator methods should be written:

-   **Keep them cheap.** They are instantiated directly in the path of a user action that should feel instant.
-   **They must determine for themselves which workbench they are being called for.** Nothing is passed in; see [Scoping to one workbench](#scoping) below.
-   **Failures are not reported.** FreeCAD catches any exception a manipulator method raises, reports it to the Report view, and carries on with the activation. Your toolbar quietly fails to appear rather than breaking FreeCAD, which is good for users, but unhelpful for *you*. Check the Report view when a manipulator seems to do nothing.


## Return values

Every method returns either a single dictionary or a sequence of dictionaries. Both of these are valid:

```python
return {"append": "MyAddon_Hello", "toolBar": "File"}
```

```python
return [
    {"append": "MyAddon_Hello", "toolBar": "File"},
    {"remove": "Std_ViewFitAll"},
]
```

Anything else, including `None`, is ignored without complaint. Returning an empty list is the conventional way to say "no changes for this workbench".

Each individual dictionary describes **one** change, keyed by the operation: `insert`, `append`, or `remove`. The value is the command name to act on. If a dictionary carries more than one operation key, only the first of `insert`, `append`, `remove` is honored, in that order. Companion keys name the target the operation applies to. To apply multiple operations, return multiple dictionaries, one operation in each.


## `modifyToolBars()`

| Operation | Value                        | Companion key | Effect                                                        |
|-----------|------------------------------|---------------|---------------------------------------------------------------|
| `append`  | Command name to add          | `toolBar`     | Appends the command to the end of the named toolbar.          |
| `insert`  | Command name to add          | `toolItem`    | Inserts the command immediately before the named command.     |
| `remove`  | Toolbar or command name      | (none)        | Removes an entire toolbar, or a single command from one.      |

```python
def modifyToolBars(self):
    return [
        {"append": "MyAddon_Hello", "toolBar": "File"},
        {"insert": "MyAddon_Setup", "toolItem": "Std_Open"},
        {"remove": "MyAddon_Obsolete"},
    ]
```

`remove` is deliberately loose: FreeCAD first looks for a *toolbar* with the given name and removes the whole thing, and only if that fails does it search inside each toolbar for a *command* of that name. A name collision between a toolbar and a command therefore resolves in favor of the toolbar. Removing the root of the toolbar tree is refused, with a warning in the Report view.

Toolbar lookup for `append` searches the named toolbar among the top-level toolbars only. It does not descend further, which matters when creating a new toolbar; see below.


## `modifyMenuBar()`

| Operation | Value                   | Companion keys        | Effect                                                              |
|-----------|-------------------------|-----------------------|---------------------------------------------------------------------|
| `append`  | Command name to add     | `menuItem`            | Appends the command to the end of the menu *containing* `menuItem`. |
| `insert`  | Command name to add     | `menuItem`, `after`   | Inserts the command relative to `menuItem`.                         |
| `remove`  | Command or menu name    | (none)                | Removes the named entry.                                            |

```python
def modifyMenuBar(self):
    return [
        {"append": "MyAddon_Hello",  "menuItem": "Std_DlgMacroRecord"},
        {"insert": "MyAddon_Setup",  "menuItem": "Std_DlgParameter"},
        {"insert": "MyAddon_Finish", "menuItem": "Std_DlgParameter", "after": ""},
    ]
```

Two points are easy to get wrong here.

**`menuItem` names an entry, not a menu.** For `append`, FreeCAD locates the menu that *contains* `menuItem` and appends to that. The example above puts `MyAddon_Hello` at the bottom of the Macro menu by naming an item that already lives there. Naming the menu itself does not append into it.

**`after` is a flag, not a value.** Only the presence of the `after` key is checked; its value is ignored, so `"after": ""` and `"after": True` behave identically. When `after` is present and `menuItem` is the last entry in its menu, there is nothing to insert before and the change is silently skipped.

Unlike toolbars, menu lookup is recursive, so `menuItem` can name an entry at any depth in the menu tree.


## `modifyContextMenu(recipient)`

Takes the same dictionaries as `modifyMenuBar()`. The `recipient` argument identifies what the user right-clicked:

| `recipient` | Where the click happened |
|-------------|--------------------------|
| `"Tree"`    | The model tree           |
| `"View"`    | The 3D view              |
| `"Sketch"`  | The Sketcher editor      |

```python
def modifyContextMenu(self, recipient):
    if recipient == "View":
        return [{"insert": "MyAddon_Hello", "menuItem": "Std_ViewFitAll"}]
    return []
```

These strings are capitalized and are the same values passed to a workbench's own `ContextMenu()` method.


## `modifyDockWindows()`

Reserved, and currently a no-op. FreeCAD calls the method and parses its return value, then discards the result: the function that would apply the changes is currently unimplemented. Do not rely on it, or its absence. To contribute a dock widget today, add it directly through Qt with `FreeCADGui.getMainWindow().addDockWidget(...)`.


## Creating a new toolbar {#new-toolbar}

`modifyToolBars()` has no "create a toolbar" operation, but it does not need one. Toolbars live in a tree whose root is an unnamed node, and every direct child of that root becomes a toolbar. Appending to the empty name therefore adds a new toolbar rather than a new button:

```python
def modifyToolBars(self):
    return [
        {"append": "Calvinball", "toolBar": ""},
        {"append": "Calvinball_Score", "toolBar": "Calvinball"},
        {"append": "Calvinball_Rule",  "toolBar": "Calvinball"},
    ]
```

The first dictionary creates the toolbar. The rest fill it, and **must come afterwards**: the toolbar has to exist as a named child before a lookup can find it. Reversing the order produces no error and no toolbar.

The new toolbar behaves in every respect like a core one. It is visible by default, it gets an entry in the toolbar visibility menu, and the user can move, hide, or restore it normally.


## Scoping to one workbench {#scoping}

Because a manipulator runs on every activation, the code above adds its toolbar to *every* workbench. Restricting it to one means determining which workbench is currently being set up. The correct way of doing this is not the one you are expecting!

`FreeCADGui.activeWorkbench()` returns the correct handler object even mid-activation, but calling `.name()` on it raises `AttributeError` during a core workbench's first activation. `name()` is a thin wrapper that delegates to a `__Workbench__` attribute FreeCAD injects into the handler, and for workbenches implemented in C++ that injection happens only after activation finishes, which is **after your manipulator has already run**.

The failure is order-dependent, which makes it a particularly unpleasant trap. I'm not bitter. Measured from inside `modifyToolBars()`:

| Situation                                        | `activeWorkbench().name()` | Identity lookup |
|--------------------------------------------------|----------------------------|-----------------|
| First activation of a core workbench             | **AttributeError**         | Correct name    |
| Any later activation of the same workbench       | Correct name               | Correct name    |
| Workbench already active at startup              | Correct name               | Correct name    |
| First activation of a Python (addon) workbench   | Correct name               | Correct name    |

An addon author who tests by switching away and back, or who only tests against their own Python workbench, sees none of this. The user whose FreeCAD starts in Part does.

Since the handler object itself is already correct, recover the name by identity instead by including this method in your Addon:

```python
def active_workbench_name():
    active = FreeCADGui.activeWorkbench()
    for name, handler in FreeCADGui.listWorkbenches().items():
        if handler is active:
            return name
    return ""
```

`FreeCADGui.listWorkbenches()` returns FreeCAD's internal name-to-handler dictionary directly, so the identity comparison is exact rather than a guess based on class names. Guard the manipulator with it:

```python
def modifyToolBars(self):
    if active_workbench_name() != "ThatOneWorkbenchICareAbout":
        return []
    ...
```

Returning an empty list for other workbenches gives exactly the behavior core workbenches get: the toolbar object persists but is hidden, and its entry in the visibility menu is hidden with it.


## Pitfalls

**Toolbar and menu names are a global namespace.** There are no identifiers, only names, and yours share one namespace with every core toolbar and every other addon's. Prefix new toolbar names with your addon's name for the same reason you prefix [command names][Commands].

**A toolbar's name is also a preference key.** FreeCAD records whether the user has hidden a toolbar under its name, in `BaseApp/MainWindow/Toolbars`. Renaming a toolbar in a later release silently discards that preference, and the toolbar reappears for everyone who had hidden it.

**Toolbar titles are translated.** The name is passed through Qt translation in the `Workbench` context before being shown, so a name that collides with a core toolbar name may be displayed translated in ways you did not intend. See [Translations][Translations].

**Core toolbar and menu names change between FreeCAD versions.** Targeting `"File"` or `"Std_Open"` is a version-coupling that nothing will warn you about; the change simply stops happening. Test against every FreeCAD version your manifest claims to support, and see [FreeCAD version compatibility][Compatibility].

**Nothing tells you a name was wrong.** Every operation here fails silently when its target cannot be found. If a change does not appear, the first thing to check is the spelling of the target name, and the second is the Report view.


## See also

-   [New Toolbar demo][NewToolbar]: a complete workbench-less addon that builds a toolbar in the Part workbench.
-   [Extend Toolbar demo][ExtendToolbar]: the smaller case of adding one command to a toolbar that already exists.
-   [Gui Commands][Commands]: how the command names used throughout this page are defined and registered.
-   [Workbench registration][Workbench]: the other way to contribute a toolbar, when your addon does own a workbench.
-   [Icons & resources][Icons]: how the buttons on your new toolbar get their icons.


[Commands]: ../Commands
[Workbench]: ../Workbench
[Icons]: ../Icons
[Translations]: ../Translations
[Compatibility]: ../../Maintaining/Compatibility

[NewToolbar]: ../../../Demos/New-Toolbar
[ExtendToolbar]: ../../../Demos/Extend-Toolbar
