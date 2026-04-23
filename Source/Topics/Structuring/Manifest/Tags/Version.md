---
layout : Default
---

# Version

The `<version>` tag specifies the version of your addon.


## General

The `<version>` tag is required and has to be placed inside the `<package>` tag.

It can either use [Semantic] ( `1.2.3` ) or [Calendar] ( `2026.01.20` ) versioning.

*» Check the [Manifest] of the [Template] for an example.*


## Syntax

Specify the version string inside.

```xml
<version>‹Version›</version>
```


## Examples

### Semantic

```xml
<version>0.1.0</version>
<version>0.1.1</version>
<version>0.1.2</version>
<version>0.2.0</version>
```

### Calendar

```xml
<version>2020.04.24</version>
<version>2020.04.25</version>
<version>2020.04.30</version>
<version>2020.05.02</version>
```


[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template

[Semantic]: https://semver.org
[Calendar]: https://calver.org
