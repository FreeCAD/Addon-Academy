---
layout : Default
---

# Demo : Minimal Workbench

The smallest useful FreeCAD workbench: registers a new entry in the Workbench selector, contributes one command to a toolbar and menu, and prints a message to the Report view when the command is clicked.

Every file in this demo is dedicated to the public domain under [CC0-1.0][CC0]. Copy and adapt freely.


## Directory layout

```
MinimalWorkbench/
├─ package.xml
├─ Resources/
│  └─ Icons/
│     └─ Logo.svg
└─ freecad/
   └─ MinimalWorkbench/
      ├─ __init__.py
      ├─ init_gui.py
      └─ Commands.py
```

The top-level `MinimalWorkbench/` is your git repository root. The `freecad/` directory has no `__init__.py` because `freecad` is a [namespace package][PEP420] shared with every other addon on the user's system. Your addon lives in `freecad/<YourAddonName>/`, and *that* directory has a normal `__init__.py`. See [Structuring][Structuring] for background.


## The files

### `package.xml`

The [Addon Manifest][Manifest] declares your addon's name, version, license, and content. For a workbench it must include a `<workbench>` content item whose `<classname>` matches the class registered in `init_gui.py`.

Source: [`package.xml`][Source-pkg]

### `freecad/MinimalWorkbench/__init__.py`

Nearly empty. It only has to exist so that `freecad/MinimalWorkbench/` is treated as a proper Python package (as opposed to the enclosing `freecad/`, which is intentionally *not* a package).

Source: [`__init__.py`][Source-init]

### `freecad/MinimalWorkbench/init_gui.py`

The file FreeCAD runs when starting the GUI. It:

-   Defines `MinimalWorkbench`, a subclass of `FreeCADGui.Workbench`.
-   Sets `MenuText`, `ToolTip`, and `Icon` (what the user sees in the Workbench selector). Note that in a "real" addon we encourage [translating these strings][Translating]. The `Icon` attribute must be an absolute path resolved at class-definition time, so the file computes it from `__file__` rather than relying on a later `addIconPath` call.
-   Defines `Initialize()`, which imports the `Commands` module (whose import side-effect is registering the command) and appends the command to a toolbar and menu.
-   Returns `"Gui::PythonWorkbench"` from `GetClassName()`, which is required for Python workbenches. Do not modify that return string!
-   Registers the workbench instance via `FreeCADGui.addWorkbench()`.

Source: [`init_gui.py`][Source-gui]

### `freecad/MinimalWorkbench/Commands.py`

Defines `HelloCommand`, a class with:

-   `GetResources()`: returns a dictionary with `MenuText` and `ToolTip` (and optionally `Pixmap` and `Accel`).
-   `IsActive()`: returns `True` whenever the command should be enabled. Return `False` to grey out the toolbar button.
-   `Activated()`: the code that runs when the user clicks the toolbar button.

At module import time the file calls `FreeCADGui.addCommand("Minimal_Hello", HelloCommand())`, registering the command by name so `init_gui.py` can refer to it.

Source: [`Commands.py`][Source-cmds]


## Trying it out

1.  Install the addon by downloading [`MinimalWorkbench.zip`][Zip] and extracting it into your FreeCAD user `Mod/` directory. To install from source instead, or to symlink for live edits, follow [Installing your addon locally][LocalInstall] using the [`Source/`][Source-root] directory next to this page.
2.  Start FreeCAD. "Minimal" should appear in the Workbench selector.
3.  Switch to the Minimal workbench. A single-button "Minimal" toolbar appears. Click it, and "Hello from the Minimal workbench!" will appear in the Report view.


## Where to go next

-   [Workbench registration][CodeWorkbench] for a deeper walk-through of the Workbench class.
-   [Gui Commands][CodeCommands] for more on commands, toolbars, and menus.
-   [Icons & resources][CodeIcons] for how to give your commands and workbench real SVG icons.


[Manifest]: ../../Topics/Structuring/Manifest
[Structuring]: ../../Topics/Structuring
[LocalInstall]: ../../Guides/Developing/Local-Install
[CodeWorkbench]: ../../Guides/Code/Workbench
[CodeCommands]: ../../Guides/Code/Commands
[CodeIcons]: ../../Guides/Code/Icons
[Translating]: ../../Guides/Code/Translations

[CC0]: https://creativecommons.org/publicdomain/zero/1.0/
[PEP420]: https://peps.python.org/pep-0420/

[Source-root]: ./Source/
[Source-pkg]: ./Source/package.xml
[Source-init]: ./Source/freecad/MinimalWorkbench/__init__.py
[Source-gui]: ./Source/freecad/MinimalWorkbench/init_gui.py
[Source-cmds]: ./Source/freecad/MinimalWorkbench/Commands.py
[Zip]: ./MinimalWorkbench.zip
