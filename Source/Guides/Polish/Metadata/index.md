---
layout : Default
---

# Metadata & discoverability

Your Manifest file contains metadata about your addon intended for use by the Addon Manager and by FreeCAD itself. See the [Manifest] documentation for complete details: this page is focused on creating the best possible user-facing metadata, including how to craft a good description, how to select the right tags, etc.

## Name

The `<name>` and `<description>` tags are your first point of communication with your users. `<name>` is a human readable name for your addon, displayed in the Addon Manager and in the list of installed addons inside FreeCAD. As such, it *should not* contain the word "FreeCAD"---your users are reading it from within FreeCAD itself already, it's clear that "Thing Creator 9000" is really "(FreeCAD) Thing Creator 9000". Also, it's generally not necessary to include the word "Workbench", that's a bit of technical detail that your users probably don't care about. If they really care, they can tell the Addon Manager to *only* display Workbenches, in which case your Workbench will be displayed as long as it used the `<workbench>` content item.

## Description

The description is a little more challenging, because the Addon Manager has three different view modes, each of which show differing amount of the description. First, the `<description>` tag can *only* contain text, and it is *never* parsed. So no markdown, html, etc. Second, in some view modes readers will only see the first few words of this description, so keep the first sentence very brief and focused. As with the `<name>` tag, there's no reason at all to include the word "FreeCAD" here (what if your users are actually running [AstoCAD] or [LinkStage3]?). Second, avoid the temptation to start with "This is an addon that...". They already know it's an addon, it's being displayed in the Addon Manager right now, that's where this text is shown. Those twenty characters are better spent saying what it does: "Adds a toolbar with buttons that destroy your model". Hopefully not *literally* that, of course.

Once you're past the first sentence you have more flexibility. The addon manager truncates the display to a very small amount of text in "Combined" and "Compact" modes, but in "Details" mode it displays all of your "description" text. It's not a good practice to have more than a couple hundred words here, users will be annoyed at you occupying so much screen real estate, but the Addon Manager won't prevent you from doing so. The team reviewing your addon might ask you to shorten it up a bit, though. Remember your primary location for telling users about your addon is in your [Overview] file.

## Tags

`<tag>` elements help users find your addon when searching or browsing the Addon Manager. Each tag is a single string, and an addon can declare as many as it wants. There is no fixed vocabulary; the ecosystem has converged on a small set of conventions through use.

The most common tags currently in the catalog fall into a few categories:

-   **Domain or discipline:** `assembly`, `fem`, `cam`, `sheetmetal`, `drafting`, `mesh`, `beam`, `fea`, `parametric`, `nurbs`.
-   **Type of addon:** `theme`, `stylesheet`, `library`, `extension`, `workbench`.
-   **Function:** `import`, `solver`, `plot`, `search`, `scripting`.
-   **Visual style** (for theme-type addons specifically): `dark`, `light`.

Multiple `<tag>` elements stack:

```xml
<tag>assembly</tag>
<tag>parametric</tag>
<tag>solver</tag>
```

Practical guidance:

-   **Pick words a user would actually search for.** Names that only mean something inside your project (a project codename, your username) will never appear in a real search. Domain and function words will.
-   **Use established terms when they exist.** Tagging your addon `fem` rather than `finite-element-method` places it next to the other addons in that space, where users browsing by tag can find it.
-   **Use lowercase.** The tag system is broadly case-insensitive in practice, but real addons mostly use lowercase, and that is what most filter UIs display.
-   **Keep the count reasonable.** Three to seven tags covers almost every addon. Longer lists dilute the signal of any individual tag.
-   **Skip noise.** Year numbers (`2024`), status markers (`beta`, `wip`), your own name, and made-up words add nothing to discoverability and clutter the shared tag pool.

## More? 

**Planned scope:**

-   Writing a searchable, concise, user-facing `<description>`.
-   Choosing `<tag>` values that match how users search.
-   Screenshot conventions in the README vs the overview page.
-   GitHub repository topics (`freecad`, `addon`, workbench-specific).

[Overview]: ../Overview-Page

[Manifest]: ../../../Topics/Structuring/Manifest
[AstoCAD]: https://astocad.com
[LinkStage3]: https://github.com/realthunder/FreeCAD