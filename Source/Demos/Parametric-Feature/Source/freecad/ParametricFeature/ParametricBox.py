# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Parametric Feature" demo.

"""The ParametricBox FeaturePython proxy class.

FreeCAD locates this class by its module and class name when reopening
saved documents that contain a ParametricBox. Renaming the module or the
class will break those files unless backwards-compatibility shims are
provided.
"""

import Part


class ParametricBox:
    """A box whose dimensions are driven by Length, Width, and Height properties."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "Length", "Box", "Length of the box").Length = 10.0
        obj.addProperty("App::PropertyLength", "Width",  "Box", "Width of the box").Width  = 10.0
        obj.addProperty("App::PropertyLength", "Height", "Box", "Height of the box").Height = 10.0

    def execute(self, obj):
        obj.Shape = Part.makeBox(
            float(obj.Length),
            float(obj.Width),
            float(obj.Height),
        )

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
