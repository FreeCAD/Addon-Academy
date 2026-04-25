---
layout : Default
---

# Custom document objects

A **document object** is anything stored inside a FreeCAD document (`.FCStd` file): a Part feature, a Sketch, an annotation, a group, etc. Most document objects are implemented in C++ as part of FreeCAD core. An addon can extend the set of available object types by defining **FeaturePython** objects: document objects whose parametric behavior is written in Python.

This is more sophisticated than the basic Workbench that simply provides a new GUI to features that already fundamentally exist. In this case you develop a true Python parametric object. For example, a user adjusts a length on the property panel; your `execute()` method regenerates the geometry; FreeCAD redraws the 3D view. The logic for that generation is completely part of your addon; FreeCAD handles everything else.


## Important: your Python code is not saved in the file

`.FCStd` files do not carry embedded Python code. The file stores the *object* (its name, its property values, its type string, its serialized state) but not the *class* that defines its behavior. When a user opens the file, FreeCAD looks up the class by name and instantiates it.

There are two main consequences of this process:

-   **Anyone opening a file that contains your custom objects needs your addon installed** to get their parametric behavior back. Without the addon, FreeCAD will load a stripped-down placeholder that shows the last-computed geometry but cannot be edited.
-   **Renaming or moving your class breaks existing files.** If you ship a version where your class was `my_addon.ponies.Widget` and then in the next version move it to `my_addon.unicorns.Widget`, every file created with the old version will fail to locate the class on load. Plan for this (see Serialization below).


## The minimal pattern

A FeaturePython object is two pieces wired together:

1.  **A document object** created by FreeCAD, typed something like `Part::FeaturePython` or `App::FeaturePython`.
2.  **A Python "proxy" class** whose instance is attached to the document object via `obj.Proxy = self`. FreeCAD calls methods on the proxy at lifecycle moments (property change, recompute, load, etc.).

