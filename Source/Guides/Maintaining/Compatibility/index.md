---
layout : Default
---

# FreeCAD version compatibility

Addons will (usually) outlive any single FreeCAD release. A workbench written against FreeCAD 1.0 should keep working when the user upgrades to 1.1, and the addon maintainer needs a strategy for what to do when an API change requires divergent code. This page covers the tools available: manifest version constraints, multi-branch addons, runtime version detection, and the patterns that combine them.


## Declaring version requirements in the manifest

The simplest compatibility tool is the pair of `<freecadmin>` and `<freecadmax>` tags in the [Manifest][Manifest]. They tell the Addon Manager the range of FreeCAD versions an addon supports, expressed as `MAJOR.MINOR.PATCH`:

```xml
<freecadmin>1.1.0</freecadmin>
<freecadmax>1.99.99</freecadmax>
```

The Addon Manager filters out incompatible addons before showing them to the user, so a user running FreeCAD 1.0 will not see an addon whose `<freecadmin>` is `1.1.0`. Both tags are optional; omitting them means "no lower bound" or "no upper bound" respectively.

`<freecadmax>` takes an exact version. To declare support for an entire minor release, use a generously large patch component (the canonical example is `1.0.99` to cover the entire 1.0.x series).

These constraints are checked at install time, not at runtime. They prevent installation, but they do not prevent loading: a user with a too-new FreeCAD who already has the addon installed will keep loading it, and is responsible for any breakage. For runtime checks, see below.


## Multi-branch addons

A single addon repository can support multiple FreeCAD versions through multiple git branches, each with its own `package.xml`. The Addon Manager reads every branch listed in the FreeCAD-addons `Index.json` file (which also contains `freecad_min` and `freecad_max` information) and displays only those whose requirements intersect the current running FreeCAD version.

A suggested layout:

| Branch                 | `freecad_min`  | `freecad_max`  | Purpose                              |
|------------------------|----------------|----------------|--------------------------------------|
| `main`                 | `1.2.0`        | (omitted)      | Current development for FreeCAD 1.2+ |
| `freecad-1.1-compat`   | `1.1.0`        | `1.1.99`       | Maintenance for FreeCAD 1.1 users    |
| `freecad-1.0-compat`   | `1.0.0`        | `1.0.99`       | Maintenance for FreeCAD 1.0 users    |

Each compatibility branch contains the version of your code that worked against that release. The Addon Manager handles the per-version selection automatically.

The cost is in maintenance: every bug fix or feature has to be evaluated for backporting, and any divergence between branches risks confusing users. Multi-branch is appropriate when:

-   Your addon has substantial users on an older FreeCAD version who cannot or will not upgrade.
-   The API differences are large enough that a single codebase with runtime branching becomes unwieldy.
-   The older FreeCAD version is still officially supported by the FreeCAD project.

For most addons most of the time, a single branch with `<freecadmin>` set to the oldest supported version is simpler and sufficient.


## Runtime version detection

When code paths must differ between FreeCAD versions but you want to keep them in a single branch, detect the running FreeCAD version at import time:

```python
import FreeCAD


def _freecad_version():
    """Return (major, minor, patch) of the running FreeCAD as a tuple of ints."""
    parts = FreeCAD.Version()  # returns a list of strings
    return tuple(int(p) for p in parts[:3])


FREECAD_VERSION = _freecad_version()
```

`FreeCAD.Version()` returns a list whose first three entries are the major, minor, and patch numbers as strings. The remaining entries (build hash, branch, repository URL, build date) vary by build and should not be relied on.

Once the version is captured as a comparable tuple, branching becomes straightforward:

```python
if FREECAD_VERSION >= (1, 1):
    # New API path
    do_thing_the_modern_way()
else:
    # Legacy API path
    do_thing_the_old_way()
```

Compute the version once at module load and cache it; calling `FreeCAD.Version()` repeatedly is unnecessary.


## Patterns for handling API differences

When the same operation has different APIs in different FreeCAD versions, consolidate the difference behind a small adapter rather than scattering version checks throughout your code.

**Wrapper function:**

```python
if FREECAD_VERSION >= (1, 1):
    def get_active_body(doc):
        return doc.ActiveObject  # hypothetical new API
else:
    def get_active_body(doc):
        return doc.LegacyActiveBody()  # hypothetical old API
```

The rest of the codebase calls `get_active_body(doc)` without caring about FreeCAD's version.

**Try / except probe:**

When the difference is the existence of an attribute or method rather than its signature, probing at import time is often cleaner than parsing version numbers:

```python
try:
    from FreeCAD import SomeNewThing
    HAS_SOME_NEW_THING = True
except ImportError:
    HAS_SOME_NEW_THING = False
```

This pattern is more robust than version checks because it tracks the actual capability rather than its proxy.


## Deprecation

When a FreeCAD core API your addon depends on is deprecated:

1.  **Add the new API behind a runtime version check** so your addon works on both old and new FreeCAD.
2.  **Bump `<freecadmin>` only when you drop the old code path.** Until then, keep both.
3.  **Update your addon's documentation** to reflect any user-visible changes.
4.  **Decide explicitly when to drop support** for the older FreeCAD version. Tracking the FreeCAD project's own deprecation cycle is reasonable: when FreeCAD core stops supporting a release, your addon usually can too.


## Testing across versions

Realistically, most addon maintainers do not run automated tests against every supported FreeCAD version. A practical minimum:

-   Keep at least one development install of each FreeCAD version your `<freecadmin>` / `<freecadmax>` cover, and run a manual test of the main commands before each release.
-   When a contributor reports a bug specific to one FreeCAD version, reproduce on that version before spending your time hunting it down and fixing.

For more rigorous testing, see [Testing][Testing].


## See also

-   [Manifest: `<freecadmin>`, `<freecadmax>`][ManifestVersions]: the manifest tags this page is built around.
-   [Data & schema migrations][Migrations]: the corresponding concern for `FeaturePython` document objects when their schema changes.
-   [Custom document objects][DocObjects]: the schema-evolution side of compatibility.
-   [Testing][Testing]: strategies for testing across FreeCAD versions.


[Manifest]: ../../../Topics/Structuring/Manifest
[ManifestVersions]: ../../../Topics/Structuring/Manifest#freecadmin
[Migrations]: ../Migrations
[DocObjects]: ../../Code/Document-Objects
[Testing]: ../../Developing/Testing
