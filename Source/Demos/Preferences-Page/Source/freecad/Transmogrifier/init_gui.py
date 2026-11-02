# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Preferences Page" demo.

"""FreeCAD startup hook: registers the Transmogrifier workbench and its preferences page."""

from pathlib import Path

import FreeCADGui

# This file is at <addon-root>/freecad/Transmogrifier/init_gui.py.
_RESOURCES_ROOT = Path(__file__).parent
_ICONS_DIR  = _RESOURCES_ROOT / "resources" / "icons"
_PREFS_UI   = _RESOURCES_ROOT / "resources" / "panels" / "TransmogrifierPrefs.ui"


class TransmogrifierWorkbench(FreeCADGui.Workbench):
    """A workbench that demonstrates the preferences-page pattern."""

    MenuText = "Transmogrifier"
    ToolTip = "Apply transmogrification with configurable parameters."
    Icon = str(_ICONS_DIR / "Logo.svg")

    def Initialize(self):
        """Run once, the first time the user activates this workbench."""
        from . import commands  # noqa: F401

        self.appendToolbar("Transmogrifier", ["Transmogrifier_Engage"])
        self.appendMenu("Transmogrifier",    ["Transmogrifier_Engage"])

    def GetClassName(self):
        """Required for Python workbenches. Must return this exact string."""
        return "Gui::PythonWorkbench"


# Register the icons path so FreeCAD can locate preferences-transmogrifier.svg
# for the preferences-dialog sidebar.
FreeCADGui.addIconPath(str(_ICONS_DIR))

FreeCADGui.addWorkbench(TransmogrifierWorkbench())

FreeCADGui.addPreferencePage(str(_PREFS_UI), "Transmogrifier")
