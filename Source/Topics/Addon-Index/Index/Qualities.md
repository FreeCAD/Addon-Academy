---
layout : Default
---

# Qualities

In order to be included in the FreeCAD Addon Index, an addon must comply with a minimum set of quality requirements.

## Governance

- The addon has at least one active maintainer or is in the process of finding a new maintainer.

- The addon maintainers address user concerns such as open issues, pull requests, and security advisories in a timely manner.

- The addon's repository and overall codebase must be at least 30 days old.

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

- The addon only [vendors][Vendoring] dependencies when technically necessary and doesn't attempt to circumvent the package [allow list][AllowList]. Vendoring is **strongly** discouraged and is grounds for rejection from the Index.

- The addon is substantially complete: "pre-alpha" and "alpha"-level code is not suitable for inclusion in the Index. The addon's main documentation page should be clear which features a user should expect to work and which should not.

- Addons in the Index are periodically scanned using [Bandit](https://bandit.readthedocs.io/) and the results posted publicly at https://freecad.github.io/Addon-Reports/ -- addon authors are encouraged to address the issues in that report.

## AI Agents

These requirements apply in addition to those above when an addon lets an AI model generate code or commands that run inside FreeCAD, whether the addon runs the agent itself or exposes FreeCAD to an outside agent, for example through an MCP server (a *bridge*). The package [allow list][AllowList] still applies: an addon may not install Python packages itself, into FreeCAD's environment or any other. A separate program that the user installs, such as an MCP server set up with `pip` or `uv`, may manage its own environment.

- **Show the code, then wait for approval.** The user sees the complete code before it runs, and only the code the user approved runs, exactly as shown (for code from a file, the contents that were shown, not a fresh read). An addon that runs the agent itself shows this approval inside FreeCAD. Tools that read or write files at paths the model chooses also need approval; fixed operations on the document with values supplied by the model don't. Documents and other data the model reads can contain instructions planted by a third party, so this review is the user's main protection.

- **Automatic approval is opt-in.** It may only be a setting, off by default, that warns in the interface itself (not just in a tooltip or the documentation) that the model's code will run with the user's full permissions. An addon that launches or configures an agent must not set it to approve code execution or file tools automatically; setting it to deny them is fine.

- **Bridges keep the agent's approval prompt.** For a bridge, the agent's own approval prompt is the approval step, and the bridge must not weaken it: no agent configuration that approves its tools automatically, no tool descriptions telling the agent to skip asking, and no tool that runs code from a file unless FreeCAD shows the file's contents first. When started, the bridge warns inside FreeCAD that connected agents can run code with the user's full permissions.

- **Ask before sending anything.** Before any request reaches a remote AI service, even one that only lists models, the addon asks for consent inside FreeCAD; a notice in the README is not enough. The request names the service and every kind of data sent, including anything sent automatically (for example prompts, object names and dimensions, file paths, file contents, screenshots, and error output). Consent is per service and is asked again when the service or the kinds of data change.

- **No default service.** No remote AI service is selected by default, and the addon doesn't use API keys or logins it finds on the system, such as environment variables or another program's saved login, until the user has consented to that service. An addon built around one vendor's tool may then use the user's existing login for it.

- **Listeners always require authentication.** Network listeners that let an agent reach FreeCAD, including any MCP server or similar program the addon ships, start with FreeCAD only if the user has enabled that, and require authentication on every request after the handshake, with no way to turn it off. HTTP listeners reject browser requests, for example any with an `Origin` header or a `Host` header that doesn't match the configured address; other listeners close the connection on any input outside their protocol.

- **Loopback by default; remote access only with safeguards.** Listeners bind to the loopback interface by default. Remote access is best done without changing that, through an SSH tunnel or by starting the MCP server on the remote machine over SSH. An addon may offer to listen on another address only if:
  - the setting is off by default, and before the listener starts on each new address, FreeCAD warns that anyone who can reach and authenticate to it can run code with the user's full permissions, and the user accepts;
  - the address is a specific one the user chose, never a wildcard such as `0.0.0.0` or `::`;
  - traffic is always encrypted, using Python's `ssl` module or another maintained library rather than the addon's own code, and the client verifies the server, for example with a pinned certificate or a pre-shared key (TLS-PSK); an unchecked self-signed certificate does not count;
  - clients the addon doesn't control, such as an agent's MCP client or a chat front end, can also verify the server, and the addon explains where the setting is turned on how to set that up, never suggesting that verification be turned off.

- **Agent files stay private.** Tokens, pairing secrets, and files the addon writes for the agent (configuration, instructions, working directories, screenshots) are readable only by the current user and never placed in shared temporary directories.

- **Credentials go in secure storage**, where the system provides it (see [Compliance](#compliance)).

- **No implied endorsement.** The addon's name, icon, and description don't suggest it is an official product of the AI vendor or of FreeCAD; descriptive names such as "for Claude Code" or "Gemini connector" are fine.

- **Existing addons have 60 days.** Addons already in the Index when these requirements were introduced have 60 days from when their maintainers are notified to comply, after which they may be removed.

## Best Practices

- The addon uses the modern, [namespaced `freecad/<ModName>/` layout][Structuring] and does not manipulate `sys.path` or rely on top-level module names that can collide with other addons. Use of the legacy Init.py/InitGui.py layout is permitted, but strongly discouraged. If the old layout is used, `sys.path` must not be manipulated by the addon.

- The addon is published from a stable branch rather than its active development branch. The recommended structure is a long-lived *release* branch that the Addon Index tracks, kept separate from a *development* branch used for day-to-day work; the development branch is merged into the release branch only when a new version is ready, and the [manifest `<version>`][ManifestVersion] and `<date>` are incremented each time the release branch changes. See [Updating an addon][Updating] for this and other release strategies.

- An addon that runs model-generated code wraps each approved run in a single undo transaction, so the user can revert it in one step.

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