Here is a complete minimal parametric box (*not* the one that exists in FreeCAD, a new one we're making in our sample Addon):

```python
import FreeCAD
import Part


class ParametricBox:
    """A box defined by length, width, and height."""

    def __init__(self, obj):
        obj.Proxy = self
        obj.addProperty("App::PropertyLength", "Length", "Box", "Length of the box").Length = 10.0
        obj.addProperty("App::PropertyLength", "Width",  "Box", "Width of the box").Width  = 10.0
        obj.addProperty("App::PropertyLength", "Height", "Box", "Height of the box").Height = 10.0

    def execute(self, obj):
        obj.Shape = Part.makeBox(
            float(obj.Length),
            float(obj.Width),
            float(obj.Height),
        )


# To create one (from a command's Activated() method, for example):
doc = FreeCAD.ActiveDocument
obj = doc.addObject("Part::FeaturePython", "MyBox")
ParametricBox(obj)
obj.ViewObject.Proxy = 0   # use the default ViewProvider
doc.recompute()
```

Notes on the details:

-   **`addObject("Part::FeaturePython", ...)`** asks FreeCAD to create a document object of type `Part::FeaturePython`. The type string determines which C++ class FreeCAD uses as the backing object. `Part::FeaturePython` gives you a `Shape` property (for BRep geometry); `App::FeaturePython` is the minimal form with no geometry; there are several other variants.
-   **`obj.Proxy = self`** tells FreeCAD "when you need to call parametric-behavior methods on this object, find them on this Python instance." This is the single line that turns a  basic C++ container into a Python-parametric feature.
-   **`obj.ViewObject.Proxy = 0`** says "use FreeCAD's default ViewProvider for Part features." Setting `Proxy` to anything else (including an instance of your own class) lets you customize the visual representation; see ViewProviders below.


## Properties

Every user-editable value on a document object is a **property**, added via `addProperty`. The call signature is:

```python
obj.addProperty(type, name, group, doc)
```

| Argument | Purpose                                                                                  |
|----------|------------------------------------------------------------------------------------------|
| `type`   | The property's type, as a string. See the table below.                                   |
| `name`   | The attribute name on the document object (e.g. `"Length"`). Must be a valid identifier. |
| `group`  | The group name shown in the property panel, used for visual grouping.                    |
| `doc`    | A human-readable description shown as tooltip text.                                      |

`addProperty` returns the document object itself, so you can chain an initial-value assignment on the end:

```python
obj.addProperty("App::PropertyLength", "Length", "Box", "Length of the box").Length = 10.0
```

Commonly-used property types:

| Type                          | Purpose                                                              |
|-------------------------------|----------------------------------------------------------------------|
| `App::PropertyBool`           | Checkbox.                                                            |
| `App::PropertyInteger`        | Integer with a spinner.                                              |
| `App::PropertyFloat`          | Unitless number.                                                     |
| `App::PropertyLength`         | Length, with units. Cannot be negative.                              |
| `App::PropertyDistance`       | Length, with units. Can be negative.                                 |
| `App::PropertyAngle`          | Angle in degrees.                                                    |
| `App::PropertyString`         | Free-form text.                                                      |
| `App::PropertyEnumeration`    | Dropdown of string values; set the allowed values on the attribute.  |
| `App::PropertyColor`          | RGB color picker.                                                    |
| `App::PropertyVector`         | 3D vector.                                                           |
| `App::PropertyPlacement`      | Position and rotation (a full `App::Placement`).                     |
| `App::PropertyLink`           | Reference to another document object.                                |
| `App::PropertyLinkList`       | List of references.                                                  |

The full list is long; see FreeCAD's [Property wiki page][WikiProperty] for the complete catalog.

For properties whose description string should be translated, wrap it in `QT_TRANSLATE_NOOP` using the context `"App::Property"` (see [Translations][Translations] for why).

Consider your property's name and type carefully before releasing your Addon. If you change your mind later and want to rename it (or re-type it, etc.) you will have to deal with backwards compatibility: the property's name is stored in the FCStd file and users with old files generally expect them to load in newer versions. This poses significant challenges if you want to change things later on.


## The `execute()` method

Called whenever the document object is recomputed. This is where you regenerate whatever derived state depends on the current property values:

```python
def execute(self, obj):
    obj.Shape = Part.makeBox(
        float(obj.Length),
        float(obj.Width),
        float(obj.Height),
    )
```

FreeCAD triggers recomputes on document load, on explicit `doc.recompute()` calls, and whenever a property the object depends on has been touched. Your job in `execute` is to update the object's derived properties (typically `Shape` for a geometry feature) based on its input properties.

Keep `execute` idempotent and side-effect-free: it should produce the same output for the same inputs, and should not modify other document objects directly. FreeCAD's dependency graph assumes this.


## The `onChanged()` callback

Optional. Called whenever a property on the document object changes:

```python
def onChanged(self, obj, prop):
    """Called on every property change."""
    if prop == "Length" and obj.Length < 0:
        obj.Length = 0  # e.g. clamp to non-negative
```

Useful for input validation, for maintaining invariants between properties, and for lazy recomputation triggers. `onChanged` is called much more often than `execute`, so keep it fast.

**NOTE:** `onChanged` is also called during initial property setup in `__init__`, before properties have their final values. If your `onChanged` assumes a property exists, guard against it not being there yet:

```python
def onChanged(self, obj, prop):
    if not hasattr(obj, "Length"):
        return  # still being initialized
    # ...
```


## ViewProviders

A ViewProvider is the visual half of a FeaturePython object: it controls the icon, tree-view display, 3D-view appearance, context menu, and double-click behavior. For most parametric features you do not need to write one at all; setting `obj.ViewObject.Proxy = 0` hands the visual side to FreeCAD's default Part ViewProvider, and your `execute()` method's `Shape` assignment drives what the user sees.

Write a custom ViewProvider when you need any of:

-   A custom icon for your feature type in the tree view.
-   Custom 3D graphics (non-BRep rendering, annotations, overlays).
-   Tree-view children that are conceptually part of your feature.
-   Custom double-click behavior (opening a task panel, for example).

The minimal shape is a second proxy class attached to `obj.ViewObject`:

```python
class ParametricBoxViewProvider:
    def __init__(self, vobj):
        vobj.Proxy = self

    def attach(self, vobj):
        """Called when the ViewProvider is first wired up."""
        self.Object = vobj.Object   # the document object we're visualizing

    def getIcon(self):
        """Path to the icon file, or inline XPM string."""
        return "/absolute/path/to/icon.svg"

    def updateData(self, obj, prop):
        """Called when a property on the document object changes."""
        pass

    def onChanged(self, vobj, prop):
        """Called when a property on the ViewObject changes."""
        pass

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
```

Then when creating the object:

```python
obj = doc.addObject("Part::FeaturePython", "MyBox")
ParametricBox(obj)
ParametricBoxViewProvider(obj.ViewObject)
doc.recompute()
```

The ViewProvider has its own set of properties (on `obj.ViewObject`, added the same way as document-object properties). Visual settings (color, transparency, display mode) usually live on the ViewObject rather than the document object.


## Claiming children

If your feature conceptually contains other document objects (a pattern feature that owns the sketch it is based on, for example), implement `claimChildren` on the ViewProvider. FreeCAD's tree view will nest the claimed objects under yours:

```python
def claimChildren(self):
    return [self.Object.BaseSketch, self.Object.Profile]
```

Claiming children does not change ownership in the document; it only affects how the tree is displayed.


## Serialization and load

When the user saves a document, FreeCAD serializes each document object's properties (types, names, values) into the file. It also serializes a minimal representation of the Python Proxy: typically just the module and class name.

On load, FreeCAD:

1.  Recreates the document objects in their saved types (`Part::FeaturePython`, etc.) with their saved property values.
2.  Looks up your Proxy class by the saved module+class name.
3.  Instantiates the proxy and calls `__setstate__(state)` on it, where `state` is whatever you returned from `__getstate__`.

If any of those steps fail (e.g. the module cannot be imported because the user does not have your addon installed), FreeCAD retains the property values and last-computed `Shape` but cannot recompute the object, and the parametric behavior is effectively gone until the addon is installed and the file is reopened.

`__getstate__` and `__setstate__` let you control what transient data gets saved. For most parametric features, returning `None` from both is fine:

```python
def __getstate__(self):
    return None

def __setstate__(self, state):
    return None
```

Return something non-trivial only if your Proxy carries runtime state that is not already captured in document-object properties. The general rule is: **put data in properties, not in the Proxy.** Properties are saved and inspected by FreeCAD's native machinery; Proxy state is a side channel that is easy to get wrong.

### Planning for class renames

Because FreeCAD locates your Proxy by module+class name, renaming or moving the class breaks existing files. Mitigations:

-   **Don't rename.** Pick a class name early and stick with it.
-   **If you have to rename, keep an alias.** Leave a stub in the old module that re-exports the class so old files continue to find it.
-   **Add a `migrationVersion` property** to your objects, incremented whenever the schema changes. Check it in `__setstate__` or `onDocumentRestored` and run any necessary upgrade logic.

See [Data & schema migrations][Migrations] for more information.


## See also

-   [Parametric Feature demo][DemoParam]: a complete runnable `FeaturePython` example.
-   [Gui Commands][Commands]: how a command creates a document object from the user's action.
-   [Translations][Translations]: wrapping property descriptions for translation.
-   [Data & schema migrations][Migrations]: evolving your document-object schema across addon releases.
-   [FreeCAD wiki: Scripted objects][WikiScripted]: the upstream reference, with deeper coverage of ViewProviders and Coin3D.


[Commands]: ../Commands
[Translations]: ../Translations
[Migrations]: ../../Maintaining/Migrations

[DemoParam]: ../../../Demos/Parametric-Feature

[WikiScripted]: https://wiki.freecad.org/Scripted_objects
[WikiProperty]: https://wiki.freecad.org/Property
