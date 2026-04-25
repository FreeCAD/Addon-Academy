---
layout : Default
---

# Data & schema migrations

When your addon defines `FeaturePython` document objects, your code's class names and property schemas become part of any document a user saves with those objects in it. Subsequent changes to your addon ripple back into the user's saved files: a renamed property, a removed class, a changed property type can all break documents that worked under the previous version.

This page covers how to evolve a `FeaturePython` schema across addon releases without breaking older documents. Read [Custom document objects][DocObjects] first; this page assumes the patterns introduced there.


## What gets included in a saved document

When a user saves a `.FCStd` containing one of your custom objects, FreeCAD stores:

-   The object's **type** (e.g., `Part::FeaturePython`).
-   The **module and class name** of your Python proxy (e.g., `freecad.MyAddon.box.ParametricBox`).
-   Each **property's name, type, and value**.
-   Whatever your `__getstate__` returned (FreeCAD passes this back to `__setstate__` on load).

On load, FreeCAD recreates the document object, instantiates the proxy by looking up the saved module and class, calls `__setstate__`, and recomputes. Anything that changed between save and load is your problem to handle.


## Common changes and how to handle their migrations

### Renaming a property

A property name is part of the saved schema. Renaming `Length` to `BoxLength` orphans the old `Length` value in the saved document, and your `execute()` will fail when it tries to read the new name.

The pattern is to detect the old name during load and migrate it:

```python
def onDocumentRestored(self, obj):
    """Run after a saved document has been loaded."""
    if hasattr(obj, "Length") and not hasattr(obj, "BoxLength"):
        old_value = obj.Length
        obj.addProperty("App::PropertyLength", "BoxLength", "Box", "Length of the box")
        obj.BoxLength = old_value
        obj.removeProperty("Length")
```

`onDocumentRestored` runs once per object after a document has been loaded. It is the conventional place for migration code. Note of course that once migrated, the new file can no longer be read by the *old* version: this pattern is a one-way migration.


### Adding a property

When a new release adds a property that older saved documents do not have, your `__init__` will not run on those existing objects (it only runs when an object is first created). Add the new property in `onDocumentRestored` if it is missing:

```python
def onDocumentRestored(self, obj):
    if not hasattr(obj, "MaterialDensity"):
        obj.addProperty(
            "App::PropertyFloat", "MaterialDensity", "Material",
            "Density in kg/m^3",
        ).MaterialDensity = 1000.0
```

This runs once per object on first reopen after the addon update; subsequent reopens skip the addition because the property is already present.


### Changing a property's type

Property types are included in the saved file. Changing `App::PropertyFloat` to `App::PropertyLength` is a schema change FreeCAD will not perform silently. The migration pattern: read the old value, remove the old property, add the new property, set the value.

```python
def onDocumentRestored(self, obj):
    if obj.getTypeIdOfProperty("Length") == "App::PropertyFloat":
        old_value = float(obj.Length)
        obj.removeProperty("Length")
        obj.addProperty("App::PropertyLength", "Length", "Box", "Length of the box")
        obj.Length = old_value
```

Be conservative with property-type changes. They are intrusive and easy to get wrong.


### Renaming or moving the proxy class

Every saved document remembers your proxy by `module.ClassName`. Renaming `freecad.myaddon.box.Box` to `freecad.myaddon.shapes.Box` makes every existing document fail to find the class on load.

Three mitigations, in order of preference:

1.  **Don't rename.** The cheapest fix is the one you do not have to make. Do you *really* need to make this work for yourself?
2.  **Keep an alias.** Leave a stub at the old location that re-exports the class:

    ```python
    # freecad/myaddon/box.py (old location, kept as a stub)
    from freecad.myaddon.shapes import Box  # noqa: F401
    ```

    Existing documents continue to find `freecad.myaddon.box.Box` through the alias.

3.  **Migrate at load time.** When the addon detects an object whose `Proxy` failed to bind, recreate it. This is more involved and only worth the effort if alias-keeping is infeasible.


## Schema versioning

For addons whose schema is likely to change repeatedly, an explicit version property is worth the small overhead. Bump it every time you make a backwards-incompatible change, and use `onDocumentRestored` to upgrade older versions one step at a time:

```python
SCHEMA_VERSION = 3


def __init__(self, obj):
    obj.Proxy = self
    obj.addProperty("App::PropertyInteger", "SchemaVersion", "Internal", "").SchemaVersion = SCHEMA_VERSION
    # ... other properties ...


def onDocumentRestored(self, obj):
    if not hasattr(obj, "SchemaVersion"):
        obj.addProperty("App::PropertyInteger", "SchemaVersion", "Internal", "").SchemaVersion = 0

    while obj.SchemaVersion < SCHEMA_VERSION:
        self._migrate_one_step(obj)
        obj.SchemaVersion += 1
```

Each `_migrate_one_step` handles a single version transition (`0 -> 1`, `1 -> 2`, and so on). This makes migration code easier to reason about than a single function trying to handle every legacy state at once.

Mark the `SchemaVersion` property's group as `"Internal"` (or hide it via `obj.setEditorMode("SchemaVersion", 2)` for a fully hidden property) so users do not see or edit it.


## What not to do

-   **Do not silently drop data.** If a property has gone away, give the user a chance to see the old value (logged to the Report view at minimum) before discarding it.
-   **Do not change the meaning of an existing property** without renaming it. A user's document with `Length = 10` should mean the same thing in v1 and v2 of your addon, even if you have changed how `execute()` interprets it. If the meaning genuinely changes, treat it as a removed-and-added-again property.
-   **Do not assume `onDocumentRestored` runs only once.** It runs every time the document is opened. Migration code must check whether the migration has already been applied (typically via `hasattr` or a schema-version check) before doing anything.
-   **Do not skip a version.** If you bump from schema version 2 to 4, ensure intermediate users (still on version 1 or 2) can migrate through 2 → 3 → 4. The step-at-a-time pattern above handles this.


## Testing migrations: best practices

Keep a small fixture of saved documents from each historical version of your addon. Reopen them with the current code as part of pre-release smoke testing. A migration that works in isolation often fails on the specific quirks of a real, complex saved document.


## See also

-   [Custom document objects][DocObjects]: the underlying `FeaturePython` patterns.
-   [FreeCAD version compatibility][Compatibility]: the analogous concern for FreeCAD-version differences (rather than addon-version differences).
-   [Parametric Feature demo][DemoParam]: a runnable starting point for experimenting with schema changes.


[DocObjects]: ../../Code/Document-Objects
[Compatibility]: ../Compatibility
[DemoParam]: ../../../Demos/Parametric-Feature
