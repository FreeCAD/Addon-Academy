# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "New Toolbar" demo.

"""FreeCAD startup hook: registers the Calvinball toolbar manipulator.

This addon defines no workbench, so there is no FreeCADGui.addWorkbench call
here and no <workbench> item in package.xml. FreeCAD imports init_gui.py for
every installed addon regardless of what it contains, which is what makes a
workbench-less addon possible at all.
"""

from pathlib import Path

import FreeCADGui

from .manipulator import Manipulator

# This file is at <addon-root>/freecad/Calvinball/init_gui.py.
_ICONS_DIR = Path(__file__).parent / "resources" / "icons"

# Registers the directory the commands' Pixmap filenames are resolved against.
FreeCADGui.addIconPath(str(_ICONS_DIR))

FreeCADGui.addWorkbenchManipulator(Manipulator())
