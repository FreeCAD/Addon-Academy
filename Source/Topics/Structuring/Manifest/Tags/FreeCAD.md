---
layout : Default
---

# FreeCAD

The `<freecadmin>` & `<freecadmax>` tags specify 
the range of FreeCAD versions your addon supports.

<br/>

## General

The `<freecadmin>` tag is required, the `<freecadmax>`
tag is optional and used for constraining older addon.

Both have to be placed inside the `<package>` tag.

*» Check the [Manifest] of the [Template] for an example.*

<br/>

### Versions

New addons should use the latest version for the minimum. 

Reference the following list for the possible versions.

-   `1.1.0`
-   `1.0.2`
-   `1.0.1`
-   `1.0.0`
-   `0.21.2`
-   `0.21.1`
-   `0.21.0`
-   `0.20.2`
-   `0.20.1`
-   `0.20.0`
-   ...

<br/>

## Syntax

Specify the version string of the FreeCAD.

```xml
<freecadmin>‹Version›</freecadmin>
<freecadmax>‹Version›</freecadmax>
```

<br/>

## Examples

### New Addon

A new addon created using the latest version.

```xml
<freecadmin>1.1.0</freecadmin>
```

<br/>

### Old Addon

An old addon that doesn't support new versions.

```xml
<freecadmin>0.20.0</freecadmin>
<freecadmax>1.0.0</freecadmax>
```

<br/>


[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template