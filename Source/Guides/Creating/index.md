---
layout : Default
---

# Creating an Addon

There are two main ways to scaffold a new FreeCAD addon:

-   The [GitHub template repository][Addon-Template]: one click, no tooling required, produces a minimal addon of any type.
-   The [cookiecutter template][Addon-Template-Cookie]: driven by the Python `cookiecutter` CLI, tailored to generating a new Workbench.


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

An alternative to the GitHub template, particularly for those interested in creating a full workbench (as opposed to a simpler addon like a theme, macro, or CAM machine), is to use the [cookiecutter]-based mechanism in the [`cookie` branch of the template][Addon-Template-Cookie]. 

To use it, first install [uv] (if you haven't already):
```bash
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Once `uv` is installed, use it to run `cookiecutter` with our tooling:
```bash
$ uvx cookiecutter https://github.com/FreeCAD/Addon-Template.git --checkout cookie
```

Answer the questions as they are presented:

```
  [1/13] Addon name (MyAddon):
  [2/13] Project directory (MyAddon):
  [3/13] Python sub-module name (MyAddon):
  [4/13] Name of the svg icon file (addon.svg):
  [5/13] Name of the author/maintainer (me):
  [6/13] Email of the author/maintainer (me@foobar.com):
  [7/13] Short description of the addon (MyAddon does something cool.):
  [8/13] Required pypi dependencies (optional, separated by comma. i.e. numpy,pillow) ():
  [9/13] Initial version using format major.minor.review (0.1.0):
  [10/13] Select addon_license
    1 - LGPL-2.1-or-later
    2 - LGPL-3.0-or-later
    3 - GPL-3.0-or-later
    4 - MIT
    5 - CC0
    6 - CC-BY-SA-4.0
    7 - OTHER
    Choose from [1/2/3/4/5/6/7] (1):
  [11/13] Select assets_license
    1 - CC-BY-SA-4.0
    2 - CC0
    3 - LGPL-2.1-or-later
    4 - LGPL-3.0-or-later
    5 - GPL-3.0-or-later
    6 - MIT
    7 - OTHER
    Choose from [1/2/3/4/5/6/7] (1):
  [12/13] Full url of the git repository (https://github.com/me/MyAddon):
  [13/13] Name of the default git branch (main):
```

The workbench is generated in a directory under the current directory. The easiest way to install a newly created workbench is to symlink it into the `Mod` directory of your FreeCAD installation:

```bash
cd [FreeCAD installation directory]/Mod
ln -s [path to the created workbench] CoolWB
```

Look for the workbench in the FreeCAD → View → Workbenches menu; it should be there.


[Addon-Template]: https://github.com/FreeCAD/Addon-Template/tree/main
[Addon-Template-Cookie]: https://github.com/FreeCAD/Addon-Template/tree/cookie
[uv]: https://github.com/astral-sh/uv
[cookiecutter]: https://cookiecutter.readthedocs.io

[Licensing]:      ../../Topics/Licensing
[Structuring]:    ../../Topics/Structuring
