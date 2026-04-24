---
layout : Default
---

# Translations (i18n)

*Originally based on the FreeCAD wiki's [Translating an external workbench][WikiSource] page, updated for the current FreeCAD and Modern addon layout.*

In the following notes, `"context"` should be your addon's or workbench's name, for example, `"MySuperAddon"` or `"DraftPlus"`, or whatever. Capitalization matters here: `"Context"` is not the same as `"context"` for example. The context makes it so that all translation of your code will be gathered under the same name, to be more easily identified by translators. That is, they will know exactly to which addon or workbench a particular string belongs.


## What to translate, and what not to

Translate text that is visible to the user in the FreeCAD UI: menu items, dialog labels, status-bar messages, tooltips, property descriptions, object labels, and so on.

**Do not translate** text that is primarily developer-facing:

-   Output sent to `FreeCAD.Console.PrintMessage/PrintLog/PrintWarning/PrintError`. These messages land in the Report view, which is a developer-facing log panel; use `QMessageBox` for anything the user needs to see. See [Logging & console][Logging] for the reasoning.
-   `print()` output (which goes to the Python console).
-   Technical identifiers: property names, class names, internal command IDs.
-   File-format keywords (XML tags, JSON keys, etc.).


## Marking strings in code

### `translate()` vs `QT_TRANSLATE_NOOP`

Two functions cover almost every case, and the distinction matters:

**`translate()`** performs the actual lookup at runtime. When your code calls `translate("MyAddon", "Hello")`, Qt looks `"Hello"` up in the loaded translation file and returns the localized string. It also serves as a marker for the `lupdate` utility: *if and only if* the string argument is a string literal, `lupdate` will extract it into the `.ts` file. Variables passed to `translate()` are ignored by `lupdate` but still translated at runtime IF the translation has been available. See below...

**`QT_TRANSLATE_NOOP`** does nothing at runtime. It returns the input string unchanged. Its sole purpose is to mark a string literal for extraction by `lupdate`. Use it when the string needs to be extracted *now* but translated *later*, typically for class-level attributes, module-level constants, and command-resource dictionaries that are evaluated before the translator is installed.

You may also see `tr()` and `QT_TR_NOOP`, which automatically provide the context based on the calling class. These are less common in FreeCAD addons; prefer the explicit-context forms above.


### In every Python file

You need a `translate()` function available in every file that translates text. It must be named exactly `translate`: the string extractor relies on that exact name. The cleanest way is:

```python
import FreeCAD
translate = FreeCAD.Qt.translate
```

All user-facing text passes through `translate()`:

```python
dialog.setText(translate("MyAddon", "My text"))
```

You must pass string *literals*. `lupdate` is a text processor, it does not execute your code. Variables passed to `translate()` are translated at runtime but not extracted into the `.ts` file. For example:

```python
# This works. "My text" is a literal, lupdate extracts it:
dialog.setText(translate("MyAddon", "My text"))

# This does NOT get extracted. lupdate only sees the variable name `a_variable`:
a_variable = "My text"
dialog.setText(translate("MyAddon", a_variable))

# This works. `a_variable` already contains the translated string:
a_variable = translate("MyAddon", "My text")
dialog.setText(a_variable)
```

If you use `.ui` files from Qt Designer, nothing special needs to be done. Qt's tooling extracts strings from `.ui` files automatically.


### In `init_gui.py`

Import `QT_TRANSLATE_NOOP` near the top:

```python
from PySide.QtCore import QT_TRANSLATE_NOOP
```

Use `"Workbench"` as the context for menu and toolbar names:

```python
self.appendMenu(QT_TRANSLATE_NOOP("Workbench", "My menu"), [...])
self.appendToolbar(QT_TRANSLATE_NOOP("Workbench", "My toolbar"), [...])
```

Register your translations directory so FreeCAD can find the compiled `.qm` files. In a Modern (namespaced) addon, `init_gui.py` lives under `freecad/<ModName>/` and has a valid `__file__`:

```python
import os
import FreeCADGui
FreeCADGui.addLanguagePath(
    os.path.join(os.path.dirname(__file__), "resources", "translations")
)
FreeCADGui.updateLocale()
```


