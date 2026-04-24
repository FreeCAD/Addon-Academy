---
layout : Default
---

# Licensing

Which license(s) to choose for your Addon is a complicated, and personal, decision. It depends on many factors, including whether you would like core FreeCAD to ever include content from your Addon, how much you are concerned about commercial re-use, etc. This document does not, and cannot, serve as legal advice: it is meant to provide practical guidance to Addon authors, but only from the standpoint of the practical points of Addon distribution and re-use.

## Basic recommendation

If you have no other preferences, the majority of code in the FreeCAD project is licensed `LGPL-2.1-or-later`. At its most basic, this allows anyone to re-use the licensed code as long as they license their changes to that code under the same license. Unlike the GPL, the LGPL permits proprietary code to link against LGPL-licensed libraries without being forced to adopt the LGPL itself, so it does not exert control over other code added to a project, or require that *all* other involved code be licensed under the same terms. It does *not* prohibit commercial use, as long as any changes the commercial entity makes to the LGPL-licensed code are *also* licensed under the LGPL. Using the `LGPL-2.1-or-later` license would make it easy to incorporate your code into FreeCAD's core if that was a desirable outcome at some future time.

## Non-code contributions

While the LGPL is a reasonable license for source code (its designed use-case), it is somewhat awkward for non-code resources. For many non-code resources, the Creative Commons family of licenses provides a clearer explanation of the rights and responsibilities of licensees. The most common in the FreeCAD ecosystem is `CC-BY-SA-4.0`, the "Creative Commons Attribution-ShareAlike" license. It requires attribution to the original creator *and* requires that any derivative works be licensed under the same terms. The `-SA` ("Share-Alike") clause is important: without it (i.e., using plain `CC-BY-4.0`), someone could take your assets, modify them, and re-license the derivatives under more restrictive terms, which typically defeats the intent of pairing a copyleft code license with an open asset license.

## Separate licenses for code and assets

Because code and assets are often licensed differently (e.g. LGPL code alongside CC-BY-SA assets), it's common to ship two license files in the addon repository: `LICENSE-Code` and `LICENSE-Assets`, as the [Addon-Template][AddonTemplate] does. Declare both with separate `<license>` tags in the [Manifest][Manifest], each with a `file` attribute pointing to the correct file.

## SPDX headers in source files

In addition to the addon-wide license declaration in the manifest, it's common practice in the FreeCAD ecosystem to add an SPDX identifier to the top of each source file so the license of an individual file is unambiguous when it's viewed in isolation. For example:

```python
# SPDX-License-Identifier: LGPL-2.1-or-later
```

The [Addon-Template][AddonTemplate] uses this convention for every file it ships.

## Alternative licenses

There are *many* licenses in the world, each designed to fit a particular use-case. A good place to start if the recommendations above don't fit your situation is [choosealicense.com][ChooseALicense], which walks through the common open-source licenses and their trade-offs. For an exhaustive list of standardized identifiers, see the [SPDX license list][SPDX].

## Including the license file

Most open-source licenses require that the full license text be distributed alongside the code. This applies to MIT, BSD, Apache, the GPL/LGPL family, and the Creative Commons family (CC0 is the main exception, as it waives its requirements altogether). In practice, you should almost always include a `LICENSE` file (or `LICENSE-Code` and `LICENSE-Assets` per the section above) in your repository and reference it from your [Manifest][Manifest]'s `<license>` entry via the `file` attribute.

## Common license pitfalls in the FreeCAD Addon Manager

The Addon Manager formally only recognizes official SPDX license tags. However, due to the long history of FreeCAD addons, many of which pre-date the SPDX standard, the Addon Manager attempts to "normalize" license strings that don't follow that standard. This normalization process is specifically designed to be conservative, delivering the license descriptor that is the *most restrictive* available given a particular unrecognized string. For example, `LGPL2` is normalized to `LGPL-2.0`, a non-FSF-Libre license. What the author probably intended was `LGPL-2.1-or-later`. As a general rule, Addon authors should work to ensure that their Addon's license ID is an officially-recognized SPDX identifier, or they risk inadvertently selecting a more restrictive license than they intended.


[AddonTemplate]: https://github.com/FreeCAD/Addon-Template
[Manifest]: ../Structuring/Manifest

[ChooseALicense]: https://choosealicense.com/
[SPDX]: https://spdx.org/licenses/
