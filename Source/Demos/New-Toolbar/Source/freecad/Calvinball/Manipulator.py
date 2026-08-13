# SPDX-License-Identifier: CC0-1.0
# SPDX-FileNotice: Part of the Addon Academy "New Toolbar" demo.

"""A workbench manipulator that creates a new toolbar in an existing workbench."""

import FreeCADGui


# The internal name of the workbench to add the toolbar to. Set to None to add
# it to every workbench instead.
_TARGET_WORKBENCH = "PartWorkbench"

# Toolbar names share one global namespace with every other toolbar in FreeCAD,
# and double as the preference key recording whether the user has hidden it, so
# this carries the addon's name for the same reasons command names do.
_TOOLBAR = "Calvinball"

_COMMANDS = [
    "Calvinball_Score",
    "Calvinball_Rule",
    "Calvinball_Mask",
]


def active_workbench_name():
    """Return the internal name of the workbench currently being set up.

    FreeCADGui.activeWorkbench().name() cannot be used here. During a core
    workbench's first activation the handler object does not yet carry the
    __Workbench__ attribute that name() delegates to, and the call raises
    AttributeError. The handler object itself is already the correct one, so
    the name is recovered by identity from the workbench dictionary instead.
    """
    active = FreeCADGui.activeWorkbench()
    for name, handler in FreeCADGui.listWorkbenches().items():
        if handler is active:
            return name
    return ""


class Manipulator:
    """Adds the Calvinball toolbar to the target workbench."""

    def modifyToolBars(self):
        if _TARGET_WORKBENCH and active_workbench_name() != _TARGET_WORKBENCH:
            return []

        # Registering the commands here rather than in init_gui.py keeps their
        # import off FreeCAD's startup path for users who never visit the
        # target workbench.
        from . import Commands  # noqa: F401

        # The first dictionary creates the toolbar. Appending to the unnamed
        # root of the toolbar tree adds a new toolbar rather than a new button.
        # The rest fill it, and must come after it in the list.
        changes = [{"append": _TOOLBAR, "toolBar": ""}]
        changes += [{"append": command, "toolBar": _TOOLBAR} for command in _COMMANDS]
        return changes
