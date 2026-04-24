---
layout : Default
---

# Logging & console

FreeCAD provides its own console logging facility via `FreeCAD.Console` (also accessible as `App.Console`). These functions write to the Report view and, when FreeCAD is launched from a terminal, to stdout / stderr.


## Logging levels

FreeCAD exposes four logging levels. Each takes a string and requires an explicit trailing newline.

### `PrintMessage`

General informational output. Shown in the Report view as normal text. Use for routine "something happened" notifications that don't require user action.

```python
import FreeCAD
FreeCAD.Console.PrintMessage("Workbench initialized\n")
```

### `PrintLog`

Debug-level logging. Hidden from the Report view unless the user enables the *Log* category in the view's context menu. Use liberally during development; leave the calls in for production so users can surface them when troubleshooting.

```python
FreeCAD.Console.PrintLog(f"Recomputing with {len(sources)} inputs\n")
```

### `PrintWarning`

Warnings that do not prevent the operation from completing. Shown in the Report view in yellow. Use when something unexpected happened but the addon continued anyway.

```python
FreeCAD.Console.PrintWarning("No active document; using default\n")
```

### `PrintError`

Errors. Shown in the Report view in red. Use for conditions that prevented the requested operation from completing successfully. Note that `PrintError` only prints, it does not raise an exception or halt execution.

```python
FreeCAD.Console.PrintError(f"Failed to parse file {path}: {exc}\n")
```


## Logging is not user-facing communication

Console output is for *developers* --- you, and users who are actively troubleshooting a problem --- not for the general user. In particular:

-   **Do not use `PrintMessage` or `PrintError` to communicate important decisions or results to the user.** Many users never open the Report view, and even those who do may have it disabled or hidden during normal work. And it's noisy. FreeCAD's developers have not always been as judicious in their use of these warnings as users might prefer. If a serious error has occurred, that should be communicated via a dedicate GUI element, not buried in the incomprehensible text stream of the Report View.
-   **Logging strings are typically not translated.** Writing log output in English is the norm in FreeCAD. As a general rule the Console is not translated, whereas strings displayed in dialogs *are*.

For user-visible feedback, e.g. "Are you sure?", "File saved", "This operation requires a selected face", etc., your addon should use Qt's dialog classes. `QMessageBox` provides ready-made information / warning / critical / question dialogs, and these *should* be translated.

```python
from PySide import QtWidgets

QtWidgets.QMessageBox.warning(
    None,
    translate("MyAddon", "Selection required"),
    translate("MyAddon", "Please select a face before running this command."),
)
```

(where `translate()` is the translation helper -- see [Translations][Translations].)

For non-modal feedback, the main window's status bar is often more appropriate than a modal dialog:

```python
import FreeCADGui
FreeCADGui.getMainWindow().statusBar().showMessage(
    translate("MyAddon", "Recomputing..."), 3000  # milliseconds
)
```

[Translations]: ../Translations
