---
layout : Default
---

# Installing your addon locally

Once you have an addon scaffold and some code, you need to get it into a running FreeCAD to test it. This page covers how to find the correct directory, how to install the addon there (copy or symlink), and how to iterate on it.


## Finding the user Mod directory

The simplest way to find the correct path is to ask FreeCAD. In the Python console (**View → Panels → Python console**), run:

```python
import FreeCAD, os
print(os.path.join(FreeCAD.getUserAppDataDir(), "Mod"))
```

This is the authoritative path for the running FreeCAD version. Install your addon as a subdirectory of whatever it prints.

If you need the path without a running FreeCAD, the conventions for v1.x releases are:

| OS      | Path                                                          |
|---------|---------------------------------------------------------------|
| Windows | `%APPDATA%\FreeCAD\v<MAJOR>-<MINOR>\Mod\`                     |
| Linux   | `~/.local/share/FreeCAD/v<MAJOR>-<MINOR>/Mod/`                |
| macOS   | `~/Library/Application Support/FreeCAD/v<MAJOR>-<MINOR>/Mod/` |

The version segment uses a **dash**, not a dot: FreeCAD 1.2 lives at `v1-2`, not `1.2`. (An unversioned `Mod/` sibling also exists at some of these paths for legacy reasons, but new work should use the versioned directory matching the FreeCAD build you are testing against.) This versioning scheme was added in FreeCAD 1.1.


## Installing

Your addon is a directory with a `package.xml` at its top level. To install it, put that directory inside the user `Mod/` folder. You have two options.

### Option 1: Copy

Simple, no special permissions needed, works the same everywhere.

```shell
cp -r MyAddon/ "<user-mod-dir>/"
```

The downside is that every change you make has to be copied over again, which is tedious during development.

### Option 2: Symlink (recommended for development)

A symbolic link in `Mod/` pointing back at your working tree lets you edit code in place and have FreeCAD see the changes immediately.

**Linux and macOS:**

```shell
ln -s "$(pwd)/MyAddon" "<user-mod-dir>/MyAddon"
```

**Windows** (from an elevated Command Prompt):

```cmd
mklink /D "<user-mod-dir>\MyAddon" "C:\path\to\MyAddon"
```

Or from PowerShell:

```powershell
New-Item -ItemType SymbolicLink -Path "<user-mod-dir>\MyAddon" -Target "C:\path\to\MyAddon"
```

On Windows, creating symlinks requires either an elevated shell or **Developer Mode** enabled in Windows Settings (**Settings → Privacy & security → For developers**). Without one of those, `mklink` will fail with *"You do not have sufficient privilege..."*.


## Testing the install

1.  Start (or restart) FreeCAD. FreeCAD scans `Mod/` only at startup.
2.  If your Addon is a workbench, look for it in the **Workbench selector**.
3.  If your addon has a preferences page, verify it shows up under **Edit → Preferences**.
4.  Check the **Report view** (**View → Panels → Report view**) for any startup errors.

For a concrete end-to-end test, see the [Minimal Workbench demo][MinimalWB].


## Iterating on your code

FreeCAD runs every addon's `init_gui.py` once at startup. Most changes you make after that point require a restart to take effect:

-   Changes to `init_gui.py` (Workbench class, toolbars, menus).
-   Changes to command registration.
-   Changes to `package.xml` (rarely affects the running code).

A few cases can be reloaded without a restart, but the mechanism is fragile. Restarting is almost always the faster path:

-   Small changes inside a command's `Activated()` method **might** pick up on the next invocation if the module has already been imported and you manually `importlib.reload()` it from the Python console. Most addon code holds references that survive the reload, so this often leaves you in an inconsistent state.
-   Changes to non-GUI helper modules that are only imported inside `Activated()` at call time are the easiest case.

Generally speaking, you should probably just restart FreeCAD. It can be slow, but no slower than debugging why your change isn't appearing!

## Common pitfalls

**Stale `__pycache__` files.** Python caches compiled bytecode in `__pycache__` directories next to your source files. After a large refactor (renamed classes, restructured imports), clear them out.

**Windows symlinks and Git.** If your working tree is a git clone, symlinking the clone into `Mod/` works fine. But if you switch branches, FreeCAD may end up looking at a very different addon state than you expect. When debugging, note which branch is checked out.

**Multiple FreeCAD versions.** Each FreeCAD version has its own `v<MAJOR>-<MINOR>/Mod/` directory. An addon installed in the v1.1 Mod directory is invisible to FreeCAD 1.2, and vice versa. For cross-version testing, either install into each version's Mod directory separately, or symlink once per version pointing at the same working tree.

**`package.xml` errors.** If the Addon Manager reports your addon as broken a missing required tag or a bad SPDX license identifier is the usual cause.


## Uninstalling

Remove the directory (or the symlink) from `Mod/` and restart FreeCAD.

Preferences stored under `User parameter:BaseApp/Preferences/Mod/MyAddon` are not removed by this; clear them through **Tools → Edit parameters** if you want a clean slate.


[MinimalWB]: ../../../Demos/Minimal-Workbench
