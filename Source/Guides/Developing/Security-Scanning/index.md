---
layout : Default
---

# Security scanning with Bandit

[Bandit][Bandit] is a static analyzer that reads Python source and reports code patterns that are commonly involved in security problems: shelling out with user-controlled strings, parsing untrusted XML with the standard library, `exec` and `eval`, unsafe deserialization, and so on. It does not run your code, and it does not know what your addon *means* to do, so its output is a list of places to look rather than a list of bugs. That still makes it valuable: most of the findings are quick to fix, and the remainder become documented, deliberate decisions instead of accidents.

Bandit is also the security check used by the FreeCAD [Addon Report][AddonReports], a monthly quality report generated for every addon in the [Addon Index][AddonIndex]. Running the same scan yourself, with the same settings, means nothing in that report will surprise you.


## Running Bandit locally

Bandit is an ordinary Python package. Install it outside of FreeCAD's Python, in whatever environment you use for development tooling.

Using `pip`, that looks like:
```
pip install bandit
```

Or using `uv`:
```
uv tool install bandit
```

Then run it over your addon's source tree, starting from the repository root:

```
bandit -r .
```

Each finding is printed with a test ID, a severity, a confidence, a link to the documentation for that check, and the offending lines:

```
>> Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.9.4/plugins/b603_subprocess_without_shell_equals_true.html
   Location: ./freecad/Midvale/tools.py:188:8
187	    try:
188	        subprocess.run(
189	            [
190	                "lrelease",
```

### Severity and confidence

Every finding has two independent ratings. **Severity** (Low, Medium, High) is how bad the problem would be if it is real. **Confidence** (Low, Medium, High) is how sure Bandit is that the pattern it matched is actually the problematic one. A `shell=True` call is High/High: it is certainly a shell invocation and shell injection is serious. A bare `import subprocess` is Low/High: Bandit is certain you imported it, and importing it is not itself a problem.

The Addon Report converts severity into a score penalty, so High findings cost far more than Low ones:

| Severity | Penalty per finding |
|----------|---------------------|
| High     | 3 points            |
| Medium   | 1 point             |
| Low      | 0.1 point           |

You can filter the local output with `-l` (Low and up, the default), `-ll` (Medium and up), or `-lll` (High only), and similarly `-i`, `-ii`, `-iii` for confidence. Filtering is useful for triage, but the goal should be a clean run at the default level. See the section below on how to address findings, including false-positives and "that's a dumb thing to flag"-type issues.

### Configuration file

Rather than remembering command-line flags, put the settings in a `bandit.yaml` at the root of your repository and pass it with `-c`:

```
bandit -c bandit.yaml -r .
```

The Addon Report uses this configuration, so matching it exactly gives you the same results the report will see:

```yaml
# Configuration for Bandit static security analysis. Run locally with:
#   bandit -c bandit.yaml -r .

exclude_dirs:
  - "*/.venv/*"

skips:
  - B101   # assert_used
  - B110   # try_except_pass
```

