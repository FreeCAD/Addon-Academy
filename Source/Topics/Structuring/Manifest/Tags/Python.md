---
layout : Default
---

# Python

The `<pythonmin>` tag specifies the minimum
version of the Python runtime your addon requires.

<br/>

## General

The `<pythonmin>` tag is required and has  
to be placed inside the `<package>` tag.

*» Check the [Manifest] of the [Template] for an example.*

<br/>

### Versions

Reference the following table for which versions
of Python is available in what versions of FreeCAD.

| FreeCAD | Python |
|:-------:|:------:|
| `1.1.0` | `3.11` |
| `1.0.2` | `3.10` |
| `1.0.1` | `3.10` |
| `1.0.0` | `3.10` |

<br/>

## Syntax

Specify the version string of the Python runtime.

```xml
<pythonmin>‹Version›</pythonmin>
```

<br/>

## Example

```xml
<pythonmin>3.11</pythonmin>
```

<br/>


[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template