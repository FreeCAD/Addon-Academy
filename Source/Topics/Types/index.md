---
layout : Default
---

# Types of Addon

FreeCAD supports many different types of Addon, with more types added with each subsequent version. The following sections cover each type supported by FreeCAD v1.1, plus the new Machine type forthcoming in v1.2. Where a type has substantive details of its own, this page links to a dedicated detail page. Note that on this page the "type" corresponds to the various XML tags available in the Manifest file: where appropriate, the more "conceptual" types are discussed separately (e.g. there is no "theme" XML tag, but a theme is indeed a conceptually-specific type of Preference Pack).

## Workbench

Adds a set of related tools centered on a particular topic (architecture, sheet metal, boat design, etc.). A Workbench generally has its own toolbars and menus when activated, and is added to the Workbenches menu in FreeCAD. This is the most complex and sophisticated Addon type, and one of the original addon types. In many cases older addons are labeled "workbenches" even if they do no actually implement a FreeCAD Workbench in the technical sense of a class that derives from `Workbench`.

## Macro

Conceptually, a macro is a short Python snippet in a `.FCMacro` file that adds a one-off tool or automates a specific task. Nothing in FreeCAD or the Addon Manager enforces this definition, and in reality the line between a "macro" and a "workbench" is blurry, with some macros consisting of multiple files and complex UI elements.

The Addon Manager copies and FCStd files it finds into your User Macros directory so they appear in the Macros dialog when it is launched. Optionally, the Addon Manager can automatically add a toolbar icon for one-click access to the macro. Note that there are multiple ways of distributing a Macro: as a standalone Addon is one option (the one that give the author the most control over it), but macros can also be submitted to the [FreeCAD Macros] repository. This is particularly useful for small single-file macro projects that don't need or want the extended infrastructure of a full Addon.

## Preference pack

A distributable bundle of FreeCAD user preferences that other users can apply in one click. Themes and stylesheets are distributed as a specialized kind of preference pack; see [Themes][Themes] for the full pattern.

## Bundle

An addon that serves only to install other Addons (and their dependencies). No direct content on its own.

## Machine

**Forthcoming in FreeCAD v1.2.** A definition of a physical CNC machine, used by the CAM workbench for multi-axis operations and machine-based postprocessing. A Machine addon ships one or more `.fcm` files: JSON documents describing the machine's kinematics and axis configuration, its working envelope, the recommended postprocessor, and any G-code customization options. The `<machine>` content item in `package.xml` points at a subdirectory where the `.fcm` files live, and the CAM workbench discovers them at startup. The canonical example is the community-curated [FreeCAD/Machines][FreeCAD-Machines] repository.

## Other

The Addon content system is open-ended: addons with the `other` type are simply unzipped into the User App Data Mod directory, but the Addon Manager takes no further action with them. This is also true of any unrecognized content item type, allowing the Addon Manager to be forwards-compatible with future types that have not been codified at the time of its creation.

[Themes]:           ./Themes

[FreeCAD Macros]:   https://github.com/FreeCAD/FreeCAD-Macros
[FreeCAD-Machines]: https://github.com/FreeCAD/Machines