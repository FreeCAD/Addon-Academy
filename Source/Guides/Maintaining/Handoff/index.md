---
layout : Default
---

# Maintainer handoff

Addons usually outlast the original maintainer's interest in them. This page covers the orderly steps to either transfer maintenance to a new person or mark the addon as orphaned in a way the ecosystem can detect and handle.

The [quality requirements][Qualities] for inclusion in the Addon Index require an addon to have "at least one active maintainer or [be] in the process of finding a new maintainer." Once an addon stops meeting that bar without an attempted handoff, the FreeCAD addons team may remove it from the Index. The procedures here are how to avoid that outcome.


## Recognizing that handoff is needed

Common signals that an addon needs a handoff or orphaning:

-   The current maintainer is no longer responding to issues, pull requests, or security advisories.
-   The maintainer no longer uses FreeCAD or the addon's domain.
-   Significant compatibility breakage with a recent FreeCAD release that the maintainer cannot or will not address.
-   The maintainer plans to stop, and is announcing the change in advance (the easiest case to handle).

Acting early, before the addon is broken on current FreeCAD, makes every later step easier.


## Three outcomes to plan for

Roughly in order of preference:

1.  **Transfer to an active new maintainer.** The addon continues development under new ownership.
2.  **Form a maintainer team.** Multiple people share commit and release rights, reducing single-point-of-failure risk.
3.  **Mark as orphaned.** No active maintainer, but the addon is left in place for users who need it. Other contributors may eventually pick it up.

Each path has different mechanics.


## Transferring to a new maintainer

The mechanics are largely the responsibility of the git host (GitHub, Codeberg, GitLab), but there are addon-specific steps:

1.  **Find the new maintainer.** Reach out via the FreeCAD forum, the addon's existing user community, recent contributors to the repository, or the FreeCAD addons team.
2.  **Hand off repository ownership.** Either transfer the repository to the new maintainer's account, or add them as an owner with full administrative rights. GitHub's "Transfer ownership" feature handles the URL redirect automatically.
3.  **Update the [Manifest][Manifest].** In `package.xml`:
    -   Update `<maintainer>` to the new maintainer's name and email.
    -   If the repository moved, update `<url type="repository">`.
    -   Optionally add the previous maintainer as `<author>` to preserve attribution.
4.  **Update the Addon Index.** If the repository URL changed, the entry in the [Addon Index][AddonIndex] needs updating. Open an issue or PR there.
5.  **Coordinate Crowdin access.** If the addon is in the freecad-addons Crowdin project, transfer manager rights to the new maintainer or coordinate with the FreeCAD i18n team.
6.  **Announce to users.** A note in the addon's `CHANGELOG.md` and `README.md` is the conventional channel. Users who have the addon installed will see the changelog through the Addon Manager.

Worked example of the manifest change:

```xml
<!-- Before -->
<maintainer email="oldmaintainer@example.com">Old Maintainer</maintainer>

<!-- After -->
<maintainer email="newmaintainer@example.com">New Maintainer</maintainer>
<author email="oldmaintainer@example.com">Old Maintainer</author>
```


## Forming a maintainer team

When more than one person can make releases, the addon survives any single contributor stepping back. The mechanics:

-   On the git host, add the additional maintainers with sufficient rights to merge PRs and tag releases.
-   In the manifest, list every active maintainer with a `<maintainer>` element. The manifest accepts multiple `<maintainer>` tags.
-   Document who handles what (review, releases, translations) somewhere in the repository, so a new contributor knows whom to contact.

Multi-maintainer addons are more resilient but require coordination overhead. They tend to work best for addons with a meaningful contributor community already in place.


## Marking an addon as orphaned

When no successor is available and the addon is still useful enough to leave in place, mark it as orphaned in the manifest. The convention is documented in the [Manifest][Manifest]:

```xml
<maintainer email="no-one@freecad.org">No current maintainer</maintainer>
```

This is a recognized signal to the Addon Manager and to other contributors that the addon is looking for a new owner. Combine it with:

-   A note at the top of the `README.md` stating that the addon is unmaintained and seeking a new maintainer.
-   A pinned issue on the repository's issue tracker with the same message.
-   An entry in the `CHANGELOG.md` recording when and why the addon was orphaned.

An orphaned addon may still receive community pull requests; if any contributor steps forward as a willing maintainer, the orphaned-marker convention is intended to facilitate that handoff rather than to be a permanent state.


## Removal from the Addon Index

If the addon is broken on current FreeCAD and no maintainer is forthcoming, removal from the Addon Index is the eventual outcome. Removed addons are listed in the [Removed Addons][Removed] page so future authors can pick up the work. Users who already have an installed copy can keep using it; new users simply will not discover it.

Removal is not deletion of the repository: the source remains available, and a future maintainer can request reinstatement after fixing the issues that led to removal.


## See also

-   [Manifest: `<maintainer>`][ManifestMaintainer]: the syntax for declaring maintainers, including the orphaned-addon convention.
-   [Quality requirements for indexed addons][Qualities]: the rules an indexed addon must meet, including maintainer presence.
-   [Removed Addons][Removed]: addons previously removed from the Index.


[Manifest]: ../../../Topics/Structuring/Manifest
[ManifestMaintainer]: ../../../Topics/Structuring/Manifest#maintainer
[Qualities]: ../../../Topics/Addon-Index/Index/Qualities
[Removed]: ../../../Topics/Addon-Index/Removed
[AddonIndex]: https://github.com/FreeCAD/Addons
