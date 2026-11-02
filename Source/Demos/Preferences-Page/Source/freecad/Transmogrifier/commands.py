# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "Preferences Page" demo.

"""Commands contributed by the Transmogrifier workbench."""

import FreeCAD
import FreeCADGui
from PySide import QtWidgets


_PREF_PATH = "User parameter:BaseApp/Preferences/Mod/Transmogrifier"

_TARGET_FORMS = ["Tiger", "Dinosaur", "Worm", "Owl", "Octopus", "Robot", "Susie Derkins"]


class EngageCommand:
    """Apply the configured transmogrification."""

    def GetResources(self):
        return {
            "MenuText": "Engage Transmogrifier",
            "ToolTip":  "Apply transmogrification using values from the preferences page.",
        }

    def IsActive(self):
        return True

    def Activated(self):
        params = FreeCAD.ParamGet(_PREF_PATH)

        target_idx = params.GetInt("DefaultTargetForm", 0)
        target = _TARGET_FORMS[target_idx] if 0 <= target_idx < len(_TARGET_FORMS) else "Unknown"
        operator = params.GetString("OperatorName", "")
        power    = params.GetInt("PowerOutput", 50)
        cooldown = params.GetFloat("CooldownDuration", 5.0)
        safety   = params.GetBool("SafetyInterlock", True)
        reverse  = params.GetBool("ReverseMode", False)

        operation = "Reverse transmogrification" if reverse else "Transmogrification"
        safety_state = "engaged" if safety else "OVERRIDDEN"

        FreeCAD.Console.PrintMessage("=== Transmogrifier engaged ===\n")
        FreeCAD.Console.PrintMessage(f"Operator:          {operator or '(unspecified)'}\n")
        FreeCAD.Console.PrintMessage(f"Operation:         {operation}\n")
        FreeCAD.Console.PrintMessage(f"Target form:       {target}\n")
        FreeCAD.Console.PrintMessage(f"Power output:      {power} W\n")
        FreeCAD.Console.PrintMessage(f"Cooldown duration: {cooldown:.1f} s\n")
        FreeCAD.Console.PrintMessage(f"Safety interlock:  {safety_state}\n")

        QtWidgets.QMessageBox.information(
            FreeCADGui.getMainWindow(),
            "Transmogrifier",
            f"{operation} to {target}.\n\n"
            f"Power: {power} W. Cooldown: {cooldown:.1f} s.\n"
            f"Safety interlock: {safety_state}."
        )


FreeCADGui.addCommand("Transmogrifier_Engage", EngageCommand())
