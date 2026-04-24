---
layout : Default
---

# Icons & resources

FreeCAD addons include icon and asset files alongside their code. This page covers how to organize those files and make them visible to FreeCAD at runtime.


## Use SVG

Use SVG for every icon in your addon. SVG is the only format that:

-   Scales cleanly to any display density, including HiDPI screens.
-   Covers toolbar, menu, and tree-view contexts from a single file, with no need for separate raster sizes.

Avoid bitmap formats (PNG, JPEG, WebP) for icons. They look blurry at non-native resolutions, do not adapt to themes, and need multiple files to cover the contexts SVG handles in one. WebP in particular depends on an optional Qt plugin that is not always present, so it can fail to display on some FreeCAD installations even when other bitmap formats work.


## Where icons go

We recommend placing icons under a top-level `Resources/Icons/` directory in your addon repository, for example:

```
Resources/
└── Icons/
    └── MyGreatLogo.svg
└── Screenshots/
    └── WowLookAtThisThing.png
└── Data/
    └── TableOfStuff.csv
```


## Do not ship compiled Qt resources

Qt's resource system supports bundling assets into a compiled `.rcc` file, or into a generated Python module via `pyside-rcc` / `pyside6-rcc`. **Do not use this mechanism in a FreeCAD addon.**

Compiled Qt resource files are tied to the Qt major version they were compiled against: a resource file built with Qt5 tools cannot be loaded by a Qt6 runtime, and vice versa. Because different FreeCAD builds ship with different Qt versions, and Qt major versions change over time, a compiled resource that works today will silently break for some users and may break for everyone after FreeCAD's next Qt upgrade.

Ship the plain SVG files in your addon directory and reference them at runtime. FreeCAD loads them using its current Qt runtime, so there is no version coupling.

**NOTE**: Qt Designer `.ui` files often reference icons via Qt resource paths like `:/icons/foo.svg`. Those references assume a compiled resource is loaded. If you use `.ui` files, set widget icons in Python code after loading the `.ui` rather than embedding resource-path references in the form itself.


## Registering icons at runtime

Add your addon's icon directory to FreeCAD's icon search path at startup, typically in `init_gui.py`:

```python
import os
import FreeCADGui
FreeCADGui.addIconPath(
    os.path.join(os.path.dirname(__file__), "Resources", "Icons")
)
```

Once registered, commands and other consumers can refer to icons by bare filename (e.g. `"MyCommand.svg"`), and FreeCAD resolves them against the registered paths. Absolute paths computed from `__file__` also work if you prefer explicit references.


## Common consumers

**Commands.** The `Pixmap` entry in a command's `GetResources()` dictionary takes a filename (resolved against registered icon paths) or an absolute path:

```python
def GetResources(self):
    return {
        "Pixmap":   "MyCommand.svg",
        "MenuText": "My Command",
        "ToolTip":  "Describes what the command does",
    }
```

**Addon Manager.** The `<icon>` tag in your [Manifest][Manifest] points at a path relative to `package.xml`. This icon is shown next to your addon in the Addon Manager listing. A common choice is `Resources/Icons/Logo.svg`.

**Preferences pages.** If your addon contributes a preferences page, FreeCAD looks for a file named `preferences-<modulename>.svg` (all lowercase) on the icon search path to use as that page's sidebar icon. Place it somewhere on a path you have registered with `addIconPath()`.


[Manifest]: ../../../Topics/Structuring/Manifest
