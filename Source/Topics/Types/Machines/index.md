---
layout : Default
---

# Machines

A Machine addon is a collection of CNC machine definitions used by FreeCAD's CAM workbench, introduced in FreeCAD 1.2 alongside the workbench's multi-axis operations and machine-based postprocessing features. Mechanically, a Machine addon ships a `<machine>` content item in `package.xml` that points at a subdirectory of `.fcm` JSON files; FreeCAD's CAM workbench discovers them at startup and offers them in the CAM Job setup.

The canonical example is the community-maintained [FreeCAD/Machines][Machines] repository.


## Anatomy of a machine

A machine definition is a single `.fcm` file: a JSON document describing one physical CNC machine. It typically contains:

-   The **machine's kinematics**: axes, their types (linear, rotary), parent-child chain, joint origins and axis vectors, travel limits, and maximum velocities.
-   **Toolheads**: spindle parameters (RPM range, max power), coolant capabilities, tool-change behavior.
-   **Output preferences**: G-code units, header content, comment style, line numbering, and numeric precision per axis.
-   **Postprocessor selection**: which postprocessor to invoke, plus per-machine overrides for preamble, postamble, supported commands, drill cycle translation, and so on.
-   **Processing options**: optional G-code transformations such as splitting arcs, translating rapid moves, or filtering inefficient motions.


## Directory layout

A Machine addon is otherwise a Modern namespaced addon. The `.fcm` files live under a subdirectory declared in `package.xml`:

```
MyMachines/
├─ package.xml
├─ README.md
├─ LICENSE
└─ Resources/
   └─ Machines/
      ├─ MyMill.fcm
      ├─ MyLathe.fcm
      └─ MyRouter.fcm
```


## The `package.xml` declaration

A Machine addon declares a `<machine>` content item with a `<subdirectory>` pointing to the directory holding its `.fcm` files. It should also declare an internal dependency on the `cam` module:

```xml
<depend type="internal">cam</depend>

<content>
    <machine>
        <subdirectory>Resources/Machines</subdirectory>
    </machine>
</content>
```

Multiple `<machine>` blocks can appear in a single addon if you want to organize machines into separate subdirectories (for example, by manufacturer).


## The `.fcm` file

A `.fcm` file is a JSON document with five top-level keys: `freecad_version`, `machine`, `output`, `postprocessor`, and `processing`, plus a top-level `version` integer for the schema itself. Stripped down, the basic structure looks like this (non-working example: to see a real, complete, machine file, see [Generic_LinuxCNC.fcm][LinuxCNC]):

```json
{
    "freecad_version": "1.2.0",
    "machine": {
        "axes": {
            "X": {
                "type": "linear",
                "role": "table_linear",
                "parent": null,
                "sequence": 0,
                "joint": {
                    "origin": [0, 0, 0],
                    "axis": [1, 0, 0]
                },
                "limits": {
                    "min": 0,
                    "max": 100
                },
                "max_velocity": 1000000
            },
            "Y": { /* etc. */ },
            "Z": { /* etc. */ }
        },
        "description": "Basic Thagomizer configuration",
        "manufacturer": "Thag Simmons",
        "name": "Thagomizer",
        "toolheads": [
            {
                "id": "toolhead1",
                "name": "Spike",
                "toolhead_type": "rotary",
                "tool_change": "manual",
                "max_power_kw": 500.0,
                "min_rpm": 6000,
                "max_rpm": 500000,
                "coolant_flood": true,
                "coolant_mist": true,
                "coolant_delay": 0.0,
                "toolhead_wait": 0.0
            }
        ],
        "units": "metric"
    },
    "output": {
        "units": "metric",
        "output_tool_length_offset": true,
        "output_header": true,
        "header": {
            "include_date": true,
            "and more!": true
        }
    },
    "postprocessor": {
        "file_name": "thagomizer",
        "properties": {
            "supports_tool_radius_compensation": true,
            "etc.": true
        }
    },
    "processing": {
        "early_tool_prep": false,
        "filter_inefficient_moves": false,
        "split_arcs": false,
        "tool_change": true,
        "translate_rapid_moves": false
    },
    "version": 1
}
```


## Related

-   [Types of addon][Types]: the full list of addon types.
-   [Manifest][Manifest]: the `package.xml` schema.
-   [FreeCAD/Machines][Machines]: the canonical community-maintained machine repository.


[Types]:    ..
[Manifest]: ../../Structuring/Manifest
[Machines]: https://github.com/FreeCAD/Machines
[LinuxCNC]: https://raw.githubusercontent.com/FreeCAD/Machines/refs/heads/Latest/Resources/Machines/Community/Generic/Generic_LinuxCNC.fcm
