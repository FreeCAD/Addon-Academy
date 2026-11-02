# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Parametric Feature" demo.

"""FreeCAD startup hook: defines and registers the Parametric Feature workbench."""

from pathlib import Path

import FreeCADGui

# This file is at <addon-root>/freecad/ParametricFeature/init_gui.py.
_ICON = Path(__file__).parent / "resources" / "icons" / "Logo.svg"


class ParametricFeatureWorkbench(FreeCADGui.Workbench):
    """A workbench that creates parametric box document objects."""

    MenuText = "Parametric Feature"
    ToolTip = "Demonstrates the FeaturePython pattern with a parametric box."
    Icon = str(_ICON)

    def Initialize(self):
        """Run once, the first time the user activates this workbench."""
        # Importing Commands has the side effect of registering the command
        # via FreeCADGui.addCommand, so it is available by name below.
        from . import commands  # noqa: F401

        self.appendToolbar("Parametric Feature", ["ParametricFeature_CreateBox"])
        self.appendMenu("Parametric Feature",    ["ParametricFeature_CreateBox"])

    def GetClassName(self):
        """Required for Python workbenches. Must return this exact string."""
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(ParametricFeatureWorkbench())
