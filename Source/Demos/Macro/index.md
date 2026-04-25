---
layout : Default
---

# Demo : Macro

A single-file FreeCAD macro distributed as an addon. The macro itself runs top to bottom when invoked, prints to the Report view, and presents a `QMessageBox` summarizing the daily tally for Vexorg, dread overlord of the Yard.

Every file in this demo is dedicated to the public domain under [CC0-1.0][CC0]. Copy and adapt freely. Due credit to Gary Larson.


## Directory layout

```
Vexorg/
├─ package.xml
└─ Vexorg.FCMacro
```

A macro addon is the smallest kind of FreeCAD addon: a single `.FCMacro` file plus a manifest that tells the Addon Manager about it. There is no namespace package, no `init_gui.py`, and no Workbench. On installation the Addon Manager copies the macro file into the user's Macros directory; from there it appears in the **Macro** dialog and can be assigned a toolbar button, etc.


## The files

### `package.xml`

The [Addon Manifest][Manifest], with a `<macro>` content item rather than a `<workbench>`. The `<file>` element names the macro file relative to `<subdirectory>`:

```xml
<macro>
    <name>Vexorg</name>
    <subdirectory>./</subdirectory>
    <file>Vexorg.FCMacro</file>
</macro>
```

Source: [`package.xml`][Source-pkg]


### `Vexorg.FCMacro`

The macro itself. A `.FCMacro` file is an ordinary Python file with the `.FCMacro` extension; FreeCAD treats it as a script that runs from top to bottom each time the user invokes it.

The file conventionally begins with a block of `__title__` / `__author__` / `__version__` / `__date__` / `__license__` module-level constants, which FreeCAD's macro browser displays alongside the macro name.

Source: [`Vexorg.FCMacro`][Source-macro]


## Trying it out

1.  The Addon Manager does most of the work when installing a macro. To simulate its work, simply copy the macro into your user macro directory. You can als copy the addon directory into the FreeCAD user `Mod/` directory, but it won't do anything special.
2.  Restart FreeCAD.
3.  Open **Macro → Macros…**. The Vexorg macro appears in the list.
4.  Select it and click **Execute**.
5.  Vexorg's daily report is written to the Report view and shown in a dialog.


## When to use a macro versus a workbench

Macros are appropriate for:

-   One-off scripts that do not need persistent UI presence.
-   Small utilities the user invokes occasionally from the Macros dialog.
-   Quick experiments before promoting to a full workbench.

A [Workbench][Workbench] is appropriate when the addon needs toolbars, menus, multiple commands, persistent state, or custom document objects. The boundary is not strict, and many addons start as macros and grow into workbenches.


## Where to go next

-   [Types of Addon][Types] for the full set of distribution shapes.
-   [Workbench registration][Workbench] for the next step up in complexity.
-   [Manifest][Manifest] for the `<macro>` content item and other manifest tags.


[CC0]: https://creativecommons.org/publicdomain/zero/1.0/

[Types]: ../../Topics/Types
[Workbench]: ../../Guides/Code/Workbench
[Manifest]: ../../Topics/Structuring/Manifest
[LocalInstall]: ../../Guides/Developing/Local-Install

[Source-pkg]:   ./Source/package.xml
[Source-macro]: ./Source/Vexorg.FCMacro