### Inside each FreeCAD command class

Import `QT_TRANSLATE_NOOP` and wrap the command's `MenuText` and `ToolTip` with it. Use the command's registered name as the context:

```python
from PySide.QtCore import QT_TRANSLATE_NOOP

class My_Command_Class:
    def GetResources(self):
        return {
            'Pixmap':   "path/to/icon.svg",
            'MenuText': QT_TRANSLATE_NOOP("CommandName", "My Command"),
            'ToolTip':  QT_TRANSLATE_NOOP("CommandName", "Describes what the command does"),
            'Accel':    "Shift+A",
        }
```

where `"CommandName"` is the name of the command, defined by:

```python
FreeCADGui.addCommand('CommandName', My_Command_Class())
```

When FreeCAD displays the command, it internally calls `translate()` on each of these strings, relying on `lupdate` having already extracted the literals from the `QT_TRANSLATE_NOOP` markers. See the [Technical details](#technical-details) section below for a full explanation.


### Object property descriptions

Don't translate property names. Wrap the description with `QT_TRANSLATE_NOOP`, using the special context `"App::Property"`:

```python
obj.addProperty(
    "App::PropertyBool",
    "MyProperty",
    "PropertyGroup",
    QT_TRANSLATE_NOOP("App::Property", "This is what My Property does"),
)
```

Use `"App::Property"` as the context rather than your own addon name; it's the convention FreeCAD relies on for property descriptions.


### Object names vs labels

When creating new objects, do not translate the object's `Name`. Translate the `Label` instead. A `Name` is unique and stays the same throughout the object's life; a `Label` is user-visible and can be changed by the user as desired.


## Directory layout and file naming

Conventional directory layouts:

-   **Modern** (Addon-Template, SheetMetal, most current addons): `Resources/translations/` at the repository root.
-   **Cookiecutter**: `freecad/<ModName>/resources/translations/`.

Either works. Pick one and make sure your `addLanguagePath` call in `init_gui.py` points to it.

Within that directory, name files `<AddonName>_<locale>.ts` (and correspondingly `<AddonName>_<locale>.qm`), e.g. `SheetMetal_de.ts`, `SheetMetal_pt-BR.ts`. The locale-agnostic template, what `lupdate` populates before per-language translations exist, is `<AddonName>.ts`.

Ship *both* `.ts` and `.qm` files in the repository. `.qm` files are what FreeCAD loads at runtime; the `.ts` files let translators rebase without re-extracting from source.


## Generating the `.ts` files

### Recommended tooling

The Academy ships two wrapper scripts that you can drop into your addon's `Resources/translations/` folder. They serve different use cases, so which one (or both) to adopt depends on your situation.

#### Python: full Crowdin release cycle

[**`run_translation_cycle.py`**][PyScript] runs an end-to-end cycle in a single invocation: downloads the latest translations from Crowdin, compiles the `.qm` files, re-extracts source strings via `lupdate`, and uploads the updated master `.ts` back to Crowdin. Uses only the Python standard library plus the Qt6 `lupdate` / `lrelease` tools on `PATH`, so it's cross-platform (Linux, macOS, and Windows).

This script is derived from [FreeCAD Telemetry's `run_translation_cycle.py`][TelemetryScript], which is itself descended from FreeCAD core's `updatecrowdin.py`.

Edit a handful of constants at the top for your addon:

```python
CROWDIN_PROJECT_NAME = "YourAddon"
CROWDIN_FILE_NAME = f"{CROWDIN_PROJECT_NAME}.ts"
MIN_TRANSLATION_THRESHOLD = 0.5
```

Requires a Crowdin API token with write access to the `freecad-addons` project, supplied via the `CROWDIN_API_TOKEN` environment variable or a `~/.crowdin-freecad-token` file. Typically reserved for addon maintainers.

#### Shell: partial workflows, day-to-day iteration

[**`update_translation.sh`**][ShellScript] is a bash script with sub-commands for partial workflows, useful for iterating on a single locale locally, or for contributors who don't have Crowdin write access. Maintained by the [SheetMetal workbench][SheetMetalTranslations] and vendored here (change the `WB="YourAddon"` variable at the top of the script).

Flags:

-   `-u <locale>`: create or update a single locale's `.ts`.
-   `-U`: update *all* `.ts` files from source.
-   `-r <locale>`: compile a single locale's `.qm`.
-   `-R`: compile all `.qm` files.
-   `-N`: normalize Crowdin's locale-name quirks.

No API token needed; uploads and downloads happen via Crowdin's web UI. [SheetMetal's translations README][SheetMetalReadme] documents the translator and maintainer workflows in detail.

#### Which to use

-   **Maintainer with Crowdin write access:** the Python script, for a one-command full release cycle.
-   **Non-maintainer contributor, or local-only iteration:** the shell script.
-   **Addon not yet on Crowdin:** the shell script. The Python one is Crowdin-specific.
-   **Windows host without WSL or Git Bash:** the Python script. The shell script needs a Unix-like shell.

### Manual Qt6 invocation

Under Qt6, `lupdate` handles both `.ui` and `.py` sources in a single pass; the separate `pylupdate` / `lconvert` steps that Qt5 required are no longer needed:

```shell
lupdate *.ui *.py -ts translations/MyModule.ts
```

Qt6 `lupdate` recursively descends into subdirectories.

On common Linux distributions:

-   **Debian / Ubuntu**: `sudo apt-get install qttools5-dev-tools pyqt6-dev-tools`
-   **Fedora**: `sudo dnf install qt6-linguist qt6-devel`
-   **Arch**: `sudo pacman -S qt6-tools python-pyqt6`

### Qt5 and earlier (legacy)

The Qt5 Python toolchain is known to be buggy and should be avoided for new work. If you must use it, extract `.ui` and `.py` separately and merge:

```shell
lupdate *.ui -ts translations/uifiles.ts
pylupdate *.py -ts translations/pyfiles.ts
lconvert -i translations/uifiles.ts translations/pyfiles.ts -o translations/MyModule.ts
rm translations/pyfiles.ts translations/uifiles.ts
```


## Translation workflow

### Using Crowdin (preferred)

FreeCAD hosts a dedicated Crowdin project for addons: [**freecad-addons**][CrowdinAddons], a separate project from the core [freecad][CrowdinFreeCAD] Crowdin. To add your addon:

1.  Coordinate with the FreeCAD i18n team via the [FreeCAD forum][Forum] or the addons repository.
2.  Once your addon is listed on Crowdin, upload your `<AddonName>.ts` template.
3.  Translators contribute there without touching your codebase.
4.  Pull completed translations back into `Resources/translations/` as part of your release cycle.

Many addons (SheetMetal included) have moved to Crowdin-only and no longer accept pull requests against `.ts` files, since those would be overwritten by the next Crowdin sync.

### Using your own account

You can also host translations yourself on [Crowdin][Crowdin] or [Transifex][Transifex]. Some platforms integrate with GitHub for automated upload and download. If you go that route you cannot share the FreeCAD Crowdin project; you need your own account.


## Merging and compiling translations

Once your `.ts` files have been translated (via Crowdin or locally), place all the `<AddonName>_<locale>.ts` files, together with your base `<AddonName>.ts` template, in the translations folder.

Run `lrelease` on each locale file to produce the `.qm` binary FreeCAD loads at runtime:

```shell
lrelease "translations/MyModule_de.ts"
lrelease "translations/MyModule_fr.ts"
lrelease "translations/MyModule_pt-BR.ts"
```

Or in a loop:

```shell
for f in translations/*_*.ts; do
    lrelease "$f"
done
```

You should get one `.qm` file for each translated `.ts` file. The wrapper script above collapses this into `./update_translation.sh -R`.

Note that certain parts of your workbench cannot be translated on-the-fly if the user switches languages; they will need to restart FreeCAD for the new language to take effect.


## Testing translations

1.  Switch FreeCAD to a language you have translated (for example, German).
2.  Ensure your addon calls `FreeCADGui.addLanguagePath("/path/to/translations")` during startup.
3.  Test by evaluating a known translated string, for example:
    ```python
    FreeCAD.Qt.translate("your context", "some string")
    ```

If you get the expected translation back, the basic setup is working. If not, verify that both the *context* and the *string* you're testing actually exist in the `.ts` / `.qm` file; a typo in either will silently return the English original.


## Technical details

This section goes into more detail on the `translate()` / `QT_TRANSLATE_NOOP` distinction, for readers who want the full picture.

`translate()` (and its siblings `tr()` and `self.tr()`) do two separate things. At runtime, they perform the actual translation lookup; this works whether you pass a literal string, a variable, or a constant, because the lookup is dynamic. Separately, they are also recognized by the `lupdate` utility: if (and only if) they contain a string literal, that literal is extracted into the `.ts` file. Variables passed to `translate()` are ignored by `lupdate` but still translated at runtime, as long as *some* piece of code, somewhere, called one of the translation functions with the matching literal so the extractor could pick it up. The code containing that literal does not need to ever execute; `lupdate` performs no code analysis, only a string search.

In contrast, `QT_TRANSLATE_NOOP` and `QT_TR_NOOP` do nothing at all at runtime; they are literal no-ops. Their sole purpose is to mark a literal string for extraction. This is exactly what you want when a string needs to be *extracted* at one point in the code but *translated* at a different point. The canonical case is a command's `GetResources()` dictionary:

```python
def GetResources(self):
    return {
        'Pixmap':   "path/to/icon.svg",
        'MenuText': QT_TRANSLATE_NOOP("CommandName", "My Command"),
        'ToolTip':  QT_TRANSLATE_NOOP("CommandName", "Describes what the command does"),
        'Accel':    "Shift+A",
    }
```

At runtime, the returned dictionary literally contains:

```python
{
    'Pixmap':   "path/to/icon.svg",
    'MenuText': "My Command",
    'ToolTip':  "Describes what the command does",
    'Accel':    "Shift+A",
}
```

There is no translation information in this dictionary. When FreeCAD later displays the command, the pseudo-code is:

```python
for command in commands:
    resources = command.GetResources()
    menu_text = translate(resources['MenuText'])
```

`lupdate` cannot extract any string from this `translate()` call because the argument is a variable. So `lupdate` ignores it, but at runtime Qt still looks up the passed string, which succeeds because the literal `"My Command"` was extracted earlier from the `QT_TRANSLATE_NOOP` call in `GetResources()`.

To verify that the expected strings are being extracted, inspect the `.ts` file directly or run `lupdate` manually:

```shell
lupdate myfile.py -ts outfile.ts
```

The file `outfile.ts` will contain the set of strings that would be uploaded for translation.


## Further reading

-   [Translating an external workbench][WikiSource]: the FreeCAD wiki page this one is based on.
-   [SheetMetal translation README][SheetMetalReadme]: the reference implementation for the script-based workflow.
-   [Localisation][Localisation]: core FreeCAD translation.
-   Why and how to translate `openCommand()` functions: [forum thread][OpenCommandForum].
-   [Translating external workbenches][TranslatingForum]: forum discussion.


[Logging]: ../Logging

[WikiSource]: https://wiki.freecad.org/Translating_an_external_workbench

[PyScript]: ./run_translation_cycle.py
[ShellScript]: ./update_translation.sh

[TelemetryScript]: https://github.com/FreeCAD/FreeCAD-Telemetry/blob/main/Resources/translations/run_translation_cycle.py
[SheetMetalTranslations]: https://github.com/shaise/FreeCAD_SheetMetal/tree/master/Resources/translations
[SheetMetalReadme]: https://github.com/shaise/FreeCAD_SheetMetal/blob/master/Resources/translations/README.md

[CrowdinAddons]: https://crowdin.com/project/freecad-addons
[CrowdinFreeCAD]: https://crowdin.com/project/freecad
[Crowdin]: https://crowdin.com/
[Transifex]: https://www.transifex.com/

[Forum]: https://forum.freecad.org/
[OpenCommandForum]: https://forum.freecad.org/viewtopic.php?f=10&t=55869
[Localisation]: https://wiki.freecad.org/Localisation
[TranslatingForum]: https://forum.freecad.org/viewtopic.php?f=10&t=36413
