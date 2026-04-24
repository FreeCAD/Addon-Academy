---
layout : Default
---

# Glossary

## FreeCAD core

**Addon**: Any component that extends FreeCAD beyond the base installation: a workbench, macro, preference pack, or similar. The list of items that may be addons expands with each FreeCAD release.

**Body**: A Part Design container holding a sequence of parametric features that build up a single part.

**Bundle**: An addon whose only purpose is to install a group of other addons (as dependencies).

**Document**: A `.FCStd` file, represented at runtime as an `App.Document`. Contains all objects (features, geometry, metadata) a user is working on.

**Document Object**: Any element stored inside a document: geometry, groups, sketches, annotations, FeaturePython objects, etc.

**Expression**: A value in a property computed from other properties at recompute time (e.g. `Box.Length * 2`). Managed by FreeCAD's expression engine.

**FeaturePython**: A Python-implemented document object. The typical way an addon adds a parametric feature. Defined by a class implementing `execute()` and optionally `onChanged()`.

**Group**: A container that holds a collection of DocumentObjects, primarily for tree organization.

**Gui Command**: A user-invokable action, usually bound to a toolbar button or menu item. Registered with `FreeCADGui.addCommand()` and referenced by name elsewhere.

**Link**: An `App::Link` object that references another DocumentObject (in the same or a different document) without copying its geometry. The basis of assembly re-use.

**Macro**: Formally any `.FCMacro` file. Usually a small, simgle-file Addon that adds a one-off tool or automation. The line between Macro and Workbench is blurry.

**Mesh**: A polygonal surface representation (`Mesh::Feature`), as distinct from a BRep Shape.

**Mod**: Short for "module." Refers both to an installed addon and to the `Mod/` directory where addons live. Sometimes used as a shorthand for "Addon".

