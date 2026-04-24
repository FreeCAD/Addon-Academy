---
layout : Default
---

# Addon Manifest

Addons should be distributed with a manifest file describing their contents. FreeCAD uses this metadata to determine what resources to load and what dependencies to install (among other things). The file also provides information used to display the addon in the [Addon Manager][AddonManager].


## Contents

* TOC
{:toc}


## Overall file format

This document currently describes file format version 1. This is the only file format at the time of this writing.

*NOTE: The original XML format and contents of this page were based on [REP 149][REP149].*

The metadata file must be a valid, well-formed XML 1.0 document. It must be called `package.xml`, and must exist in the base directory of each of the software package's displayed branches (as specified by the [FreeCAD-addons AddonCatalog.json file][AddonCatalog]) in its git repository. Each branch is expected to contain an independent `package.xml` file that pertains specifically to that branch (e.g. a "development" branch should specify a version number that makes it clear it is a development branch, etc.). All understood XML tags are in lowercase, but unrecognized tags are **not** an error. Most tags are optional, and some only apply to certain types of package contents (for example, only Workbenches currently provide a `classname` element). Unneeded or unrecognized elements are ignored.

Any file path specified in `package.xml` must use the slash (`/`) as the directory separator: on systems that expect a different separator during execution (e.g. Windows) FreeCAD will automatically convert to the correct separator.


## Tags

### `<package>` {#package}

The `<package>` tag is the only top-level element allowed in the manifest and there can only be one. All other tags and their contents are nested within it.

```xml
<package
    format="1"
    xmlns="https://wiki.freecad.org/Package_Metadata"
>
```

#### Attributes

-   `format="NUMBER"`: Specifies the version of the format being used, currently only version `"1"` exists.
-   `xmlns="NAMESPACE"`: Specifies the XML namespace being used. Must be set to `"https://wiki.freecad.org/Package_Metadata"`.

#### Required tags

The following tags must be present in the `<package>` element:

