---
layout : Default
---

# Qualities

In order to be included in the FreeCAD Addon Index, an addon must comply with a minimum set of quality requirements.

## Governance

- The addon has at least one active maintainer or is in the process of finding a new maintainer.

- The addon maintainers address user concerns such as open issues, pull requests, and security advisories in a timely manner.

## Compliance

- The addon complies with GDPR, doesn't send user data to 3rd parties unless expressly permitted by the user, and in permitted cases keeps the data to the minimum required.

- The addon is open, clear and direct with the user about any external connections, services, etc. it uses, what data it sends, when and how often it does so, etc.

- The addon informs its users and re-requests consent if its use of their data changes.

- The addon makes an effort to use secure storage options of the user's system if it saves data locally.

- The addon accepts and addresses security reports as soon as possible and implements necessary fixes in a timely manner, including previously released versions.

- The addon informs users about security issues as soon as is appropriate and if needed provides adequate instructions on how to resolve the problem locally.

## Licensing

- The addon has one or more fitting licenses and provides a copy of their text in the source when required by the license. See [Licensing] for the recommended licenses and how to apply them.

- The license is declared consistently everywhere it appears: the [manifest's `<license>` tag][ManifestLicense], the `LICENSE` file(s), and any per-file [SPDX] headers all agree. A license string that is not a recognized SPDX identifier may be normalized to the most restrictive match (for example, `LGPL2` becomes `LGPL-2.0`), so use exact SPDX identifiers.

## Codebase

- The addon's code is Python 3+ based.

- The addon's code uses the FreeCAD-provided Qt wrappers.

- The addon has a valid [manifest][Manifest] (`package.xml` file) that accurately describes it, including the correct [`<content>` type][ManifestContent], a [`<classname>`][ManifestClassname] matching its `InitGui` class for workbenches, and a [`<url>`][ManifestUrl] whose `branch` attribute matches the branch the manifest lives on.

- The addon confines its commands, toolbars, menus, and other side effects to its own workbench, and does not modify, hide, or otherwise interfere with FreeCAD's core interface or that of other addons.

- The addon avoids expensive work, network access, and other global side effects at import or startup time, deferring them until the user invokes the relevant command.

- The addon is compatible with the latest version of FreeCAD unless it's specifically designed to only be used with older versions, in which case it declares the supported range via [`<freecadmin>` / `<freecadmax>`][ManifestFreecadmin].

- The addon doesn't require dependencies unless they are functionally necessary, and every Python [dependency][ManifestDepend] it declares is on the package [allow list][AllowList].

- The addon only [vendors][Vendoring] dependencies when technically necessary and doesn't attempt to circumvent the package [allow list][AllowList].

## Best Practices

- The addon uses the modern, [namespaced `freecad/<ModName>/` layout][Structuring] and does not manipulate `sys.path` or rely on top-level module names that can collide with other addons. Use of the legacy Init.py/InitGui.py layout is permitted, but strongly discouraged. If the old layout is used, `sys.path` must not be manipulated by the addon.

- The addon is published from a stable branch rather than its active development branch. The recommended structure is a long-lived *release* branch that the Addon Index tracks, kept separate from a *development* branch used for day-to-day work; the development branch is merged into the release branch only when a new version is ready, and the [manifest `<version>`][ManifestVersion] and `<date>` are incremented each time the release branch changes. See [Updating an addon][Updating] for this and other release strategies.

<!----------------------------------------------------------------------------->

[Licensing]:          ../../Licensing
[Updating]:           ../../../Guides/Maintaining/Updating
[Structuring]:        ../../Structuring
[ManifestVersion]:    ../../Structuring/Manifest#version
[Manifest]:           ../../Structuring/Manifest
[ManifestLicense]:    ../../Structuring/Manifest#license
[ManifestContent]:    ../../Structuring/Manifest#content
[ManifestClassname]:  ../../Structuring/Manifest#classname
[ManifestUrl]:        ../../Structuring/Manifest#url
[ManifestDepend]:     ../../Structuring/Manifest#depend
[ManifestFreecadmin]: ../../Structuring/Manifest#freecadmin
[AllowList]:          ../../Dependencies/Allow-List
[Vendoring]:          ../../Dependencies/Vendoring
[SPDX]:               https://spdx.org/licenses/
