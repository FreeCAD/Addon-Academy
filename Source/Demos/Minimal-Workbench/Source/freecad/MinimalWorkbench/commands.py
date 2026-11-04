# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Minimal Workbench" demo.

"""Commands contributed by the Minimal Workbench."""

import FreeCAD
import FreeCADGui


class HelloCommand:
    """A one-line command that prints a message to the Report view."""

    def GetResources(self):
        return {
            "MenuText": "Hello",
            "ToolTip": "Print a hello message to the Report view.",
            # "Pixmap":  "hello.svg",  # filename on the registered icon path
        }

    def IsActive(self):
        """Return True whenever the command should be enabled."""
        return True

    def Activated(self):
        """Run when the user clicks the toolbar button or menu item."""
        FreeCAD.Console.PrintMessage("Hello from the Minimal workbench!\n")


FreeCADGui.addCommand("Minimal_Hello", HelloCommand())
