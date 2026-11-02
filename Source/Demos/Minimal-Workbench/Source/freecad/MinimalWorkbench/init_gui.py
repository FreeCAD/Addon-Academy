# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Minimal Workbench" demo.

"""FreeCAD startup hook: defines and registers the Minimal Workbench."""

from pathlib import Path

import FreeCADGui

_ICON = Path(__file__).parent / "resources" / "icons" / "Logo.svg"


class MinimalWorkbench(FreeCADGui.Workbench):
    """The smallest useful FreeCAD workbench.

    Contributes a single command ("Hello") to a toolbar and menu.
    """

    MenuText = "Minimal"
    ToolTip = "A minimal example workbench."
    Icon = str(_ICON.absolute())

    def Initialize(self):
        """Run once, the first time the user activates this workbench."""
        # Importing Commands has the side effect of calling
        # FreeCADGui.addCommand("Minimal_Hello", ...), which registers the
        # command by name so we can reference it below.
        from . import commands  # noqa: F401

        self.appendToolbar("Minimal", ["Minimal_Hello"])
        self.appendMenu("Minimal", ["Minimal_Hello"])

    def GetClassName(self):
        """Required for Python workbenches. Must return this *exact* string, DO NOT MODIFY."""
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(MinimalWorkbench())
