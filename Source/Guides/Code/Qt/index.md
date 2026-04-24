---
layout : Default
---

# Qt & PySide

FreeCAD's GUI is built on Qt. Any visible element your addon contributes (dialog, dock, task panel, custom widget) is a Qt widget. This page covers which Qt binding to import, how to load forms designed in Qt Designer, how to integrate with FreeCAD's main window, and a few specific concerns (threading, themes).


## Which Qt binding to import

FreeCAD 1.x ships with Qt6 and the PySide6 Python binding. However, Addons should *not* import `PySide6` directly. Instead, import from FreeCAD's `PySide` compatibility shim:

```python
from PySide import QtCore, QtGui, QtWidgets
```

FreeCAD provides a top-level `PySide` module that re-exports whichever real binding is installed. Using it means your addon code keeps working across FreeCAD releases that bump the Qt major version (Qt5 to Qt6, Qt6 to some future Qt7) without your having to change every import. In cases where you want to be able to run your code *outside* FreeCAD as well, or where you want to get your IDE to provide code-completion for Qt methods, etc. you can use the Addon Manager's strategy:
```
try:
    from PySide6 import QtCore, QtWidgets # ... etc. etc.
except ImportError:
    try:
        from PySide2 import QtCore, QtWidgets
    except ImportError:
        from PySide import QtCore, QtWidgets  # If this fails, just die
```
(though note that when Qt7 is released you'll then have to add another branch, or shift from PySide 2 and 6 to 6 and 7, etc.).

For UI-form loading specifically, use `FreeCADGui.PySideUic`:

```python
form = FreeCADGui.PySideUic.loadUi("path/to/form.ui")
```

See below for the full pattern.


## Getting the FreeCAD main window

`FreeCADGui.getMainWindow()` returns the `QMainWindow` instance for the running FreeCAD. Use it as the parent for any top-level widgets you create, so that your dialog inherits FreeCAD's theme and modality behaves correctly:

```python
import FreeCADGui
from PySide import QtWidgets

mw = FreeCADGui.getMainWindow()
dialog = QtWidgets.QMessageBox(mw)
dialog.setText("Erasing all your files, please stand by…")
dialog.exec()
```

Parenting to the main window is especially important for modal dialogs: a dialog with no parent can end up behind FreeCAD's main window on some window managers, making it appear that FreeCAD has locked up.


## Loading `.ui` files from Qt Designer

The most common pattern for non-trivial dialogs is to design them in Qt Designer and ship the resulting `.ui` file alongside the Python code. Load it at runtime with `FreeCADGui.PySideUic.loadUi()`:

```python
import os
import FreeCADGui
from PySide import QtWidgets


class MyDialog:
    def __init__(self):
        ui_path = os.path.join(os.path.dirname(__file__), "my_dialog.ui")
        self.form = FreeCADGui.PySideUic.loadUi(ui_path)

        # The form's widgets are available as attributes by objectName:
        self.form.ok_button.clicked.connect(self.on_ok)
        self.form.input.setText("The clocks were striking thirteen")

    def on_ok(self):
        text = self.form.input.text()
        # ...
        self.form.close()
```

`loadUi` returns the top-level widget from the `.ui` file. Child widgets defined in Qt Designer are accessible as attributes of that top-level widget using the `objectName` you set in Qt Designer.

**Do not put `:/...` resource-path icon references into your `.ui` file.** Those assume a compiled `.rcc` resource is loaded. FreeCAD addons do not ship compiled resources (see [Icons & resources][Icons] for why). Either omit icons from the `.ui` and set them in Python code after loading, or use plain filesystem paths.


## Creating widgets programmatically

For simple dialogs, building the widget tree in Python is often less work than a `.ui` file:

```python
from PySide import QtWidgets
import FreeCADGui

mw = FreeCADGui.getMainWindow()
dlg = QtWidgets.QDialog(mw)
dlg.setWindowTitle("Settings")

layout = QtWidgets.QVBoxLayout(dlg)
layout.addWidget(QtWidgets.QLabel("Enter a value:"))

line = QtWidgets.QLineEdit()
layout.addWidget(line)

buttons = QtWidgets.QDialogButtonBox(
    QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
)
buttons.accepted.connect(dlg.accept)
buttons.rejected.connect(dlg.reject)
layout.addWidget(buttons)

if dlg.exec() == QtWidgets.QDialog.Accepted:
    value = line.text()
    # ...
```

Programmatic dialogs are easier to diff in version control and easier to translate programmatically, but harder to tweak visually. Most real addons use a mix: `.ui` files for anything with multiple inputs or a complex layout, programmatic dialogs for simple confirmations and single-input prompts.

`QMessageBox.information`, `QMessageBox.warning`, `QMessageBox.question`, and `QMessageBox.critical` cover most simple cases without needing to build anything yourself. See [Logging & console][Logging] for when to use a message box versus the Report view.


## Task panels

In many cases in FreeCAD, the **task panel** replaces modal command dialogs. It appears in the Combo View when a command is active and replaces or supplements a modal dialog. The pattern is:

```python
import FreeCADGui

class MyTaskPanel:
    def __init__(self):
        self.form = FreeCADGui.PySideUic.loadUi("my_panel.ui")

    def accept(self):
        """Called when the user clicks OK."""
        FreeCADGui.Control.closeDialog()
        return True

    def reject(self):
        """Called when the user clicks Cancel."""
        FreeCADGui.Control.closeDialog()
        return True


# To show the panel:
FreeCADGui.Control.showDialog(MyTaskPanel())
```

The `form` attribute is what FreeCAD displays in the panel area. `accept()` and `reject()` are called when the user clicks the OK / Cancel buttons that FreeCAD adds to the panel automatically.

Task panels integrate better with FreeCAD than modal dialogs for anything the user might want to tweak iteratively while observing the 3D view. Modal dialogs are fine for simple confirmations.


## Docked widgets

To add a permanent panel to FreeCAD's main window (alongside the model tree, Report view, etc.), create a `QDockWidget` and add it:

```python
from PySide import QtCore, QtWidgets
import FreeCADGui

mw = FreeCADGui.getMainWindow()
dock = QtWidgets.QDockWidget("My panel", mw)
dock.setWidget(my_content_widget)
mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
```

Dock areas: `LeftDockWidgetArea`, `RightDockWidgetArea`, `TopDockWidgetArea`, `BottomDockWidgetArea`. The user can drag and re-dock the panel wherever they like after creation.


## Threading

Qt's threading rule applies to FreeCAD addons unchanged: **all GUI access must happen on the main (GUI) thread.** If you do work in a `QThread` (or Python `threading.Thread`), and that work needs to update a widget, communicate via signals rather than calling widget methods directly:

```python
from PySide import QtCore

class Worker(QtCore.QObject):
    progress = QtCore.Signal(int)
    done = QtCore.Signal(str)

    def run(self):
        for i in range(100):
            # ... heavy work ...
            self.progress.emit(i)
        self.done.emit("finished")

# In the GUI thread:
worker = Worker()
thread = QtCore.QThread()
worker.moveToThread(thread)
worker.progress.connect(progress_bar.setValue)  # safe: queued across threads
worker.done.connect(on_done)
thread.started.connect(worker.run)
thread.start()
```

Qt queues signals emitted from non-GUI threads onto the GUI thread automatically, so `progress_bar.setValue` runs on the main thread even though `progress.emit` was called from the worker thread.

`FreeCAD.Console.PrintMessage` is also safe to call from worker threads.


## HiDPI and themes

FreeCAD 1.x with Qt6 is HiDPI-aware by default. As an addon author you mostly do not need to think about this, provided you:

-   Use SVG for icons (see [Icons & resources][Icons]). Bitmaps at a fixed pixel size will look blurry on HiDPI screens.
-   Let Qt lay out your widgets rather than hard-coding pixel widths. `QLayout` subclasses scale correctly with DPI and user font-size settings; fixed `setFixedWidth(200)` calls do not.

Dark-mode and custom stylesheets are applied globally by FreeCAD at startup. Your widgets inherit whatever theme the user has selected, as long as you do not override colors explicitly. Avoid hardcoding colors (`widget.setStyleSheet("color: black")`) unless you really mean it; let Qt's palette system handle appearance.


## See also

-   [Preferences pages][Preferences]: the specific pattern for addon settings, which uses `Gui::Pref*` widgets in a `.ui` file.
-   [Icons & resources][Icons]: why addons should not ship compiled Qt resources.
-   [Logging & console][Logging]: when to use `QMessageBox` versus the Report view.
-   [Translations][Translations]: wrapping user-visible strings in `QMessageBox`, form labels, and button text.


[Preferences]: ../Preferences
[Icons]: ../Icons
[Logging]: ../Logging
[Translations]: ../Translations
