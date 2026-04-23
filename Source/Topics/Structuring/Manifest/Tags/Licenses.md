---
layout : Default
---


# Licenses

The `<license>` tag specifies the license of part or all of the content found in your addon / project / repository.


## General

At least one `<license>` tag has to be present inside the `<package>` tag, however multiple are common in cases where for example your code & assets use different licenses.

*» Check the [Manifest] of the [Template] for an example.*


## Syntax

Specify the [SPDX License Identifier] as the content of the `<license>` tag and the path from the root to the license file in the `file` attribute.

```xml
<license
    file = '‹Path›'
>‹SPDX License Identifier›</license>
```

### Exceptions

-   If no license applies i.e. `All rights reserved.` set the  
    tag's value to `UNLICENSED` and don't specify a license file.

-   If you use a non-standard / custom license that doesn't have a SPDX license identifier, set the tag's value to `SEE LICENSE IN ‹File›`


## Example

The following example references the [Template] repository's licensing setup.

The addon has 2 licenses, a GPL license for the code and a Creative Commons one for the icons.

```txt
<Repository>
└─ LICENSE-CODE
└─ LICENSE-ICON
```

```xml
<license
    file = 'LICENSE-CODE'
>LGPL-3.0-or-later</license>

<license
    file = 'LICENSE-ICON'
>CC-BY-SA-4.0</license>
```



[SPDX License Identifier]: https://spdx.org/licenses
[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template
