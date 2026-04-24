---
layout : Default
---

# Structuring

There are two common ways to lay out a FreeCAD addon: a **Modern**, namespaced structure used by the current addon templates, and a **Legacy** structure that keeps Python files at the top level with `Init.py` and `InitGui.py`. 

New addons should prefer the Modern layout. It is what both the [Addon-Template] and the [workbench starter kit][Starterkit] produce by default, it places the addon's code in its own namespace rather than in FreeCAD's global namespace, and it opens up the possibility of using standard Python packaging tools (such as `pip` and `uv`) for installing the addon and managing its development dependencies.


## Modern

In the Modern layout, all of the addon's Python code lives under a `freecad/<ModName>/` subdirectory — a namespace package under the shared `freecad` import namespace. The top of the repository contains only metadata, documentation, resources, and packaging files; no Python source sits at the top level.

A typical Modern addon looks like this (based on the [Addon-Template Structure reference][Template-Structure]):

```
MyAddon/
├─ freecad/
│  └─ MyAddon/
│     ├─ __init__.py
│     └─ init_gui.py
├─ Documentation/
├─ Resources/
│  ├─ Icons/
│  │  └─ Logo.svg
│  └─ Media/
├─ LICENSE-Code
├─ LICENSE-Assets
├─ README.md
├─ package.xml
└─ pyproject.toml
```

### Code

-   `freecad/MyAddon/__init__.py`: package initializer; runs when the namespace is first imported.
-   `freecad/MyAddon/init_gui.py`: registers the Workbench, toolbars, and commands with FreeCAD's GUI.

Additional Python modules for the addon's tools and commands also live inside `freecad/MyAddon/`.

### Metadata & packaging

-   `package.xml`: the [addon manifest][Manifest] read by the Addon Manager.
-   `pyproject.toml`: standard Python project metadata; consumed by `pip`, `uv`, or any PEP 517-compatible tool, typically to install development dependencies such as `freecad-stubs` and `pyside6`.
-   `CHANGELOG.md`, `README.md`, and license files (the Addon-Template splits them by what they cover, e.g. `LICENSE-Code` and `LICENSE-Assets`).

For a file-by-file breakdown of every entry the template ships with, see the Addon-Template's [Structure wiki page][Template-Structure].


## Legacy

The legacy layout predates namespaced packaging and is still supported. From the wiki's [Workbench creation][Workbench-Creation] page:

> You need a folder, with any name you like, placed in the user Mod directory, with an `Init.py` file, and, optionally an `InitGui.py` file. The `Init.py` file is executed when FreeCAD starts, and the `InitGui.py` file is executed immediately after, but only when FreeCAD starts in GUI mode. That's all it needs for FreeCAD to find your workbench at startup and add it to its interface.

The workbench's directory should look like this (at a minimum):

```
MyWorkbench/
├─ Init.py
├─ InitGui.py
└─ package.xml
```

Of course any real workbench will likely have many more files, subdirectories, resources, etc., but none of that is dictated by FreeCAD. Any additional Python files sit alongside `Init.py` and `InitGui.py` at the top level of the addon folder.

-   `Init.py`: executed even when FreeCAD is running in console mode; typically used for file importers, exporters, and other non-GUI setup.
-   `InitGui.py`: executed only when FreeCAD starts in GUI mode; registers the Workbench class with FreeCAD's UI.

The wiki describes this as "the classic way of creating a new workbench." Unless you are maintaining an existing legacy addon, prefer the Modern layout above.


## Related

-   [Addon Manifest][Manifest]: the `package.xml` file read by the Addon Manager.


[Manifest]: ./Manifest

[Addon-Template]: https://github.com/FreeCAD/Addon-Template
[Template-Structure]: https://github.com/FreeCAD/Addon-Template/wiki/Structure
[Starterkit]: https://github.com/FreeCAD/freecad.workbench_starterkit
[Workbench-Creation]: https://wiki.freecad.org/Workbench_creation
