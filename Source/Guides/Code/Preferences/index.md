---
layout : Default
---

# Preferences pages

A preferences page lets users configure your addon from the standard **Edit → Preferences** dialog. FreeCAD does most of the work for you: Qt Designer forms containing FreeCAD's `Gui::Pref*` family of widgets automatically save their values to (and restore them from) the parameter store.

This page walks through the pattern, using the [SheetMetal workbench][SheetMetalRepo] as an example. Thanks to @shaise for writing such a great Addon!


## The three pieces

Every preferences page is made up of three components:

1.  **A Qt Designer `.ui` file** describing the page layout, using `Gui::Pref*` widgets for every value you want persisted.
2.  **A registration call** in `init_gui.py` that tells FreeCAD about the `.ui` file.
3.  **Python code that reads the stored values** when your addon needs them.

FreeCAD handles the save and restore automatically: no code is needed to write a value when the user clicks *OK* or to read the initial value when the preferences dialog opens.


## Designing the `.ui` form

Create the preferences page as a standard Qt Designer form. For every value the user should configure, drop in a widget from FreeCAD's `Gui::Pref*` family instead of the corresponding plain Qt widget. The most common ones are `Gui::PrefCheckBox`, `Gui::PrefComboBox`, `Gui::PrefSpinBox`, `Gui::PrefDoubleSpinBox`, `Gui::PrefLineEdit`, and `Gui::PrefColorButton`; the full set mirrors Qt's basic input widgets.

Each `Gui::Pref*` widget has two custom properties that control how it's persisted:

-   **`prefEntry`**: the key name the value is stored under.
-   **`prefPath`**: the path within the parameter store, relative to `User parameter:BaseApp/Preferences/`. A conventional path is `Mod/<AddonName>`.

Set both on every `Gui::Pref*` widget you add. For example, a combo box in SheetMetal's preferences form is configured roughly like:

```xml
<widget class="Gui::PrefComboBox" name="gui::comboBox">
  <property name="prefEntry" stdset="0">
    <cstring>EngineeringUXMode</cstring>
  </property>
  <property name="prefPath" stdset="0">
    <cstring>Mod/SheetMetal</cstring>
  </property>
  ...
</widget>
```

When the preferences dialog opens, FreeCAD reads the stored value (from `User parameter:BaseApp/Preferences/Mod/SheetMetal/EngineeringUXMode` in that example) and populates the widget; when the user clicks *OK*, the widget's current value is written back.

**NOTE:** To use the `Gui::Pref*` widgets directly in Qt Designer you will need to install FreeCAD's Designer plugin. As an alternative you can edit the `.ui` XML by hand after saving the original using the basic Qt widget set.

SheetMetal's [`Resources/panels/SMprefs.ui`][SMprefsUI] is a complete, representative example of a FreeCAD preferences form.


## Registering the page

In your `init_gui.py`, call `Gui.addPreferencePage` with the path to your `.ui` file and the group name that should appear in the preferences dialog's sidebar:

```python
import os
import FreeCADGui
FreeCADGui.addPreferencePage(
    os.path.join(os.path.dirname(__file__), "Resources", "panels", "MyAddonPrefs.ui"),
    "MyAddon",
)
```

Call `addPreferencePage` only once at startup. Calling it multiple times will add the page multiple times to the dialog.

SheetMetal does this in [`InitGui.py`][SheetMetalInitGui]:

```python
Gui.addPreferencePage(os.path.join(SMWBPath, "Resources/panels/SMprefs.ui"), "SheetMetal")
```


## Sidebar icon

FreeCAD looks for a file named `preferences-<modulename>.svg` (all lowercase) on the registered icon path to use as the sidebar icon for your preferences group. For a group named `"MyAddon"`, the icon file should be `preferences-myaddon.svg`. See [Icons & resources][Icons] for details on registering the icon path.

SheetMetal's sidebar icon lives at `Resources/icons/preferences-sheetmetal.svg`.


## Reading values at runtime

When your addon code needs a current preference value, look it up through `FreeCAD.ParamGet`. The full path is `User parameter:BaseApp/Preferences/` followed by the `prefPath` you set on the widget:

```python
import FreeCAD
params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/MyAddon")
```

The returned parameter group exposes typed getters and setters. Match the type to the widget you used in the form:

| Widget                   | Read                                                      | Write                          |
|--------------------------|-----------------------------------------------------------|--------------------------------|
| `Gui::PrefCheckBox`      | `params.GetBool(key, default)`                            | `params.SetBool(key, value)`   |
| `Gui::PrefSpinBox`       | `params.GetInt(key, default)`                             | `params.SetInt(key, value)`    |
| `Gui::PrefDoubleSpinBox` | `params.GetFloat(key, default)`                           | `params.SetFloat(key, value)`  |
| `Gui::PrefComboBox`      | `params.GetInt(key, default)` (stores the selected index) | `params.SetInt(key, value)`    |
| `Gui::PrefLineEdit`      | `params.GetString(key, default)`                          | `params.SetString(key, value)` |

Always pass a default value to the getter. FreeCAD returns the default if the user has never opened the preferences dialog (in which case no value has been written yet):

```python
auto_link = params.GetInt("AutoLinkBendRadius", 0)
```

SheetMetal's [`SheetMetalTools.py`][SheetMetalTools] shows this pattern in full, including helpers that save and restore values for dialogs that aren't full preferences pages.


## Further reading

-   [SheetMetal workbench][SheetMetalRepo]: the worked example this page is built around.
-   SheetMetal [`SMprefs.ui`][SMprefsUI]: the preferences form.
-   SheetMetal [`InitGui.py`][SheetMetalInitGui]: the `addPreferencePage` registration.
-   SheetMetal [`SheetMetalTools.py`][SheetMetalTools]: `ParamGet` usage patterns.


[Icons]: ../Icons

[SheetMetalRepo]: https://github.com/shaise/FreeCAD_SheetMetal
[SMprefsUI]: https://github.com/shaise/FreeCAD_SheetMetal/blob/master/Resources/panels/SMprefs.ui
[SheetMetalInitGui]: https://github.com/shaise/FreeCAD_SheetMetal/blob/master/InitGui.py
[SheetMetalTools]: https://github.com/shaise/FreeCAD_SheetMetal/blob/master/SheetMetalTools.py