**Mod directory**: The filesystem location FreeCAD scans for installed addons. On Windows typically `%APPDATA%\FreeCAD\Mod\`; on Linux `~/.local/share/FreeCAD/Mod/`; on macOS `~/Library/Application Support/FreeCAD/Mod/`. Programmatically: `FreeCAD.getUserAppDataDir() + "Mod"`.

**Placement**: A combined translation + rotation applied to an object. Expressed as an `App.Placement`.

**Preference pack**: A distributable set of FreeCAD preferences that users can apply in one click. Themes and stylesheets ship as a specialized preference pack.

**Python console**: FreeCAD's interactive Python REPL, available via **View → Panels → Python console**.

**Recompute**: FreeCAD's process of re-executing `execute()` on every DocumentObject whose inputs have changed (i.e. are marked *Touched*).

**Report view**: FreeCAD's log panel. Receives output from `FreeCAD.Console.Message/Log/Warning/Error`.

**Shape**: A geometric object from the OCCT kernel (a `TopoDS_Shape`). Edges, faces, solids, and compounds are all shapes.

**Sketch**: A 2D parametric drawing (from the Sketcher workbench) typically used to drive 3D features.

**Theme**: A stylesheet + icon set that changes FreeCAD's appearance. Distributed as a preference pack with a `<type>Theme</type>` tag, which has special meaning within FreeCAD's preferences system.

**Topological naming**: The problem (and proposed solutions) of stably identifying a topological element like an edge or face across feature edits. An ongoing engineering topic in FreeCAD. The Topoligical Naming Problem ("TNP") is an often-referenced challenge in parametric CAD.

**Touched**: A flag set on a DocumentObject when one of its inputs has changed, scheduling it for the next recompute.

**Transaction**: A group of document changes that can be undone and redone as a unit. Bracketed by `Document.openTransaction()` / `commitTransaction()`.

**User App Data directory**: FreeCAD's per-user data root, where preferences, recent-documents state, and the `Mod/` directory live. Accessible via `App.getUserAppDataDir()`.

**ViewProvider**: The visual representation of a DocumentObject in the 3D view and tree. Paired with a FeaturePython object to define how it's drawn, iconified, and interacted with.

**Workbench**: Formally, a Python class that derives from FreeCAD's Workbench class. Informally, a collection of related tools (usually a toolbar + menu) focused on a particular task or domain. Activated via FreeCAD's Workbench selector. See [Types of Addon][Types].


## FreeCAD internals

**App / Gui / Base**: The three core modules of FreeCAD's C++ code. `App` is headless document logic; `Gui` is the user interface layer; `Base` is shared low-level infrastructure (exceptions, matrices, vectors).

**BRep (boundary representation)**: The geometric representation OCCT uses: solids defined by their enclosing faces, edges, and vertices. Distinct from mesh or voxel representations.

**Coin3D / Pivy**: The 3D scene graph library FreeCAD uses to render the view. Pivy is its Python binding; ViewProviders that customize rendering build Coin3D scene-graph nodes.

**OCCT (OpenCascade)**: The open-source CAD kernel FreeCAD uses for BRep geometry, boolean operations, and most 3D operations.


## Addon packaging

**Addon Index**: The registry of addons at [github.com/FreeCAD/Addons][AddonIndex], shown by the Addon Manager.

**Addon Manager**: FreeCAD's built-in tool for discovering, installing, updating, and removing addons. Found under **Tools → Addon Manager**.

**Allow-list**: The list of Python packages the Addon Manager will install automatically as addon dependencies. Python deps not on the list require manual user installation, and risk conflict with other addons and their dependencies.

**CalVer**: Calendar-based versioning (e.g. `2026.04.23`). One of the two version schemes the manifest accepts.

**Content item**: A `<workbench>`, `<macro>`, `<preferencepack>`, `<bundle>`, or `<other>` element inside a manifest's `<content>` block, declaring one discrete piece of functionality the addon ships.

**Cookiecutter**: A Python-based template generator used by the [workbench starter kit][Starterkit]. See [Creating][Creating].

**GitHub Template**: GitHub's built-in feature for turning a repository into a one-click template for new repos. The [Addon-Template][AddonTemplate] uses this mechanism.

**Legacy addon**: The older addon layout with `Init.py` / `InitGui.py` at the top level of the addon folder. Deprecated, but still supported.

**Manifest (package.xml)**: The XML metadata file at the root of an addon describing its contents, dependencies, license, and presentation metadata. See [Addon Manifest][Manifest].

**Namespaced addon**: The modern addon layout where Python code lives under `freecad/<ModName>/` rather than at the top level. Allows installation via `pip` and avoids polluting FreeCAD's global namespace. See [Structuring][Structuring]. Recommended for new Addons.

**Orphaned addon**: An addon with no active maintainer, marked in the manifest with `<maintainer email="no-one@freecad.org">No current maintainer</maintainer>`.

**SemVer**: [Semantic versioning 2.0][SemVer] (e.g. `1.0.2-beta`). The other accepted version scheme.

**SPDX identifier**: The short license name from the [SPDX license list][SPDX] (e.g. `LGPL-2.1-or-later`, `MIT`). Used in the manifest's `<license>` tag.

**Vendoring**: Shipping a copy of a third-party library inside your addon rather than declaring it as a dependency. See [Vendoring][Vendoring].


## Qt & Python tooling

**pip**: Python's default package installer.

**PyPI**: The [Python Package Index][PyPI]. The default source for `pip install`.

**pyproject.toml**: The standard Python project metadata file ([PEP 517][PEP517] / [PEP 621][PEP621]).

**PySide / PySide6**: Official Python bindings for Qt. Addon GUI code should import from these (via FreeCAD's wrappers) rather than from PyQt. FreeCAD provides wrappers that insulate Addon developers from needing to update their addon to accomodate new major versions of Qt by using `import PySide` rather than, e.g. `import PySide6`.

**Qt**: The cross-platform application framework FreeCAD's GUI is built on.

**Qt Designer**: Qt's WYSIWYG form designer. Produces `.ui` files that addon code can load at runtime, or that can be converted directly into Python code for inclusion in an Addon.

**Qt Linguist**: Qt's translation tool. Edits `.ts` files (XML translation source) and compiles them to `.qm` (binary, loaded at runtime).

**Qt Resource System (.qrc)**: A mechanism for embedding icons and other assets into compiled Python modules. Compiled with `pyside-rcc` / `pyside6-rcc`. Generally not usable by Addons.

**requirements.txt**: A plain-text list of Python dependencies, consumable by `pip install -r`.

**.ui file**: An XML form description produced by Qt Designer.

**uv**: A modern, fast Python package installer and resolver. Reads `pyproject.toml`.


## Community & workflow

**Author**: A contributor credited in the manifest's `<author>` tag. Authors may or may not be current maintainers.

**Crowdin**: The translation platform FreeCAD and many of its addons use to coordinate community translation work.

**Issue tracker**: The bug/feature list attached to a git hosting repository (GitHub, GitLab, Codeberg). Referenced in the manifest via `<url type="bugtracker">`.

**Maintainer**: The person (or people) responsible for an addon's upkeep: reviewing issues, creating releases, and responding to security reports.

**Pre-commit**: The `pre-commit` git hook framework, which runs formatters and linters before each commit. Common in FreeCAD addon repositories.

**Pull Request (PR)**: A proposed change to a git repository, submitted for review and merge.


[Types]: ../Types
[Structuring]: ../Structuring
[Manifest]: ../Structuring/Manifest
[Vendoring]: ../Dependencies/Vendoring
[Creating]: ../../Guides/Creating

[AddonIndex]: https://github.com/FreeCAD/Addons
[AddonTemplate]: https://github.com/FreeCAD/Addon-Template
[Starterkit]: https://github.com/FreeCAD/freecad.workbench_starterkit
[SPDX]: https://spdx.org/licenses/
[SemVer]: https://semver.org
[PyPI]: https://pypi.org
[PEP517]: https://peps.python.org/pep-0517/
[PEP621]: https://peps.python.org/pep-0621/
