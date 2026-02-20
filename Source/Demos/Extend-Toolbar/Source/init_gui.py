# SPDX-License-Identifier: <License Identifier>
# SPDX-FileNotice: Part of the <Addon Name> addon.

from .Manipulator import Manipulator
from .Command import Command

from FreeCAD import Gui


#   Creates a command and registers it with the given name.

Gui.addCommand('Example_Command',Command())


#   Creates & registers a manipulator.

Gui.addWorkbenchManipulator(Manipulator())