# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Parametric Feature" demo.

"""Commands contributed by the Parametric Feature workbench."""

import FreeCAD
import FreeCADGui

from .ParametricBox import ParametricBox


class CreateBoxCommand:
    """Create a new parametric box in the active document."""

    def GetResources(self):
        return {
            "MenuText": "Create Parametric Box",
            "ToolTip":  "Add a new parametric box to the active document.",
            # "Pixmap": "ParametricFeature_CreateBox.svg",
        }

    def IsActive(self):
        return True

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        if doc is None:
            doc = FreeCAD.newDocument()
        doc.openTransaction("Create Parametric Box")
        try:
            obj = doc.addObject("Part::FeaturePython", "ParametricBox")
            ParametricBox(obj)
            obj.ViewObject.Proxy = 0
            doc.commitTransaction()
        except Exception:
            doc.abortTransaction()
            raise
        doc.recompute()


FreeCADGui.addCommand("ParametricFeature_CreateBox", CreateBoxCommand())