`exclude_dirs` keeps Bandit out of directories that are not your code (though note that the Addons Report doesn't know anything about these, so if you've chosen to vendor some library with a zillion warnings, those are going to show up in your score. Pro Tip: don't vendor.). Each entry is matched as a glob against the *full* path of every file, so anchor the pattern with path separators: a bare `CatalogCache` would also match a file named `CatalogCacheCreator.py`. Add entries for any vendored dependencies or generated output in your tree.

`skips` disables a test everywhere in the project. B101 (`assert` statements) and B110 (`try`/`except`/`pass`) are stylistic checks rather than security defects, and the report skips them too. Resist the temptation to add anything else here: a skipped test cannot catch a real problem introduced later, and just because *you* skip it doesn't mean the Addons Report does. If you want to match the report, leave just the two shown here. Per-line suppression, described below, is almost always the right tool instead.

Bandit also accepts a `[tool.bandit]` table in `pyproject.toml` (install `bandit[toml]`) or a `.bandit` INI file, but a YAML file is the simplest option and is what the rest of this page assumes.


## Running Bandit as a pre-commit hook

[pre-commit][PreCommit] runs checks against the files in each commit before the commit is created. Bandit ships a hook definition, so adding it to your `.pre-commit-config.yaml` is a few lines:

```yaml
repos:
    -   repo : https://github.com/PyCQA/bandit
        rev : 1.9.4
        hooks:
            -   id : bandit
                args : [ '-c', 'bandit.yaml' ]
```

Pin `rev` to a release tag, and let `pre-commit autoupdate` bump it. Pre-commit passes the staged Python files to Bandit as explicit targets, so `-r` is not needed and `exclude_dirs` in the config file has no effect here; use pre-commit's own `exclude:` pattern on the hook if you need to keep files out.

After adding the hook, your addon's contributors run `pre-commit install` once per clone, and the scan runs on every commit from then on. You can also run it against the whole repository on demand:

```
pre-commit run bandit --all-files
```

Note that `pre-commit run --all-files` is what pre-commit.ci and most CI configurations execute, so the Bandit hook covers the whole tree there even though it only checks changed files locally.


## Running Bandit in CI

A dedicated GitHub Actions workflow keeps the security scan visible as its own check on every pull request, independent of your unit tests. Save this as `.github/workflows/bandit.yml`, adjusting the branch names to match your repository:

```yaml
name: Bandit security scan

permissions:
  contents: read

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  bandit:
    name: Bandit
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install Bandit
        run: |
          python -m pip install --upgrade pip
          pip install bandit

      - name: Run Bandit
        run: bandit -c bandit.yaml -r .
```

The job fails whenever Bandit reports a finding. That is the behavior you want: a finding must either be fixed or deliberately suppressed before the pull request merges. If you are adding Bandit to an existing addon with a backlog of findings and cannot clear them all at once, `--exit-zero` makes the step advisory until you are ready to enforce it. Do not leave it that way for long, since an advisory check is quickly ignored.

If your addon already has a workflow that runs `pre-commit run --all-files`, the hook from the previous section is exercised there and a separate workflow is optional. A separate job still has one advantage: the finding appears under its own name in the pull request checks, where reviewers are more likely to read it.


## Suppressing a finding with `nosec`

When a finding is a false positive, or the flagged pattern is safe in context, add a `# nosec 1234` comment on the line it reported. The line that matters is the one in the `Location:` field. For a call that spans several lines, that is the line containing the opening of the call, e.g.

```python
subprocess.run(  # nosec B603 B607
    ["lrelease", ts_path],
    timeout=5,
)
```

Follow these guidelines for every suppression:

-   **Always name the test IDs.** A bare `# nosec` silences every check on that line, including ones that do not exist yet. `# nosec B603 B607` silences exactly the two findings you audited and nothing else. Multiple IDs are separated by spaces or commas.

-   **Tell humans why it is safe.** The `nosec` comment tells Bandit to be quiet; a second comment tells the *next developer* (probably your future self) why that was the case. You won't remember, trust me. The convention used by FreeCAD's addons is an `Audited:` comment that ends by listing the IDs added:

    ```python
    # Audited: fixed arguments, no shell; lrelease is expected on PATH (added nosec B603, B607)
    subprocess.run(  # nosec B603 B607
        ["lrelease", ts_path],
        timeout=5,
    )
    ```

    Leaving that line out just leaves a strange mystery for the next developer to track down. And remember, the next developer is probably you!

-   **Suppress narrowly, fix exapansively.** If a finding is a real problem, fix the code. Reserve `nosec` for patterns that are safe *because of the surrounding code*, and describe that surrounding code in the audit comment so that a later change to it prompts a re-check.

Note that Bandit's summary reports how many lines were skipped and how many findings were suppressed by specific IDs, so suppressions never disappear entirely from view. Running with `--ignore-nosec` lists every suppressed finding, which is a useful periodic audit of the audits. While right now the Addons Report does not employ this, it may do so in the future to help catch developers trying to "game the system." Please, take care of your users: fix the problems, don't just hide them.


## Resolving common findings

The checks below account for nearly all findings in FreeCAD addons, so they are documented here so you don't have to develop the appropriate remediation yourself. For each, the preferred fix comes first, and the audited `nosec` pattern is the fallback for cases where the code is correct as written.

### Subprocess and shell commands: B404, B602, B603, B605, B606, B607

Addons frequently launch external tools: Qt's `lrelease`, a slicer, `git`, or the system's file opener. Bandit reports every step of that.

**`import subprocess` (B404, Low).** Bandit warns on the import so you remember to audit each use. Once the call sites are audited (but not until then!), suppress the import with a comment that summarizes the policy:

```python
# Audited: subprocess calls use fixed argument lists and no shell (added nosec B404)
import subprocess  # nosec B404
```

Of course, this can become stale over time, but it's useful as a first pass while you're getting started with Bandit.

**`shell=True` or `os.system` (B602, B605, High).** These are the ones to actually fix. Passing a string to a shell means every space, quote, semicolon, and `$` in that string is interpreted, so any part of it that came from a filename, a preference, or a user is a potential injection. Replace the string with an argument list and drop `shell=True`:

```python
# Before
os.system("lrelease " + ts_path)
subprocess.run(f"lrelease {ts_path}", shell=True)

# After
subprocess.run(["lrelease", ts_path], timeout=5)
```

With a list, `ts_path` is delivered to the program as a single argument no matter what characters it contains. Shell features like pipes and globbing are lost, but those are almost never needed from an addon and can be reproduced in Python when they are.

**Subprocess without a shell (B603, Low).** This fires on every `subprocess.run`, `Popen`, or `check_output` call, even the safe ones, because Bandit cannot see where the arguments come from. First, audit it: confirm the arguments are either literals or values you control. Only after auditing, suppress with a comment that says so. If any argument is user input, validate it first (for example, check that a path resolves inside the directory you expect).

**Partial executable path (B607, Low).** Starting `["lrelease", ...]` rather than `["/usr/bin/lrelease", ...]` means the program is found via `PATH`, and a malicious directory earlier in `PATH` could substitute its own `lrelease`. For a developer tool run by the developer, this is an accepted risk; document that and suppress. For a program run on the user's machine, consider resolving it once with `shutil.which()` and failing clearly when it is not found, which also gives you a better error message than a `FileNotFoundError` from deep inside `subprocess`.

**`os.startfile` (B606, Low).** Windows-only; opens a file with its associated application. Bandit rates this Low/Medium. It is safe when the path is one your addon created or the user just chose. Audit and suppress.

A fully audited helper looks like this:

```python
# Audited: subprocess calls use fixed argument lists and no shell (added nosec B404)
import subprocess  # nosec B404


def open_in_editor(path: str) -> None:
    """Open `path` in the platform's default text editor."""
    # Audited: `path` is a file this addon just wrote; fixed arguments, no shell
    # (added nosec B606, B603, B607)
    if platform.system() == "Windows":
        os.startfile(path, "edit")  # nosec B606
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", "-t", path])  # nosec B603 B607
    else:
        subprocess.Popen(["xdg-open", path])  # nosec B603 B607
```

### Opening URLs: B310, B113

**`urllib.request.urlopen` (B310, Medium).** `urlopen` accepts `file://` and other schemes as well as `http(s)://`. If the URL is built from anything other than a hardcoded constant, a caller could point it at a local file. The fix is to check the scheme before opening, then suppress with a comment pointing at the check:

```python
download_url = response["url"]
if not download_url.startswith("https://"):
    raise ValueError(f"Refusing to download from non-HTTPS URL {download_url}")
# Audited: only HTTPS URLs reach this point (added nosec B310)
urlretrieve(download_url, filename)  # nosec B310
```

When the URL is a literal `https://...` string, the check is unnecessary and the audit comment can simply say the URL is hardcoded.

**`requests` without a timeout (B113, Medium).** If you use the [`requests`][Requests] package Bandit does not report B310, but it *does* insist on a `timeout=` argument, because a hung connection otherwise blocks FreeCAD's GUI thread forever. Always pass one. For GUI code, prefer Qt's `QNetworkAccessManager` or a worker thread over *any* blocking network call, even one with a timeout.

### XML parsing: B405, B314 and friends

FreeCAD addons parse XML often: `package.xml` manifests, Qt `.ui` files, SVG icons, exported data. The standard library's `xml.etree.ElementTree`, `xml.dom.minidom`, and `xml.sax` are all vulnerable to entity-expansion attacks ("billion laughs") when given hostile input. Bandit flags the import (B405, B406, B408, ...) and each parse call (B313 through B320).

The fix is to parse with [defusedxml][DefusedXML], which wraps the standard parsers with the dangerous features disabled and is on the [allow-list][AllowList], so you can declare it as a dependency:

```python
# Before
import xml.etree.ElementTree as ET
root = ET.fromstring(data)

# After
import defusedxml.ElementTree as ET
root = ET.fromstring(data)
```

The class and function names are the same, so the change is usually just the import. One possible "gotcha": exception classes are not re-exported by every defusedxml module, so you may still need one standard-library import for `except ParseError:`. That import only warns on B405 and is a legitimate suppression:

```python
# Audited: only the exception class is imported; all parsing is done by defusedxml (added nosec B405)
from xml.etree.ElementTree import ParseError  # nosec B405
```

### `exec` and `eval`: B102, B307

Executing strings as code is High or Medium severity depending on the form, and there is rarely a good reason for it. The common cases and their replacements:

-   Parsing a literal from a string: use `ast.literal_eval`, which evaluates only Python literals and cannot call functions.
-   Reading a config or data file: use `json`, or `configparser`, or `tomllib`.
-   Building a name dynamically: use `getattr`, a dictionary of callables, or `importlib.import_module`.

The one legitimate FreeCAD case is deliberately running a macro or script *at the user's explicit request*, for example an uninstall script an addon provides. Even then, put the action behind a confirmation dialog and document that in the audit comment:

```python
# This use of exec() is behind an explicit user opt-in dialog (added nosec B102)
exec(f.read())  # nosec B102
```

Never, ever, **ever** run `eval()` on something you read in from a user-controlled file, including (especially!!) an `FCStd` file. An attacker could provide an innocent-looking FreeCAD file that your addon then executes arbitrary code when loading. This can do literally anything that user's permission level allows. Never, ever do this.

### Deserialization: B301, B403, B506

**`pickle` (B301, B403).** A pickle file can execute arbitrary code when loaded, so loading one from disk means trusting whoever wrote that file. Store addon state as JSON instead, or in FreeCAD's parameter system. If you inherit pickle usage from older code, migrate the on-disk format rather than suppressing.

**`yaml.load` (B506).** Without an explicit safe loader, PyYAML can instantiate arbitrary Python objects. Replace `yaml.load(data)` with `yaml.safe_load(data)`. There is no reason to suppress this one: just fix it.

### Hashing and randomness: B324, B311

**Weak hash (B324, High).** `hashlib.md5()` and `hashlib.sha1()` are flagged because they are unsuitable for anything security-related. Addons rarely use them that way: the typical purpose is a cache key or a change detector. Tell both Bandit and the reader that by passing `usedforsecurity=False`, which also clears the finding:

```python
digest = hashlib.md5(data, usedforsecurity=False).hexdigest()
```

**`random` (B311, Low).** The `random` module is not cryptographically secure. If you are generating tokens, IDs that must be unguessable, or anything an attacker would benefit from predicting, use `secrets` instead. For jitter, sample data, or picking a placeholder color, `random` is fine (and probably the right choice); audit, then suppress.

### Temporary files: B108

Hardcoding `/tmp/something` (B108) is both a security problem (another user can pre-create the file) and a portability problem (Windows has no `/tmp`). Use `tempfile.mkdtemp()` or `tempfile.NamedTemporaryFile()`, which create unique, correctly permissioned paths on every platform.

### Hardcoded passwords: B105, B106, B107

Bandit guesses that any string assigned to a variable or parameter whose name contains "password", "token", "secret", or similar is a hardcoded credential. It is right often enough to be worth keeping, and wrong often enough that you will see it on code like `password = ""` or `def connect(host, token=None)`. When it is a false positive, the audit comment is trivially short. When it is *not* a false positive, remove the secret from the source, rotate it, and read it from the environment or the user's system keyring at runtime.

### Style checks: B101, B110, B112

`assert` (B101), `try`/`except`/`pass` (B110), and `try`/`except`/`continue` (B112) are not security defects, and the Addon Report skips B101 and B110 entirely. If you enable them anyway, the usual fixes are to replace `assert` with an explicit `if`/`raise` in non-test code (asserts are stripped under `python -O`), and to at least log something in an `except` block rather than discarding the exception silently. See [Logging & console][Logging] for how to do that in FreeCAD.


## Putting it together

A reasonable order of operations for an existing addon:

1.  Add `bandit.yaml` with the report's settings and run `bandit -c bandit.yaml -r .` locally.
2.  Fix every High finding. These are almost always `shell=True`, `os.system`, or a weak hash, and the fixes are simple and documented above.
3.  Over time, go through the Medium and Low findings, fixing the code where a real fix exists and adding audited `nosec` markers where it doesn't.
4.  Consider adding the CI workflow so the report stays clear going forward.
5.  Consider adding a pre-commit hook so developers see findings before even opening a pull request.


<!----------------------------------------------------------------------------->

[Logging]:      ../../Code/Logging
[AllowList]:    ../../../Topics/Dependencies/Allow-List
[AddonIndex]:   ../../../Topics/Addon-Index

[Bandit]:       https://bandit.readthedocs.io/
[AddonReports]: https://freecad.github.io/Addon-Reports/
[PreCommit]:    https://pre-commit.com/
[DefusedXML]:   https://pypi.org/project/defusedxml/
[Requests]:     https://requests.readthedocs.io/