-   [`<name>`](#name)
-   [`<version>`](#version)
-   [`<date>`](#date)
-   [`<description>`](#description)
-   [`<maintainer>`](#maintainer)
-   [`<license>`](#license)
-   [`<icon>`](#icon)
-   [`<content>`](#content)

#### Optional tags

-   [`<url>`](#url)
-   [`<author>`](#author)
-   [`<depend>`](#depend)
-   [`<conflict>`](#conflict)
-   [`<replace>`](#replace)
-   [`<tag>`](#tag)
-   [`<freecadmin>`](#freecadmin)
-   [`<freecadmax>`](#freecadmax)
-   [`<pythonmin>`](#pythonmin)


### `<name>` {#name}

**REQUIRED**

The displayed name of this package. Must only contain characters that are valid for filenames (disallowed characters are `/\?%*:|"<>`). Does *not* have to match the name of the repository. Serves as the canonical name of the Addon when another Addon declares it as a dependency.


### `<version>` {#version}

**REQUIRED**

A version number that follows either the [semantic versioning 2.0 standard][SemVer] (e.g. `1.0.2-beta`) or the [CalVer style][CalVer] (e.g. `2021.12.08`). Note that you cannot include both types, and switching between types is not supported. Internally the code has no concept of which type is chosen, when comparing versions it performs a simple numerical comparison between each successive numeric component regardless of type. This cannot be left blank: some kind of version number *must* be assigned.

Note that you should increment this *anytime* you publish a change to your addon in a branch or tag that is listed in the Addon Index. Failing to do so results in an Addon with an "available update" to an identical version number, which is confusing to users. It's generally a best-practice to maintain a separate working branch for your day-to-day pushes, and only sync that branch to your actual listed release branch when you want to increment the version.


### `<date>` {#date}

**REQUIRED**

The date of the current version, in the format `YYYY-MM-DD` or `YYYY.MM.DD`. Required even if the version is CalVer style.


### `<description>` {#description}

**REQUIRED**

A concise (up to several sentences) text-only description of this package. No markup is supported. The Addon Manager will truncate overly-long descriptions, depending on the user's chosen view.


### `<maintainer>` {#maintainer}

**AT LEAST ONE REQUIRED** (multiple allowed)

The name of the person maintaining the package. All packages require a maintainer. For orphaned packages see below.

#### Attributes

-   `email="name@domain.tld"` (required): Email address of the maintainer.

An orphaned package is one with no current maintainer. Orphaned packages should use the following maintainer information:

```xml
<maintainer email="no-one@freecad.org">No current maintainer</maintainer>
```


### `<license>` {#license}

**AT LEAST ONE REQUIRED** (multiple allowed)

SPDX short identifier of the license(s) for this package, e.g. `BSD-2-Clause`, `GPL-3.0-or-later`, `LGPL-2.1-or-later`. In order to assist machine readability, only include the license's SPDX short identifier (see [the SPDX site][SPDX]). For multiple licenses multiple separate tags must be used. A package will have multiple licenses if different source files have different licenses. Every license occurring in the source files should have a corresponding `<license>` tag. For any explanatory text about licensing caveats, please use the `<description>` tag. To specify that no license applies (e.g. "All rights reserved.") set this value to `UNLICENSED`. To specify a custom license without an SPDX identifier set this value to `SEE LICENSE IN <filename>`.

Commonly-used license strings for code (typically in a `LICENSE-Code` file):

-   `Apache-2.0`
-   `BSD-2-Clause`
-   `BSD-3-Clause`
-   `BSL-1.0`
-   `GPL-2.0-or-later`
-   `GPL-3.0-or-later`
-   `LGPL-2.1-or-later`
-   `LGPL-3.0-or-later`
-   `MIT`
-   `MPL-1.1`
-   `CC0-1.0`

Commonly-used license strings for other non-code resources (typically in a `LICENSE-Resources` file):

-   `CC-BY-SA-4.0`
-   `CC0-1.0`

**Backwards-compatibility note:** The Addon Manager will attempt to normalize license identifiers that do not exactly match an SPDX license string. This will sometimes result in a license ID that yields a non-FSF-Libre or non-OSI-approved license: for example `LGPL2` will be normalized to `LGPL-2.0`, which is a non-FSF-Libre license: what was probably intended was `LGPL-2.1-or-later`.

#### Attributes

-   `file="FILE"` (optional): A path relative to the `package.xml` file containing the full license text. Many licenses require including the license text when redistributing the software. E.g. the Apache License, Version 2.0 states in paragraph 4.1: "You must give any other recipients of the Work or Derivative Works a copy of this License"


### `<content>` {#content}

**REQUIRED**

The `<content>` tag describes the actual contents of the package. It has no attributes, and contains any number of children. Those children can have arbitrary tag names, only some of which may be recognized by FreeCAD. FreeCAD currently supports `workbench`, `macro`, `preferencepack`, `bundle`, and `other` elements. Each child is then defined recursively by this standard, containing any or all of the elements allowed for the root `<package>` node. For example:

```xml
<content>
  <preferencepack>
    <name>Unicorn Sparkles Theme</name>
    <version>1.0.0</version>
    <url type="readme">https://github.com/chennes/FreeCAD-themes/blob/main/Unicorn%20Sparkles%20Theme/Readme.md</url>
    <icon>sparkles.svg</icon>
  </preferencepack>
</content>
```

The existence of most `<content>` items implies a set of subfolders, one for each content item, named exactly as the given name of the item. So for the example above, the package's folder structure is:

```
Package Directory/
  package.xml
  Unicorn Sparkles Theme/
    Unicorn Sparkles Theme.cfg
    sparkles.svg
    (the theme's other files)
```

In addition to the other elements of `<package>`, content items can optionally provide information in `<icon>`, `<classname>`, and `<file>` tags (technically these can be provided to the root `<package>` tag as well, but they are generally unused there).

**Backwards-compatibility note:** to avoid having to restructure packages that pre-date this metadata standard, the optional [`<subdirectory>`](#subdirectory) tag is allowed to specify `./` as the subdirectory for a content item, in which case no subdirectory is required. This matches the pre-standard system where a single workbench was located at the top of the directory structure.


#### `<icon>` {#icon}

**REQUIRED for Workbenches**

The path to an icon file. If it is an icon for the top-level package this path is relative to the `package.xml` file itself. If the icon is an element of a `<content>` item, then the path is relative to the content's folder. The Addon Manager will display the top-level icon as the icon for the overall package. If no top-level icon is present, the first specified workbench icon will be used as the package icon.


#### `<subdirectory>` {#subdirectory}

**Optional**

Normally a content item is assumed to be located in a subdirectory with the same name as the item. In some cases, however, it is useful to explicitly specify the subdirectory. For example, many macros may be located within a single subdirectory, but each have their own entry in the `package.xml` file. It also provides backwards-compatibility support for packages that predate the `package.xml` file format specification, and do not follow the expected subdirectory structure. Often in these cases, a `<subdirectory>./</subdirectory>` is used to indicate that the item is not located in a subdirectory at all.


#### `<classname>` {#classname}

**REQUIRED for Workbenches**

For workbenches, the name of the Python main entry class. This is the class that FreeCAD will try to load on startup to locate the workbench's icon, which should be set as a member variable of the class. For example, if your workbench defines the following class (usually in `InitGui.py`):

```python
class MyNewWB:
    Icon="resources/icon.svg"
```

then the `package.xml` file expects:

```xml
<classname>MyNewWB</classname>
```


#### `<file>` {#file}

**Optional**

Provided for convenience to other tools, any number of other files may be listed here. Their use depends on the type of content. In a macro content item, each file entry is a single macro, and will be linked into the user's Macros installation directory by the [Addon Manager][AddonManager].


### `<url>` {#url}

**Multiple allowed.** `repository` is required, and `readme`-type is highly recommended.

A Uniform Resource Locator for the package's website, bug tracker, source repository, zip download link, readme file, or documentation (as specified by the `type` attribute, see below).

When specifying the `readme` type, a direct link to a rendered version of the README should be provided. For example, on GitHub, this is a `blob`-type link such as `https://github.com/FreeCAD/FreeCAD-addons/blob/master/README.md`, or on a GitLab instance, `https://gitlab.com/opensimproject/cfdof/-/blob/master/README.md` (note the slightly different URL format between the two).

It is a good idea to include `<url>` tags pointing users to your package's online resources. The website is commonly a wiki page on `wiki.freecad.org` where users can find and update information about the package, for example. The Addon Manager lists these URLs and provides clickable links to them in the package description.

#### Attributes

-   `type="TYPE"` (required): The type should be one of the following identifiers: `website`, `bugtracker`, `repository`, `readme`, `documentation`, or `discussion`.
-   `branch="BRANCH"` (required for `type="repository"`): The name of the branch to check out to obtain this package. Typically the name of your main development branch. May also specify any other type of git reference, e.g. a tag or specific commit.


### `<author>` {#author}

**Multiple allowed**

The name of a person who is an author of the package, as acknowledgement of their work and for questions.

#### Attributes

-   `email="name@domain.tld"` (optional): Email address of author.


### `<depend>` {#depend}

**Multiple allowed**, at least one required for bundles.

Declares a dependency on another FreeCAD Addon or internal workbench, or Python package. The named dependency is first checked against the list of known Addons (e.g. those available either from the official FreeCAD Addons git repository, or those in a custom user-specified repository). The check is against the canonical name of the Addon. If a `package.xml` file is present for that Addon, the name is that package's `<name>` element. An exact match is required. If no match is found it is checked against the list of known internal workbenches (both installed and uninstalled). Finally, if the named dependency has not been located in the previous two steps it is assumed to be a Python package dependency. Note that not all dependency-related features are fully implemented yet.

A `bundle` content item is expected to contain multiple `depends` lines, one for each external addon being "bundled". Note that the bundling is not literal, in the sense that the bundle is not expected to actually contain the source code of the dependency, but only to declare that it must be installed by the Addon Manager as part of installing the bundle.

#### Attributes

All dependencies and relationships may restrict their applicability to particular versions. For each comparison operator an attribute can be used. Two of these attributes can be used together to describe a version range.

-   `version_lt="VERSION"` (optional): The dependency to the package is restricted to versions less than the stated version number.
-   `version_lte="VERSION"` (optional): The dependency to the package is restricted to versions less or equal than the stated version number.
-   `version_eq="VERSION"` (optional): The dependency to the package is restricted to a version equal than the stated version number.
-   `version_gte="VERSION"` (optional): The dependency to the package is restricted to versions greater or equal than the stated version number.
-   `version_gt="VERSION"` (optional): The dependency to the package is restricted to versions greater than the stated version number.
-   `optional="true|false"`: If `optional` is `true`, then the dependency is treated as optional when the Addon is installed using the Addon Manager. In general this means that a failure to install the dependency does not prevent the Addon from installing, and the user may be prompted about whether they want to install it.
-   `type="automatic|addon|internal|python"`: Optional, defaults to `automatic`. Indicates what this dependency statement refers to. `addon` is for external addons, `internal` is for internal workbenches and `python` indicates a Python package dependency.

##### Type: internal

The following internal workbench types are available:

-   `assembly`
-   `bim`
-   `cam`
-   `draft`
-   `fem`
-   `import`
-   `material`
-   `mesh`
-   `openscad`
-   `part`
-   `partdesign`
-   `plot`
-   `points`
-   `reverseengineering`
-   `robot`
-   `sketcher`
-   `spreadsheet`
-   `techdraw`
-   `tux`
-   `web`


### `<conflict>` {#conflict}

**Multiple allowed**

Declares a package name with which this package conflicts. This package and the conflicting package should not be installed at the same time.

#### Attributes

See [`<depend>`](#depend).


### `<replace>` {#replace}

**Multiple allowed**

Declares a package name that this package is intended to replace.

#### Attributes

See [`<depend>`](#depend).


### `<tag>` {#tag}

A simple text tag used for categorization when using a package manager. Multiple `<tag>` elements may be specified.


### `<freecadmin>` {#freecadmin}

The minimum version of FreeCAD required to use this package/element, as a semantic version 2.0 string in the format `MAJOR.MINOR.BUILD`. This tag may be used to specify that a particular branch of this addon should only be shown to users of a specific FreeCAD version (or later). It may be combined with `<freecadmax>` to set a specific valid range.


### `<freecadmax>` {#freecadmax}

The maximum version of FreeCAD required to use package/element, as a semantic version 2.0 string in the format `MAJOR.MINOR.BUILD`. This tag may be used to specify that a particular branch of this addon should only be shown to users of a specific FreeCAD version (or earlier). It may be combined with `<freecadmin>` to set a specific valid range. Note that it is an exact version string, so to indicate that the addon supports an entire minor release, the "patch" component should be chosen to be a suitably large number (e.g. `1.0.99` to support the entire 1.0.x release series).


### `<pythonmin>` {#pythonmin}

The minimum version of Python required to use package/element, as a semantic version 2.0 string in the format `MAJOR.MINOR`. The Addon Manager will not permit an Addon to be installed on a system running a version of Python before this one. Only Python 3.x versions are supported. Although you may specify a three-component version, only the minor number is considered during the compatibility check.


## Quick guide

For a quick guide on how to create a basic `package.xml` file and add a workbench to the [Addon Manager][AddonManager], see [Add Workbench to Addon Manager][AddWorkbench].


## Examples

Note that comments (the text between `<!--` and `-->`) are ignored by the XML parser, and are not a required part of the file format. They are provided here for information purposes and may be omitted from the final `package.xml` if desired.


### Simple workbench-only package

A simple workbench-only package (for example, to add a metadata file to a package that predates this metadata format):

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<package format="1" xmlns="https://wiki.freecad.org/Package_Metadata">
  <name>Legacy Workbench</name> <!-- What the Addon Manager displays to users -->
  <description>Text that the Addon Manager shows for the Addon. Any length, but remember that Addon Manager's compact view only shows the first sentence or so.</description>
  <version>1.0.1</version> <!-- Semantic versioning (1.2.3-beta) or CalVer-based, (2022.01.07), don't omit or non-git installations won't see your updates -->
  <date>2022-01-07</date> <!-- Date of the last update to the version number -->
  <maintainer email="your_address@null.com">Your Name</maintainer>
  <license file="LICENSE">LGPL-2.1-or-later</license> <!-- Make sure you actually have this file in your Addon repo if the license requires it -->
  <url type="repository" branch="main">https://github.com/chennes/FreeCAD-Package</url> <!-- Don't forget to update the branch name here -->
  <url type="readme">https://github.com/chennes/FreeCAD-Package/blob/main/README.md</url> <!-- Link to the HTML-rendered README page -->
  <icon>Resources/icons/PackageIcon.svg</icon> <!-- If you include your icon here, you don't have to submit it to the main FreeCAD repo -->

  <content>
    <workbench>
      <classname>MyLegacyWorkbench</classname> <!-- Must match class name in InitGui.py -->
      <subdirectory>./</subdirectory>
    </workbench>
  </content>

</package>
```


### Complex multi-component package

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<package format="1" xmlns="https://wiki.freecad.org/Package_Metadata">
  <name>Example Package Format</name>
  <description>An example of the package.xml file format</description>
  <version>2022.01</version>
  <date>2022-01-07</date>
  <maintainer email="no-one@freecad.org">No Maintainer</maintainer>
  <license file="LICENSE">GPL-3.0-or-later</license>
  <url type="repository" branch="main">https://github.com/chennes/FreeCAD-Package</url>
  <icon>PackageIcon.svg</icon>

  <content>
    <preferencepack>
      <name>FreeCAD Classic Colors</name>
      <description>FreeCAD default colors for core app and included Mods.</description>
      <version>1.0.0</version>
      <tag>color</tag>
      <tag>stylesheet</tag>
    </preferencepack>
    <workbench>
      <name>Metadata Creation Workbench</name>
      <description>A set of tools to assist in creation of package.xml metadata files</description>
      <classname>MetadataCreationWorkbench</classname>
      <subdirectory>MCW</subdirectory>
      <icon>Resources/mcw.svg</icon>
      <tag>developers</tag>
      <version>0.9.0-alpha</version>
    </workbench>
    <macro>
      <name>Problem Solver 9000</name>
      <description>Deletes all emails in your inbox</description>
      <subdirectory>./</subdirectory>
      <file>PS9000.FCMacro</file>
    </macro>
  </content>

</package>
```


### Package with dependencies

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<package format="1" xmlns="https://wiki.freecad.org/Package_Metadata">
  <name>Example with Dependencies</name>
  <description>An example of the package.xml file format</description>
  <version>1.0.1-beta3</version>
  <date>2022-01-07</date>
  <maintainer email="no-one@freecad.org">No Maintainer</maintainer>
  <license file="LICENSE">GPL-3.0-or-later</license>
  <url type="repository" branch="main">https://github.com/chennes/FreeCAD-Package</url>
  <icon>PackageIcon.svg</icon>

  <content>
    <workbench>
      <name>Metadata Creation Workbench</name>
      <description>A set of tools to assist in creation of package.xml metadata files</description>
      <classname>MetadataCreationWorkbench</classname>
      <subdirectory>MCW</subdirectory>
      <icon>Resources/mcw.svg</icon>
      <tag>developers</tag>

      <depend>FEM</depend>
      <depend version_gte="0.3.0">Curves workbench</depend>
      <depend version_gte="3.3" version_lt="4">Steel column</depend>

      <depend optional="true" type="python">markdown</depend>
      <depend type="addon">TabBar</depend>

      <!-- If this package is installed, the Addon Manager may warn the user to remove it -->
      <replace>Metadata Creation Workbench Beta</replace>

      <!-- An unresolvable conflict to prevent installation on, e.g. a specific build -->
      <conflict condition="$BuildRevision==24267">Do not use with build 24267</conflict>

      <!-- Python package dependencies (no support for version information) -->
      <depend>matplotlib</depend>
      <depend>some_other_package</depend> <!-- Assumed to be a Python dependency because it's unrecognized -->
    </workbench>
  </content>

</package>
```


### Workbench addon

A complete `package.xml` for a workbench-style addon, formatted in the Academy's preferred style: [Workbench.xml][ExampleWorkbench]


### Toolbar extension

A `package.xml` for an addon that uses the `<other/>` content type to ship a toolbar extension to an existing workbench: [Toolbar.xml][ExampleToolbar]


[AddonManager]: https://wiki.freecad.org/Std_AddonMgr
[AddonCatalog]: https://github.com/FreeCAD/FreeCAD-addons/blob/master/AddonCatalog.json
[AddWorkbench]: https://wiki.freecad.org/Add_Workbench_to_Addon_Manager
[REP149]: https://ros.org/reps/rep-0149.html
[SemVer]: https://semver.org
[CalVer]: https://calver.org/
[SPDX]: https://spdx.org/licenses/

[ExampleWorkbench]: ./Examples/Workbench.xml
[ExampleToolbar]: ./Examples/Toolbar.xml
