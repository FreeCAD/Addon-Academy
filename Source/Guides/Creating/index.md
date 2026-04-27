---
layout : Default
---

# Creating an Addon

There are two main ways to scaffold a new FreeCAD addon:

-   The [GitHub template repository][Addon-Template]: one click, no tooling required, produces a minimal addon of any type.
-   The [cookiecutter template][Starterkit]: driven by the Python `cookiecutter` CLI, tailored to generating a new Workbench.


## GitHub Template

The [Addon-Template] repository describes itself as an

> Addon example that's easy to make your own.

> **Important:** All files in the template repository are examples for a fictional addon. The `CONTRIBUTING.md` file is for the addon, not for the template.

### Usage

To use the template:

1.  Click the green `Use this template` button on the [Addon-Template] repository page.

2.  Click on `Create a new repository`. This opens a dialog for creating the new repository.

3.  Select the account to create the repository in and give it a simple name (typically the name of your addon).

4.  After your repository is created, customize the [License][Licensing] for your addon and any other metadata.

For a file-by-file breakdown of what the template ships with, see [Structure of an Addon][Structuring].


## Cookiecutter

The [freecad.workbench_starterkit][Starterkit] repository is a [cookiecutter] template for generating FreeCAD workbenches.

### Dependencies

-   `python3`
-   [cookiecutter]

### Quick Start

Launch cookiecutter and point it at the template repo:

```bash
$ cookiecutter https://github.com/FreeCAD/freecad.workbench_starterkit.git
```

Answer the questions:

```
  [1/13] workbench_project_name (cool_wb):
  [2/13] workbench_module_name (cool_wb):
  [3/13] workbench_class_name (CoolWorkbench):
  [4/13] workbench_menu_text (cool workbench):
  [5/13] workbench_tooltip (FreeCAD workbench to make cool parametric objects):
  [6/13] workbench_icon (cool.svg):
  [8/13] workbench_maintainer_name (me):
  [9/13] workbench_maintainer_email (me@foobar.com):
  [10/13] workbench_project_url (https://foobar.com/me/coolWB):
  [11/13] workbench_description (The cool WB creates cool parametric objects):
  [12/13] workbench_dependencies ('numpy',):
  [13/13] workbench_version (0.1.0):
```

The workbench is generated in a directory under the current directory. The easiest way to install a newly created workbench is to symlink it into the `Mod` directory of your FreeCAD installation:

```bash
cd [FreeCAD installation directory]/Mod
ln -s [path to the created workbench] CoolWB
```

Look for the workbench in the FreeCAD → View → Workbenches menu; it should be there. See the [starter kit README][Starterkit] for additional installation options, including building into FreeCAD source and submitting to the Addon Manager.


[Addon-Template]: https://github.com/FreeCAD/Addon-Template
[Starterkit]:     https://github.com/FreeCAD/freecad.workbench_starterkit
[cookiecutter]:   https://cookiecutter.readthedocs.io

[Licensing]:      ../../Topics/Licensing
[Structuring]:    ../../Topics/Structuring
