# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "New Toolbar" demo.

"""Commands contributed by the Calvinball addon.

Nothing here is specific to toolbars. These are ordinary commands, registered
in the ordinary way; Manipulator.py is what gets them onto a toolbar without a
workbench to put them in.
"""

import random

import FreeCAD
import FreeCADGui


_SCORES = [
    "Q to 12",
    "oogy to boogy",
    "Kirk to Enterprise",
    "eleventeen to the square root of π",
]

_RULES = [
    "You can't play it the same way twice!",
    "Anyone stepping in the Vortex Zone hops on one foot until the next flag change.",
    "The Bonus Box is wherever the Bonus Box says it is.",
    "Nobody may bring up the noodle incident.",
    "Questions asked while holding the ball are rhetorical.",
    "Rule 7 is now Rule 4. Rule 4 is unchanged.",
]

_MASK_LOCATIONS = [
    "under the porch",
    "in the wagon",
    "exactly where you left it, which is not where you are looking",
]


class ReviseScoreCommand:
    """Assign a new score."""

    def GetResources(self):
        return {
            "MenuText": "Revise the score",
            "ToolTip":  "Assign a new score. The previous score is not retained.",
            "Pixmap":   "Calvinball_Score.svg",
        }

    def IsActive(self):
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage(f"The score is now {random.choice(_SCORES)}.\n")


class DeclareRuleCommand:
    """Declare a new rule."""

    def GetResources(self):
        return {
            "MenuText": "Declare a rule",
            "ToolTip":  "Declare a new rule. It takes effect immediately and retroactively.",
            "Pixmap":   "Calvinball_Rule.svg",
        }

    def IsActive(self):
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage(f"New rule: {random.choice(_RULES)}\n")


class LocateMaskCommand:
    """Report the location of the mask."""

    def GetResources(self):
        return {
            "MenuText": "Locate the mask",
            "ToolTip":  "Report where the mask is. The mask is mandatory.",
            "Pixmap":   "Calvinball_Mask.svg",
        }

    def IsActive(self):
        return True

    def Activated(self):
        FreeCAD.Console.PrintMessage(f"The mask is {random.choice(_MASK_LOCATIONS)}.\n")


FreeCADGui.addCommand("Calvinball_Score", ReviseScoreCommand())
FreeCADGui.addCommand("Calvinball_Rule",  DeclareRuleCommand())
FreeCADGui.addCommand("Calvinball_Mask",  LocateMaskCommand())
