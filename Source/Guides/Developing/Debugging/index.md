---
layout : Default
---

# Debugging

When something inside an addon goes wrong, FreeCAD provides several ways to investigate, ranging from quick instrumentation through full attached-debugger sessions. This page covers the practical options in roughly increasing order of involvement.


## Quick instrumentation

For a one-off "what is this value?" question, the fastest approach is to print into the Report view through `FreeCAD.Console`:

```python
FreeCAD.Console.PrintMessage(f"selection has {len(FreeCADGui.Selection.getSelection())} objects\n")
```

See [Logging & console][Logging] for the full set of console functions and when each is appropriate. Quick instrumentation is appropriate when:

-   The question is small and self-contained.
-   You can edit, save, and reload the affected file without restarting FreeCAD.
-   You only need a few values, not a full call-stack inspection.

For anything more involved, move to one of the interactive options below.


## `breakpoint()` and `pdb`

Python's standard library provides `pdb`, an interactive command-line debugger, and a built-in `breakpoint()` that drops into it by default. In a regular Python script, calling `breakpoint()` halts execution at that line and presents a `(Pdb)` prompt for stepping, inspecting variables, and continuing.

Inside FreeCAD, the practical experience is uneven and depends on how the process was launched:

-   **Launched from a terminal on Linux or macOS:** `pdb` may attach its I/O to that terminal. The GUI freezes and debugger commands are typed into the launching shell. This is platform-dependent and has not been recently confirmed in print.
-   **Launched from a GUI shortcut on Windows:** the FreeCAD process typically has no console attached. `sys.stdin` is unusable and a `breakpoint()` call hangs.
-   **From the embedded Python console panel:** historically not a working `pdb` terminal. An [early forum thread][PdbForum] (2008) describes `pdb.set_trace()` triggering the debugger but with input arriving via a modal dialog box, and breakpoints not surviving across event dispatches. [Bug 826][PdbTracker] (closed/fixed in FreeCAD 0.14, May 2013) removed the dialog-box requirement, but the current upstream [Debugging wiki page][WikiDebugging] does not mention `breakpoint()` or `pdb.set_trace()` at all and jumps straight to remote debuggers. The wiki also documents a user-defined helper that prints a message and then triggers a divide-by-zero exception as a halt-and-inspect substitute, which is a strong hint that stock `pdb` is not currently a smooth path from the console panel.

For anything beyond a single inspection, and any time you are working on Windows or relying on the embedded Python console, attach `debugpy` (below).

If you find a current, reliable way to drive `pdb` from FreeCAD's Python console, both this page and the upstream wiki would benefit from a writeup of the steps.


## Reading the Report view

When a command fails with an unhandled exception, FreeCAD writes the traceback to the Report view (**View → Panels → Report view**). The Report view does not pop up a dialog by default; users and addon authors alike sometimes click a button, see no visible result, and miss that the traceback is sitting in a panel they have not opened.

Habits worth forming:

-   Open the Report view at startup and dock it where it remains visible during development.
-   When a command appears to do nothing, check the Report view first.
-   For FreeCAD core's own debug output, enable the **Log** category from the Report view's context menu. By default the Report view shows `PrintMessage`, `PrintWarning`, and `PrintError` but suppresses `PrintLog`.


## Attaching VS Code with `debugpy`

For step-through debugging with persistent breakpoints, variable inspection, and conditional pauses, attach Visual Studio Code to FreeCAD's Python process via the `debugpy` package.

### One-time setup

`debugpy` is the Microsoft-maintained successor to the older `ptvsd` package. Install it into the Python environment FreeCAD imports from. The most reliable approach is to run pip from inside FreeCAD's own Python console, so that the install lands wherever FreeCAD's interpreter looks:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "debugpy"])
```

If your FreeCAD's bundled Python lacks `pip`, install `debugpy` into your system Python and add that location to FreeCAD's import path with `sys.path.append`.

### Code-side setup

At the entry point of interest (a command's `Activated()`, the workbench's `Initialize()`, the start of a long-running operation), insert:

```python
import debugpy

debugpy.listen(("localhost", 5678))
print("Waiting for debugger to attach...")
debugpy.wait_for_client()
```

`listen()` opens a TCP port (`5678` is the conventional default). `wait_for_client()` blocks until VS Code attaches; FreeCAD's GUI will appear frozen during this wait, which is expected behaviour.

### VS Code launch configuration

In your project's `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach to FreeCAD",
            "type": "debugpy",
            "request": "attach",
            "connect": { "host": "localhost", "port": 5678 },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "${workspaceFolder}"
                }
            ]
        }
    ]
}
```

The `pathMappings` block tells VS Code that the file paths the debugger reports correspond to files in the workspace. When your addon is symlinked into the user `Mod/` directory rather than copied, set `remoteRoot` to the symlink target (which FreeCAD reports as `__file__`) and `localRoot` to the workspace path where you edit. Without correct mappings, breakpoints set in VS Code will be marked "unverified" and will never trigger.

### Attaching

1.  Start FreeCAD and trigger the code path that calls `debugpy.listen()` / `wait_for_client()`. FreeCAD's GUI will freeze.
2.  In VS Code, run the **Attach to FreeCAD** configuration.
3.  Set breakpoints in VS Code. Execution resumes from `wait_for_client()` and halts at any breakpoint subsequently reached.

`debugpy` connections are per-session: when you stop debugging in VS Code, the connection closes, and the next breakpoint will require a re-attach. To attach repeatedly without modifying source, guard the `listen()` / `wait_for_client()` calls behind an environment variable:

```python
import os
if os.environ.get("FREECAD_DEBUG"):
    import debugpy
    debugpy.listen(("localhost", 5678))
    debugpy.wait_for_client()
```

Start FreeCAD with `FREECAD_DEBUG=1` set when you want to debug, and start it without when you do not.


## PyCharm

PyCharm's remote-debug workflow operates on the same principle, using either `debugpy` or PyCharm's own bundled `pydevd_pycharm` package. The mechanical differences:

-   PyCharm's run-configuration type for an attached process is **Python Debug Server**, set to listen on a port matching your `debugpy.listen()` call.
-   Path mappings are configured per run-configuration in PyCharm's UI rather than in a JSON file.

The general "freeze FreeCAD with `wait_for_client()`, attach the IDE, hit breakpoints" pattern is identical.


## Legacy approaches

The FreeCAD wiki's [Debugging page][WikiDebugging] documents older tooling: `ptvsd` (the predecessor to `debugpy`, no longer maintained), `winpdb` (a standalone Python GUI debugger, also unmaintained), and LiClipse with PyDev. All three still work in principle. `debugpy` with VS Code or PyCharm covers the same use cases with current, actively-supported tooling.

For C++ crashes inside FreeCAD itself rather than Python errors in your addon, the same wiki page's `gdb` instructions remain useful. That is out of scope for addon-level debugging.


## See also

-   [Logging & console][Logging]: the cheap-instrumentation cousin to interactive debugging.
-   [Installing your addon locally][LocalInstall]: getting your code into a FreeCAD reachable for a debugger to attach.
-   [Testing][Testing]: automated alternatives that catch regressions before they need debugging.


[Logging]: ../../Code/Logging
[LocalInstall]: ../Local-Install
[Testing]: ../Testing
[WikiDebugging]: https://wiki.freecad.org/Debugging
[PdbForum]: https://forum.freecad.org/viewtopic.php?t=231
[PdbTracker]: https://tracker.freecad.org/view.php?id=826
