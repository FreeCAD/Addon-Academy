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
                "role": "head_linear",
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
            }
        },
        "description": "Basic Thagomizer configuration",
        "manufacturer": "Thag Simmons",
        "name": "Thagomizer",
        "toolheads": [
            {
                "id": "toolhead1",
                "name": "Spike",
                "toolhead_type": "rotary",
                "tool_change": "none",
                "max_power_kw": 500.0,
                "min_rpm": 0,
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


## Axes

Each entry in the `axes` map is keyed by axis name (`X`, `Y`, `Z`, `A`, `B`, `C`, etc.). The fields:

-   `type`: `linear` or `rotary`.
-   `role`: where the axis sits in the kinematic chain. One of `table_linear`, `table_rotary`, `head_linear`, `head_rotary`. The "table" variants move the workpiece; the "head" variants move the cutting head. The chain is what lets a multi-axis postprocessor convert a 3D toolpath into joint motions.
-   `parent`: the name of the axis that physically carries this one, or `null` if the axis is mounted directly to the machine frame.
-   `sequence`: an ordering hint used when more than one axis shares a parent.
-   `joint`: reference frame for the axis (origin and direction vector).
-   `limits`: `min` and `max` travel. For linear axes the units match `machine.units` (millimeters or inches); for rotary axes the values are in degrees.
-   `max_velocity`: maximum traverse rate, per minute, in the same units as `limits`.

FreeCAD recognizes a small set of named configurations based on which axes are present: `xyz` (3-axis), `xyza` and `xyzb` (4-axis with one rotary), `xyzac` and `xyzbc` (5-axis with two rotaries). Anything else falls under `custom`. Several CAM features (alignment strategies, multi-axis ops) are gated on these recognized configurations.


## Toolheads

The `toolheads` array can list one or more toolheads, each declared with a `toolhead_type`. The supported types and their type-specific fields:

-   **`rotary`** (default; routers, mills, drills): `min_rpm`, `max_rpm`, `max_power_kw`.
-   **`laser`**: `max_power_kw`, `laser_wavelength` (nanometers), `laser_focus_range` (a `[min, max]` pair).
-   **`waterjet`**: `max_power_kw`, `waterjet_pressure` (bar).
-   **`plasma`**: `max_power_kw`, `plasma_amperage` (amps).

Fields common to all toolhead types: `id`, `name`, `tool_change` (`"manual"` or a postprocessor-specific identifier), `coolant_flood`, `coolant_mist`, `coolant_delay` (seconds), `toolhead_wait` (seconds to wait after the toolhead is started).

The example above shows a single rotary toolhead (sort of... technically the Thagomizer doesn't rotate at all, but "just a giant spike" isn't yet an available `toolhead` option). Other types substitute the corresponding type-specific fields.


## Authoritative schema

The complete on-disk schema is defined by the `Machine` dataclass and its supporting types in [`Mod/CAM/Machine/models/machine.py`][MachineSchema] in the FreeCAD source tree. That file is the source of truth for field names, defaults, and validation rules; refer to it when an `.fcm` field is unclear or when the example here lags behind the format.


## Related

-   [Types of addon][Types]: the full list of addon types.
-   [Manifest][Manifest]: the `package.xml` schema.
-   [FreeCAD/Machines][Machines]: the canonical community-maintained machine repository.


[Types]:         ..
[Manifest]:      ../../Structuring/Manifest
[Machines]:      https://github.com/FreeCAD/Machines
[LinuxCNC]:      https://raw.githubusercontent.com/FreeCAD/Machines/refs/heads/Latest/Resources/Machines/Community/Generic/Generic_LinuxCNC.fcm
[MachineSchema]: https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/CAM/Machine/models/machine.py
