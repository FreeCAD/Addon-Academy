---
layout : Default
---

# Demo : Parametric Feature

A small workbench whose single command creates a parametric box: a `Part::FeaturePython` document object whose Length, Width, and Height properties drive its geometry. Adjusting any of those properties from the property panel triggers a recompute and updates the 3D view.

This demo is the runnable companion to the [Custom document objects][DocObjects] guide. Every file is dedicated to the public domain under [CC0-1.0][CC0]; copy and adapt freely.


## Directory layout

```
ParametricFeature/
├─ package.xml
└─ freecad/
   └─ ParametricFeature/
      ├─ __init__.py
      ├─ init_gui.py
      ├─ Commands.py
      └─ ParametricBox.py
```

The top-level `ParametricFeature/` is the git repository root. See [Structuring][Structuring] for the rationale behind this layout, and the [Minimal Workbench demo][MinimalWB] for a step-by-step description of the `package.xml` and Workbench plumbing.


## The files

### `package.xml`

The [Addon Manifest][Manifest], with a `<workbench>` content item whose `<classname>` matches the `ParametricFeatureWorkbench` class registered in `init_gui.py`.

Source: [`package.xml`][Source-pkg]


### `freecad/ParametricFeature/__init__.py`

Empty namespace-package marker. See [Structuring][Structuring].

Source: [`__init__.py`][Source-init]


### `freecad/ParametricFeature/init_gui.py`

Defines `ParametricFeatureWorkbench`. The `Initialize()` method imports the `Commands` module (which registers the command as an import side effect) and adds `"ParametricFeature_CreateBox"` to a toolbar and menu.

Source: [`init_gui.py`][Source-gui]


### `freecad/ParametricFeature/Commands.py`

Defines `CreateBoxCommand`. Its `Activated()` method creates a new document object of type `Part::FeaturePython`, attaches a `ParametricBox` proxy instance to it, assigns the default ViewProvider, and recomputes. The work is wrapped in an undo transaction.

Source: [`Commands.py`][Source-cmds]


### `freecad/ParametricFeature/ParametricBox.py`

The Python proxy class. Its `__init__` adds three `App::PropertyLength` properties; its `execute` builds a `Part.makeBox` shape from the current property values and assigns it to `obj.Shape`.

This class is the one FreeCAD looks up by module and class name when reopening any saved document containing a `ParametricBox` object. Renaming or moving the class will break those files; see the discussion in [Custom document objects][DocObjects] for the implications and mitigations.

Source: [`ParametricBox.py`][Source-box]


## Trying it out

1.  Copy the addon directory into the FreeCAD user `Mod/` directory. See [Installing your addon locally][LocalInstall].
2.  Create an icon at `Resources/Icons/Logo.svg` (referenced from `package.xml`).
3.  Restart FreeCAD. "Parametric Feature" appears in the Workbench selector.
4.  Switch to that workbench. A single-button "Parametric Feature" toolbar appears.
5.  Click the button. A "ParametricBox" object is added to the tree and a 10 x 10 x 10 mm box appears in the 3D view.
6.  Select the object and adjust Length, Width, or Height in the property panel. The box geometry updates on each change.
7.  Save the document, exit FreeCAD, and reopen the document. The box reloads with its property values intact and remains parametrically editable, provided the addon is installed.


## Where to go next

-   [Custom document objects][DocObjects] for the underlying patterns: properties, `execute`, ViewProviders, serialization.
-   [Gui Commands][Commands] for more on the `Activated` / `IsActive` / `GetResources` structure.
-   [Workbench registration][Workbench] for the `init_gui.py` walk-through.
-   [Translations][Translations] for wrapping the `MenuText` and property-description strings in a production addon.


[DocObjects]: ../../Guides/Code/Document-Objects
[Commands]: ../../Guides/Code/Commands
[Workbench]: ../../Guides/Code/Workbench
[Translations]: ../../Guides/Code/Translations
[Structuring]: ../../Topics/Structuring
[Manifest]: ../../Topics/Structuring/Manifest
[LocalInstall]: ../../Guides/Developing/Local-Install
[MinimalWB]: ../Minimal-Workbench

[CC0]: https://creativecommons.org/publicdomain/zero/1.0/

[Source-pkg]:  ./Source/package.xml
[Source-init]: ./Source/freecad/ParametricFeature/__init__.py
[Source-gui]:  ./Source/freecad/ParametricFeature/init_gui.py
[Source-cmds]: ./Source/freecad/ParametricFeature/Commands.py
[Source-box]:  ./Source/freecad/ParametricFeature/ParametricBox.py
