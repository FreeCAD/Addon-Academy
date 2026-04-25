---
layout : Default
---

# Vendoring

Vendoring means shipping a copy of a third-party Python library inside your addon's source tree, rather than declaring it as a dependency for the Addon Manager to install. This page describes when vendoring is appropriate, when it is not, and how to do it correctly when it is. TL;DR? Basically, don't.


## The default answer is "do not vendor"

FreeCAD's addon ecosystem coordinates Python dependencies through the [allow-list][AllowList]. That coordination provides basic security review, version pinning across addons, and a single point of update. Vendoring opts your addon out of all of those benefits.

The [quality requirements][Qualities] for inclusion in the Addon Index reflect this directly: an addon should "only vendor dependencies when technically necessary and not attempt to circumvent the package allow list." Vendoring a package that could be on the allow-list works against the ecosystem.

Before vendoring, consider the alternatives:

1.  **Is the package on the allow-list?** If yes, declare it as a `<depend>` in your [Manifest][Manifest]. This is the standard path and by far the most common method for including a dependency.
2.  **Could the package reasonably be added to the allow-list?** If it is well-maintained, generally useful, and available on PyPI, request its addition. See [The Python allow-list][AllowList] for the procedure.
3.  **Could you avoid the dependency?** Reimplementing a small piece of functionality in-house is sometimes simpler than carrying a third-party library through your addon's lifetime.

Only if none of the above applies should vendoring enter the discussion.


## When vendoring is acceptable

Roughly in order of strength:

-   **The package is too niche to belong on the allow-list.** A small, single-purpose utility that no other addon in the ecosystem is likely to need.
-   **You need only a small fraction of the package.** When one or two functions are all you actually use, copying just those (with attribution per the upstream license) is often cleaner than vendoring the whole package.
-   **You have forked and modified the upstream.** A modified copy is your addon's code, not a dependency, and treating it as such is appropriate.
-   **You need a specific pinned version that conflicts with the allow-list pin.** Rare, since the allow-list pins versions centrally, but possible.


## When vendoring is not acceptable

-   **The package is on the allow-list.** Declaring the dependency is correct. Vendoring duplicates the install footprint across every addon that does it, and your vendored copy will drift from the version the allow-list pins, leading to inconsistent behavior across addons in the same FreeCAD installation.
-   **The package could reasonably be added to the allow-list.** Request the addition; do not work around the process.
-   **The package has compiled extensions** (numpy, scipy, lxml, Pillow, and similar). Vendoring binary wheels across every Python version, operating system, and architecture FreeCAD ships on is a significant maintenance burden. Which is to say: basically infeasible.
-   **The license is restrictive or unclear.** Without explicit redistribution rights, vendoring may not be legal. See the licensing requirements below.
-   **The package is large or rapidly evolving.** A multi-megabyte vendored library bloats your repository, and a fast-moving upstream means you will perpetually trail behind, inheriting bugs that have already been fixed.


## License requirements

You may only vendor code whose license permits redistribution. Common permissive licenses (MIT, BSD-2-Clause, BSD-3-Clause, Apache-2.0, MPL-2.0) all allow vendoring with attribution. The LGPL family allows vendoring as long as the user can replace the LGPL component, which a vendored Python library generally satisfies.

The GPL is more restrictive: vendoring GPL-licensed code into a non-GPL addon makes the combined work GPL. If your addon is itself GPL-licensed, this is fine; otherwise it is not.

Proprietary, custom, or unclear licenses are usually unsuitable for vendoring. When in doubt, consult the upstream package's `LICENSE` file and, if necessary, the package authors. See [Licensing][Licensing] for broader license guidance.

Whatever the upstream license, you must:

-   Preserve the upstream `LICENSE` file inside your vendored copy.
-   Acknowledge the vendored package in your addon's documentation or `README`.
-   Comply with any other terms the upstream license imposes (e.g., notice files for Apache-2.0).


## Decision tree

```
Need a Python package?
│
├─ On the allow-list?
│  └─ Yes ─► declare <depend> in package.xml.
│
├─ Could reasonably be added to the allow-list?
│  └─ Yes ─► request addition.
│
└─ Neither, AND
   ├─ pure Python (no compiled extensions)
   ├─ permissively licensed
   ├─ small or used only fragmentarily
   ├─ relatively stable upstream
   └─ all yes ─► vendor with care (see below).
      any no  ─► rework your addon to avoid the dependency.
```


## How to vendor

Place the vendored code under a clearly internal subdirectory of your namespace package:

```
freecad/MyAddon/
├─ __init__.py
├─ init_gui.py
├─ ...
└─ _vendor/
   └─ somepkg/
      ├─ LICENSE       (preserved from upstream)
      ├─ README.md     (your notes on version, source URL, modifications)
      ├─ __init__.py
      └─ ...
```

The leading underscore on `_vendor` signals "internal; do not depend on this from outside the addon." This is a Python convention, not enforced by the language, but readers (and future maintainers) recognize it.

Import vendored code through your addon's namespace, not the original package name:

```python
# Good: clear that this is your vendored copy.
from freecad.MyAddon._vendor.somepkg import thing

# Bad: looks like a system-installed dependency, and may clash with one.
import somepkg
from somepkg import thing
```

Importing through your namespace prevents your vendored copy from interfering with a system-installed version of the same package, and prevents another addon's vendored or system-installed `somepkg` from interfering with yours.

Document what you vendored, where it came from, and which version. A short `_vendor/README.md` is the conventional place. At minimum, record:

-   The upstream package name and PyPI link.
-   The exact version vendored (commit SHA if vendored from a repository).
-   Any modifications made to the upstream code.
-   The reason vendoring was chosen rather than declaring a dependency.


## Maintenance

Vendored code freezes at the version you ship. Each subsequent upstream release, including security fixes, is your responsibility to track and re-vendor. Practical mitigations:

-   **Pin the upstream version explicitly** in `_vendor/README.md` so a future maintainer (or you, in a year) can compare against current upstream.
-   **Watch the upstream repository** for releases, especially security advisories.
-   **Avoid modifying the vendored code.** A clean copy is easy to update; a heavily-patched copy means every upstream update requires re-applying patches.
-   **Re-evaluate periodically** whether vendoring is still the right choice. If the package has since been added to the allow-list, switch.


## See also

-   [The Python allow-list][AllowList]: the standard path for declaring Python dependencies.
-   [Manifest: `<depend>`][ManifestDepend]: how to declare a dependency in `package.xml`.
-   [Licensing][Licensing]: license guidance, including what licenses are compatible with redistribution.
-   [Quality requirements for indexed addons][Qualities]: the rules an indexed addon must meet, including the vendoring guidance.


[AllowList]: ../Allow-List
[Manifest]: ../../Structuring/Manifest
[ManifestDepend]: ../../Structuring/Manifest#depend
[Licensing]: ../../Licensing
[Qualities]: ../../Addon-Index/Index/Qualities
