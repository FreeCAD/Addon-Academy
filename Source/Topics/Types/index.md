---
layout : Default
---

# Types of Addon

FreeCAD supports many different types of Addon, with more types added with each subsequent version. As of the FreeCAD v1.1 release, the following types of addon are supported:

## Workbench

Adds a set of related tools centered on a particular topic (architecture, sheet metal, boat design, etc.). A Workbench generally has its own toolbars and menus when activated, and is added to the Workbenches menu in FreeCAD. This is the most complex and sophisticated Addon type.

## Macro

A short Python snippet in a single `.FCMacro` file that adds a one-off tool or automates a specific task. The Addon Manager copies it into your User Macros directory so it appears in the Macros dialog. Optionally, the Addon Manager can add a toolbar icon for one-click access to the macro. Note that there are multiple ways of distributing a Macro: as a standalone Addon is one option (the one that give the author the most control over it), but macros can also be submitted to the [FreeCAD Macros] repository. This is particularly useful for small single-file macro projects that don't need or want the extended infrastructure of a full Addon.

## Preference pack

A distributable bundle of FreeCAD user preferences that other users can apply in one click. Themes and stylesheets are distributed as a specialized kind of preference pack.

## Bundle

An addon that serves only to install other Addons (and their dependencies). No direct content on its own.

## Other

The Addon content system is open-ended: addons with the `other` type are simply unzipped into the User App Data Mod directory, but the Addon Manager takes no further action with them. This is also true of any unrecognized content item type, allowing the Addon Manager to be forwards-compatible with future types that have not been codified at the time of its creation.

[FreeCAD Macros]: https://github.com/FreeCAD/FreeCAD-Macros