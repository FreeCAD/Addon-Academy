---
layout : Default
---

# Package

The `<package>` tag encloses all other tags.


## General

The `<package>` tag is placed at the top-level. Only one can be specified per manifest / addon.

*» Check the [Manifest] of the [Template] for an example.*


## Syntax

Place all your other tags inside the `<package>` tag.

The values of `format` & `xmlns` are currently static.

```xml
<package
    format = '1'
    xmlns = 'https://wiki.freecad.org/Package_Metadata'
>
    ‹Other Tags›
</package>
```



[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template
