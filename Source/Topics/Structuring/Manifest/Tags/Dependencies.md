---
layout : Default
---

# Dependencies

The `<depend>` , `<replace>` & `<conflict>` tags declare the dependencies of your addon.


## General

For every relationship to a dependency one tag should be added to the `<package>` tag.

-   The `<depend>` tag declares a dependency your addon requires.

-   The `<conflict>` tag declares that a dependency conflicts with your addon.

-   The `<replace>` tag declares that your addon replaces a dependency.

*» Check the [Manifest] of the [Template] for an example.*


### Bundles

Bundle addons — which use the `<bundle>` content item — list a multitude of dependencies that will be installed when the addon is installed.


## Syntax

Set the tag value to the name of the dependency and specify the type and version range you need.

```xml
<depend
    version_lte = '‹Version›'
    version_gte = '‹Version›'
    version_lt = '‹Version›'
    version_gt = '‹Version›'
    version_eq = '‹Version›'
    optional = 'true'
    type = '‹Type›'
>‹Id›</depend>

<conflict
    ...
>‹Id›</conflict>

<replace
    ...
>‹Id›</replace>
```


### Version

Use one or a combination of the `version` attributes to specify the what ranges of versions you require.


### Optional

Add this attribute if your dependency is not strictly necessary for the base functionality.

The user will be prompted on install whether they want to download these extra dependencies.

Ensure your addon checks that the optional dependencies are available before using them.


### Type

Specify the `type` of the dependency, this can be one of the following types:

- `internal` : An internal mod like [PartDesign].

- `python` : A package found on the [PyPI] registry.

- `addon` : Another addon listed on our [Index].


### Internal

The following `internal` mod types are available:

`assembly` , `bim` , `cam` , `draft` , `fem` , `import` ,  `material` , `mesh`  
`openscad` , `part` , `partdesign` , `plot` , `points` , `web` , `sketcher`  
`reverseengineering` , `spreadsheet` , `techdraw` , `tux` , `robot`


## Examples


### Internal

Dependency on the internal [PartDesign] mod.

```xml
<depend
    type = 'internal'
>partdesign</depend>
```


### Python

Dependency on the [Numpy] python package.

```xml
<depend
    version_gte = '2.4.2'
    type = 'python'
>numpy</depend>
```


### Addon

Optional dependency on the [Curves] addon.

```xml
<depend
    version_gte = '0.6.70'
    optional = 'true'
    type = 'addon'
>Curves</depend>
```


[PartDesign]: https://github.com/FreeCAD/FreeCAD/tree/main/src/Mod/PartDesign
[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template

[Curves]: https://github.com/tomate44/CurvesWB
[Index]: https://github.com/FreeCAD/Addons
[Numpy]: https://pypi.org/project/numpy
[PyPI]: https://pypi.org
