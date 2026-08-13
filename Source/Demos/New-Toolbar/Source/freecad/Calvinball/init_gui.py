# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "New Toolbar" demo.

"""FreeCAD startup hook: registers the Calvinball toolbar manipulator.

This addon defines no workbench, so there is no FreeCADGui.addWorkbench call
here and no <workbench> item in package.xml. FreeCAD imports init_gui.py for
every installed addon regardless of what it contains, which is what makes a
workbench-less addon possible at all.
"""

import os

import FreeCADGui

from .Manipulator import Manipulator

# This file is at <addon-root>/freecad/Calvinball/init_gui.py.
_ADDON_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ICONS_DIR  = os.path.join(_ADDON_ROOT, "Resources", "Icons")

# Registers the directory the commands' Pixmap filenames are resolved against.
FreeCADGui.addIconPath(_ICONS_DIR)

FreeCADGui.addWorkbenchManipulator(Manipulator())
