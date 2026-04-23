---
layout : Default
---

# Icon

The `<icon>` tag specifies the logo of your addon.


## General

The `<icon>` tag is required and has to be placed inside the `<package>` tag.

*» Check the [Manifest] of the [Template] for an example.*


## Syntax

Specify the relative path from your repository root to your icon file.

```xml
<icon>‹Path›</icon>
```


## Example

The following example references the [Template] repository's folder structure.

```txt
<Repository>
└─ freecad
   └─ Minimal
      └─ Resources
         └─ Icons
            └─ Logo.svg
```

The resulting `<icon>` tag would be:

```xml
<icon>freecad/Minimal/Resources/Icons/Logo.svg</icon>
```



[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template
