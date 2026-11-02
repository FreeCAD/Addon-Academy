# SPDX-License-Identifier: <License Identifier>
# SPDX-FileNotice: Part of the <Addon Name> addon.

from FreeCAD import Gui

from .command import Command
from .manipulator import Manipulator

#   Creates a command and registers it with the given name.

Gui.addCommand('Example_Command', Command())


#   Creates & registers a manipulator.

Gui.addWorkbenchManipulator(Manipulator())
