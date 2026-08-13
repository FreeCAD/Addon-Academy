---
layout : Default
---

# Gui Commands

A Command is a single user-invocable action, bound to a toolbar button, menu item, context-menu entry, or keyboard shortcut. Commands are the granular building blocks of an addon's user interface; a [Workbench][Workbench] bundles them into toolbars and menus. This page covers how to write and register a command.

For a complete working example, see the [Minimal Workbench demo][MinimalWB].


## Where commands live

Convention is to put commands in a `Commands.py` module inside your addon's namespace package, alongside `init_gui.py`:

```
freecad/MyAddon/
├─ __init__.py
├─ init_gui.py
└─ Commands.py
```

For larger addons, split into multiple files (`CommandsFoo.py`, `CommandsBar.py`) or a `commands/` subpackage. Each file registers its commands with `FreeCADGui.addCommand(...)` at module scope, so that importing the file has the side effect of making the commands available.


## The command class

A command is a plain Python class (not a subclass of anything) with three methods that FreeCAD looks up by name via duck typing (Python's most delightfully-named thing):

```python
import FreeCAD
import FreeCADGui


class RuinThingsCommand:

    def GetResources(self):
        return {
            "MenuText": "Ruin things",
            "ToolTip":  "Deletes a randomly-selected set of edges from your model",
            "Pixmap":   "MyAddon_Explosion.svg",
            "Accel":    "Ctrl+Alt+Shift+R",
        }

    def IsActive(self):
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage("This was probably a mistake...\n")


FreeCADGui.addCommand("MyAddon_Hello", RuinThingsCommand())
```


### `GetResources()`

Returns a dictionary describing how the command appears in the UI. Recognized keys:

| Key              | Required | Purpose                                                                                                 |
|------------------|----------|---------------------------------------------------------------------------------------------------------|
| `MenuText`       | Yes      | The command's label in menus and its default button tooltip.                                            |
| `ToolTip`        | No       | A longer description shown on hover over toolbar buttons.                                               |
| `Pixmap`         | No       | A filename for the button icon, resolved against registered icon paths. See [Icons & resources][Icons]. |
| `Accel`          | No       | A keyboard shortcut string such as `"Ctrl+Shift+H"` or `"Shift+A"`.                                     |
| `StatusTip`      | No       | Text shown in the status bar when the command is highlighted. Falls back to `ToolTip` if absent.        |
| `WhatsThis`      | No       | Text shown by the "What's this?" help mechanism.                                                        |
| `CmdType`        | No       | Declares what the command alters. Governs availability while a task dialog is open; see below.          |

A command missing `GetResources` will technically still be registered, but it cannot be placed into a menu or toolbar because FreeCAD will have no label to display. In practice, every command class should provide a `GetResources` method.


### `CmdType` {#cmdtype}

An optional string in `GetResources()` declaring what the command changes. FreeCAD uses the declaration to decide whether the command stays available while a *task dialog* is open.

Five values are recognized:

| Value            | Meaning                                                                                       |
|------------------|-----------------------------------------------------------------------------------------------|
| `AlterDoc`       | The command modifies the document.                                                            |
| `Alter3DView`    | The command modifies the 3D view.                                                             |
| `AlterSelection` | The command modifies the selection.                                                           |
| `ForEdit`        | The command remains available while a task dialog is open.                                    |
| `NoTransaction`  | Do not set up an automatic transaction. Currently has no effect on addon commands, see below. |

Several values may be combined in the one string. FreeCAD searches the string for each value as a substring, so the separator is irrelevant and `"ForEdit AlterDoc"`, `"ForEdit, AlterDoc"`, and `"ForEditAlterDoc"` are all equivalent. A space-separated list is the conventional form:

```python
def GetResources(self):
    return {
        "MenuText": "Add construction line",
        "CmdType":  "ForEdit AlterDoc",
    }
```

Because matching is by substring, a misspelled value is not reported as an error. `"Foredit"` matches nothing and leaves the command with no declared type at all.


#### Why a command stops working in Sketcher

When `GetResources()` omits `CmdType`, the command keeps the default that FreeCAD's `Command` constructor assigns, which is `AlterDoc | Alter3DView | AlterSelection`. Every plain Python command therefore declares that it modifies the document if it doesn't otherwise specify a `CmdType`.

Before enabling a command's toolbar button or menu entry, FreeCAD asks the active task dialog whether each declared alteration is permitted. The base `TaskDialog` class permits view and selection changes but **not** document changes. Individual dialogs may override that, and a handful in core do permit document changes, but the great majority either inherit the default or explicitly reaffirm it; Sketcher's edit dialog is in the latter group. A command carrying the default type is consequently disabled the moment such a dialog opens, with nothing in the addon's own code to suggest why. This is a frequent source of confusion, because the symptom (a button that greys out on entering Sketcher edit mode) has no visible connection to a resource key the addon never set.

Measured button states for three otherwise identical commands:

| Situation                | Default `CmdType` | `"ForEdit"` | `"Alter3DView"` |
|--------------------------|-------------------|-------------|-----------------|
| No task dialog open      | Enabled           | Enabled     | Enabled         |
| Sketch edit mode open    | **Disabled**      | Enabled     | Enabled         |
| After leaving edit mode  | Enabled           | Enabled     | Enabled         |

`ForEdit` skips the permission check entirely, which is why adding it resolves the problem. It is not the only remedy, and often not the most appropriate one. A command that declares its actual scope accurately also stays available whenever that scope excludes the document: the third column above is a command that only changes the 3D view, and task dialogs permit view changes by default. Declare the alterations the command genuinely performs, and reserve `ForEdit` for commands that really do need to modify the document from inside an edit session.

`CmdType` does not replace `IsActive()`. The two checks are independent and both must pass: FreeCAD applies the task-dialog check first, then calls `IsActive()`.


#### `NoTransaction`

`NoTransaction` is listed above for completeness. FreeCAD parses the value for Python commands, but nothing then consults it for them: the only code that reads the flag is the built-in `Std_Refresh` command. Setting it on an addon command currently has no effect. Note also that `PythonGroupCommand`, the class behind grouped drop-down commands, parses only the first four values and ignores `NoTransaction` outright.


### `IsActive()`

Returns a boolean indicating whether the command is currently available. A `False` return disables the toolbar button and menu entry. Typical uses:

```python
def IsActive(self):
    return FreeCAD.ActiveDocument is not None
```

```python
def IsActive(self):
    sel = FreeCADGui.Selection.getSelection()
    return len(sel) == 1
```

`IsActive` should be kept fast: prefer no disk access, no network calls, no walking a large document graph. If you need an expensive check, consider caching the result (of course, proper cache invalidation is left as an exercise to the reader…).

If your command has no availability requirements, either return `True` unconditionally or omit `IsActive` entirely.

`IsActive()` is your addon's own availability logic, and it is not the only thing that can disable a command. FreeCAD applies a separate check based on the [`CmdType`](#cmdtype) resource, which governs whether the command survives while a task dialog is open. A command returning `True` from `IsActive()` can still appear greyed out if its `CmdType` declaration fails that check.


### `Activated()`

The method FreeCAD calls when the user triggers the command (clicking a toolbar button, selecting a menu item, or typing the shortcut). This is where your command actually does its work:

```python
def Activated(self):
    doc = FreeCAD.ActiveDocument
    doc.openTransaction("Ruin everything")
    try:
        # ... your work here ...
        doc.commitTransaction()
    except Exception:
        doc.abortTransaction()
        raise
```

Wrap document-modifying work in `openTransaction` / `commitTransaction` so the user can undo it with a single Ctrl+Z. The argument to `openTransaction` is the label that appears in the Undo menu.


## Registering the command

At the bottom of the module that defines the command class, call `FreeCADGui.addCommand`:

```python
FreeCADGui.addCommand("MyAddon_Ruin", RuinThingsCommand())
```

The first argument is the **command name**, a string identifier used to refer to the command from toolbars, menus, and other places. The second is an **instance of the class** (not the class itself).

Once registered, the command is available to every workbench within FreeCAD, not only your own. Prefixing it with your addon's name is a basic "poor man's namespace" mechanism (see below).


## Command naming

Command names are a flat, global namespace across FreeCAD. Convention is to prefix with your addon's name and an underscore:

-   `MyAddon_DoSomething`
-   `MyAddon_OpenDialog`
-   `MyAddon_Export_XYZ`

Avoid collisions with core FreeCAD commands, which use `Std_*`, `Part_*`, `Sketcher_*`, and similar prefixes. Giving every command your addon's prefix makes it visually obvious which addon owns a given command and prevents silent clobbering if two addons pick the same command name. Of course, if two addons pick the same *prefix*, all bets are off. So try to make yours unique. Like a snowflake❄️.


## Placing commands in the UI

Commands are registered once and then referenced by name wherever you want them to appear. The workbench methods `appendToolbar`, `appendMenu`, and `appendContextMenu` take lists of command names. See [Workbench registration][Workbench] for the full description.

Short version:

```python
# inside your Workbench class's Initialize(self):
self.appendToolbar("My tools", ["MyAddon_Hello"])
self.appendMenu("My Addon",    ["MyAddon_Hello"])
```

You can also reference core FreeCAD commands from your own toolbars and menus, since all registered commands share the same global namespace:

```python
self.appendToolbar("My tools", ["Std_New", "MyAddon_Hello"])
```

Useful built-ins include `Std_New`, `Std_Open`, `Std_Save`, `Std_Undo`, `Std_Redo`, and `Std_SelectAll`.


## Separators

To insert a separator between groups of commands in a toolbar or menu, use the special string `"Separator"`:

```python
self.appendToolbar("My tools", ["MyAddon_One", "Separator", "MyAddon_Two"])
```

*Don't translate "Separator"*, it's hard-coded into FreeCAD's source as a special name, parsed during menu and toolbar creation.

## Translation

User-visible strings in `GetResources` should be wrapped with `QT_TRANSLATE_NOOP`, using the command name as the context:

```python
from PySide.QtCore import QT_TRANSLATE_NOOP

class HelloCommand:
    def GetResources(self):
        return {
            "MenuText": QT_TRANSLATE_NOOP("MyAddon_Hello", "Hello"),
            "ToolTip":  QT_TRANSLATE_NOOP("MyAddon_Hello", "Print a hello message."),
        }
```

See [Translations][Translations] for why `QT_TRANSLATE_NOOP` rather than `translate()`, and for the broader translation workflow.


## See also

-   [Minimal Workbench demo][MinimalWB]: a complete working workbench with a single command.
-   [Workbench registration][Workbench]: how to place commands into toolbars, menus, and context menus.
-   [Icons & resources][Icons]: how `Pixmap` filenames are resolved at runtime.
-   [Translations][Translations]: wrapping `GetResources` strings for translation.
-   [Logging & console][Logging]: how to report progress or errors from `Activated`.


[MinimalWB]: ../../../Demos/Minimal-Workbench
[Workbench]: ../Workbench
[Icons]: ../Icons
[Translations]: ../Translations
[Logging]: ../Logging
