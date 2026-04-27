---
permalink : /
layout : Default
title : Addon Academy
---

The **Addon Academy** is your one-stop shop for documentation about creating and maintaining a FreeCAD Addon of any variety. The **Guides** section below is a top-down list of steps you'll want to go through to author an Addon, while the **Topics** section covers several specific topics, and of course the **Demos** section contains sample code (all licensed CC0, so you are welcome to take whatever you need, no attribution is required, etc.).

## [Guides][Guides]

Step-by-step how-tos.

-   [Creating an addon][Creating]: starting from the GitHub template repository or the cookiecutter generator. Pros and cons of each.

-   [Writing addon code][Code]: the details of creating an Addon: workbenches, commands, Qt UI, preferences, custom document objects, icons, translations, and logging.

-   [Developing locally][Developing]: installing your addon into FreeCAD's `Mod/` directory, debugging, and writing tests.

-   [Publishing your addon][Publishing]: ZIP archives, repository URLs, and the official Addon Index.

-   [Polishing for users][Polish]: making things look nice: writing an overview page, manifest metadata, and selecting screenshots.

-   [Maintaining an addon][Maintaining]: cross-version compatibility, data migrations, and handing the project off to a new maintainer.


## [Topics][Topics]

Reference material on how addons fit into FreeCAD.

-   [Types of addon][Types]: workbench, macro, preference pack, bundle, and other.

-   [Structure of an Addon][Structuring]: modern namespaced layout, legacy layout, and the `package.xml` manifest.

-   [Dependencies][Dependencies]: the Addon Manager's allow-list, and when to vendor a library instead.

-   [Licensing][Licensing]: choosing licenses for code and assets, and SPDX identifiers.

-   [Addon Index][Addon Index]: the official registry, its quality requirements, and addons that have been removed from it.

-   [Glossary][Glossary]: terminology used throughout the Academy and the wider FreeCAD ecosystem.


## [Demos][Demos]

Worked examples with runnable source code.

-   [Add a command to an existing toolbar][Demo-Extend-Toolbar]: the smallest unit of addon functionality, building on what FreeCAD already ships.

-   [Minimal Workbench][Demo-Minimal-Workbench]: a complete but stripped-down workbench, suitable as a starting point for a new one.

-   [Parametric Feature][Demo-Parametric-Feature]: a custom document object with an `execute()` method and its own ViewProvider.

-   [Preferences Page][Demo-Preferences-Page]: an addon-supplied page under **Edit → Preferences** driven by a Qt Designer `.ui` file.

-   [Macro][Demo-Macro]: distributing a single-file `.FCMacro` as a standalone addon.


<!----------------------------------------------------------------------------->

[Guides]: ./Guides

[Creating]: ./Guides/Creating
[Code]: ./Guides/Code
[Developing]: ./Guides/Developing
[Publishing]: ./Guides/Publishing
[Polish]: ./Guides/Polish
[Maintaining]: ./Guides/Maintaining

<!----------------------------------------------------------------------------->

[Topics]: ./Topics

[Types]: ./Topics/Types
[Structuring]: ./Topics/Structuring
[Dependencies]: ./Topics/Dependencies
[Licensing]: ./Topics/Licensing
[Addon Index]: ./Topics/Addon-Index
[Glossary]: ./Topics/Glossary

<!----------------------------------------------------------------------------->

[Demos]: ./Demos

[Demo-Extend-Toolbar]: ./Demos/Extend-Toolbar
[Demo-Minimal-Workbench]: ./Demos/Minimal-Workbench
[Demo-Parametric-Feature]: ./Demos/Parametric-Feature
[Demo-Preferences-Page]: ./Demos/Preferences-Page
[Demo-Macro]: ./Demos/Macro
