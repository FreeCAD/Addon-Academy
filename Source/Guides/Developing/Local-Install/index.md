---
layout : Default
---

# Installing your addon locally

*Work in progress.*

**Planned scope:**

-   Finding the user `Mod/` directory on Linux, macOS, and Windows.
-   Symlinking your addon into `Mod/` (`ln -s`, `mklink /D`).
-   Using `App.getUserAppDataDir()` to locate the data directory at runtime.
-   Reloading code without restarting FreeCAD.
-   Common pitfalls (namespace caching, stale `.pyc` files).
