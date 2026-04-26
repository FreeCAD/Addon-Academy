---
layout : Default
---

# The Python allow-list

FreeCAD's Addon Manager will only install Python packages that appear on a curated allow-list. This page describes what that list is, where it lives, what format it uses, and how to get a new package added.


## What it is, and why

When your addon declares a Python package as a `<depend>` in its [Manifest][Manifest], the Addon Manager looks that package up in a list of explicitly allowed Python dependencies. Packages on the list are installed automatically when a user installs your addon. Packages not on the list are not installed automatically.

The allow-list exists for several reasons:

-   **Security.** Arbitrary `pip install` from PyPI is a common supply-chain attack vector. Gating dependencies behind a reviewed list reduces the chance of an addon silently pulling in malicious code.
-   **Version consistency.** Different addons often depend on the same library (numpy, scipy, etc.). If each addon pinned its own version, the user's FreeCAD Python environment would end up with conflicting installs. A shared, version-controlled list lets the ecosystem coordinate. No addon's package requirements conflict with another's, by construction.
-   **Quality control.** Packages that are unmaintained, abandoned, or require compiling against specific system libraries can be kept off the list entirely.


## Where the list lives

Two lists are maintained in parallel, corresponding to the two supported versions of the Addon Manager currently in the field.

### FreeCAD v1.1 and later (or Addon Manager 2026.2.19 and later)

The current list lives in the [FreeCAD/Addons][AddonsRepo] repository, split by Python version:

```
Data/Python/<python-version>/Allowed-Packages
```

For example, `Data/Python/3.11/Allowed-Packages`. A companion `constraints.txt` in the same directory pins each allowed package to a specific version, so every user gets a consistent install regardless of when they run the Addon Manager. Constraints is generated automatically from the Allowed-Packages file, and is updated automatically by a Dependabot process.

### Pre-v1.1 (legacy)

Older FreeCAD builds read `ALLOWED_PYTHON_PACKAGES.txt` from the root of the [FreeCAD/FreeCAD-addons][LegacyRepo] repository. That file is still maintained so older FreeCAD versions keep working, but new package requests should go to the new repository above.


## Format

Both files are plain text. Each non-empty, non-comment line is the PyPI package handle:

```
numpy
matplotlib
lxml
```

Version specifiers and wildcards are not supported in the allow-list itself. Version pinning happens in the companion `constraints.txt`, which the infrastructure maintains centrally so addon authors do not need to 9and indeed, *cannot*) specify versions themselves.


## What happens when a dependency is not on the list

The Addon Manager will not automatically install a Python package that is not on the allow-list. In practice this means:

-   Your addon's manifest can still declare the dependency.
-   Users who already have the package installed in FreeCAD's Python environment will see the addon work normally.
-   Users who do not have the package will see the dependency flagged as unavailable. They can install it manually through their system's Python package manager, but this is awkward and error-prone, and often not an option for users who are not comfortable at a command line.

If your addon requires a Python package that is not on the allow-list, most users will not be able to install the addon successfully. Getting the package added is usually the appropriate next step. If that fails, see [Vendoring][Vendoring] for when it might be appropriate to ship a copy of the package with your addon instead.


## Requesting a new package

Open an issue in the [FreeCAD/Addons][AddonsRepo] repository using the **Package - Addition** template. You will be asked for:

-   The package handle as it appears on [PyPI][PyPI] (e.g. `numpy`, not the display name "NumPy").
-   A short reason for the request. A normal answer is "my addon *X* needs this package to do *Y*."

Similar issue templates exist for requesting removal of a package from the list (`Package - Removal`) and for requesting that one package be replaced by another (`Package - Replace`).

There is no formal review SLA. Requests for well-known, well-maintained packages tend to move quickly; more obscure packages may need additional discussion. Ultimate responsibility for the curation of the allow-list falls to the [FreeCAD Maintainers team][Maintainers].


## See also

-   [Manifest: `<depend>`][ManifestDepend]: syntax for declaring a dependency in `package.xml`.
-   [Vendoring][Vendoring]: when to ship a copy of a package inside your addon instead of depending on it.


[Manifest]: ../../Structuring/Manifest
[ManifestDepend]: ../../Structuring/Manifest#depend
[Vendoring]: ../Vendoring

[AddonsRepo]: https://github.com/FreeCAD/Addons
[LegacyRepo]: https://github.com/FreeCAD/FreeCAD-addons
[PyPI]: https://pypi.org/
[Maintainers]: https://freecad.github.io/DevelopersHandbook/maintainersguide/