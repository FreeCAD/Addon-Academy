#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-2.1-or-later
# SPDX-FileNotice: Adapted for the FreeCAD Addon Academy.
# SPDX-FileNotice: Derived from FreeCAD Telemetry's run_translation_cycle.py,
# SPDX-FileNotice: which is itself derived from FreeCAD's updatecrowdin.py script.

################################################################################
#                                                                              #
#   © 2015 Yorik van Havre <yorik@uncreated.net>                               #
#   © 2021 Benjamin Nauck <benjamin@nauck.se>                                  #
#   © 2021 Mattias Pierre <github@mattiaspierre.com>                           #
#   © 2025 FreeCAD Project Association                                         #
#                                                                              #
#   This script is free software: you can redistribute it and/or modify        #
#   it under the terms of the GNU Lesser General Public License as             #
#   published by the Free Software Foundation, either version 2.1              #
#   of the License, or (at your option) any later version.                     #
#                                                                              #
#   This script is distributed in the hope that it will be useful,             #
#   but WITHOUT ANY WARRANTY; without even the implied warranty                #
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                    #
#   See the GNU Lesser General Public License for more details.                #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public           #
#   License along with this script. If not, see https://www.gnu.org/licenses   #
#                                                                              #
################################################################################

"""Run a full Crowdin translation cycle for a FreeCAD addon.

Workflow:
  1. Download the latest translations from Crowdin (triggering a new build if
     the last one is more than an hour old).
  2. For every language that meets MIN_TRANSLATION_THRESHOLD, copy the .ts
     file into the local translations folder and compile it to .qm via
     `lrelease`.
  3. Re-extract source strings from every .py and .ui file into the master
     .ts via `lupdate`.
  4. Upload the updated master .ts back to Crowdin.

Requirements:
  - `lupdate` and `lrelease` on PATH (Qt6 recommended).
  - A Crowdin API token with write access to the freecad-addons project,
    stored either in the CROWDIN_API_TOKEN environment variable or in
    ~/.crowdin-freecad-token.
  - This script is intended to be run from inside the addon's translations
    folder; it walks up the directory tree looking for package.xml to find
    the addon root.
"""

import collections
import datetime
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from functools import lru_cache
from urllib.parse import quote_plus
from urllib.request import Request, urlopen, urlretrieve


# =============================================================================
# CONFIGURATION — edit these constants for your addon
# =============================================================================

# The name of your addon as it appears on Crowdin.
CROWDIN_PROJECT_NAME = "YourAddon"

# The filename of your master .ts source file (typically <addon-name>.ts).
CROWDIN_FILE_NAME = f"{CROWDIN_PROJECT_NAME}.ts"

# Minimum translation ratio (0.0–1.0) a language must reach before a .qm
# file will be produced for it. This prevents shipping mostly-untranslated
# languages where users would see inconsistent mixes of their language
# and English.
MIN_TRANSLATION_THRESHOLD = 0.5

# Directories to skip when walking the source tree for .py/.ui files.
# Dot-directories (.git, .venv, etc.) are skipped automatically.
SKIP_DIRS = ["__pycache__", "build", "dist"]

# Crowdin project identifier. Rarely changes — stays "freecad-addons" for
# addons hosted on the shared FreeCAD addons Crowdin project.
CROWDIN_API_PROJECT_ID = "freecad-addons"

# Path to the local translations directory, relative to the script's cwd.
TS_FILE_PATH = os.curdir

# =============================================================================

CROWDIN_API_URL = "https://api.crowdin.com/api/v2"


class CrowdinUpdater:
    BASE_URL = CROWDIN_API_URL

    def __init__(self, token, project_identifier):
        self.token = token
        self.project_identifier = project_identifier
        self.multithread = False

    @lru_cache()
    def _get_project_id(self):
        url = f"{self.BASE_URL}/projects/"
        response = self._make_api_req(url)

        for project in [p["data"] for p in response]:
            if project["identifier"] == self.project_identifier:
                return project["id"]

        raise Exception("No project identifier found!")

    def _make_project_api_req(self, project_path, *args, **kwargs):
        url = f"{self.BASE_URL}/projects/{self._get_project_id()}{project_path}"
        return self._make_api_req(url=url, *args, **kwargs)

    def _make_api_req(self, url, extra_headers=None, method="GET", data=None):
        if extra_headers is None:
            extra_headers = {}
        headers = {"Authorization": "Bearer " + load_token(), **extra_headers}

        if type(data) is dict:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data).encode("utf-8")

        request = Request(url, headers=headers, method=method, data=data)
        request_result = urlopen(request)
        if request_result.getcode() >= 300:
            print(f"Failed to make API request {url}: return code {request_result.getcode()}")
            raise Exception("Failed to make API request")
        return json.loads(request_result.read())["data"]

    def _get_files_info(self):
        files = self._make_project_api_req("/files?limit=250")
        return {f["data"]["path"].strip("/"): str(f["data"]["id"]) for f in files}

    def _add_storage(self, filename, fp):
        response = self._make_api_req(
            f"{self.BASE_URL}/storages",
            data=fp,
            method="POST",
            extra_headers={
                "Crowdin-API-FileName": filename,
                "Content-Type": "application/octet-stream",
            },
        )
        return response["id"]

    def _update_file(self, ts_file, files_info):
        filename = quote_plus(ts_file)

        with open(os.path.join(TS_FILE_PATH, ts_file), "rb") as fp:
            storage_id = self._add_storage(filename, fp)

        if filename in files_info:
            file_id = files_info[filename]
            self._make_project_api_req(
                f"/files/{file_id}",
                method="PUT",
                data={
                    "storageId": storage_id,
                    "updateOption": "keep_translations_and_approvals",
                },
            )
            print(f"{filename} updated")
        else:
            self._make_project_api_req("/files", data={"storageId": storage_id, "name": filename})
            print(f"{filename} uploaded")

    def status(self):
        response = self._make_project_api_req("/languages/progress?limit=100")
        return [item["data"] for item in response]

    def download(self, build_id):
        filename = f"{self.project_identifier}.zip"
        response = self._make_project_api_req(f"/translations/builds/{build_id}/download")
        urlretrieve(response["url"], filename)
        print("download of " + filename + " complete")

    def build(self):
        self._make_project_api_req("/translations/builds", data={}, method="POST")

    def build_status(self):
        response = self._make_project_api_req("/translations/builds")
        return [item["data"] for item in response]

    def wait_for_build_completion(self):
        while True:
            status = self.build_status()
            still_running = False
            for builds in status:
                if builds["status"] == "inProgress":
                    still_running = True
            if not still_running:
                print("done.")
                return
            print(".", end="")
            time.sleep(10)

    def update(self, ts_files):
        files_info = self._get_files_info()
        for ts_file in ts_files:
            self._update_file(ts_file, files_info)


def load_token():
    """Return the Crowdin API token from CROWDIN_API_TOKEN or ~/.crowdin-freecad-token."""
    if os.environ.get("CROWDIN_API_TOKEN"):
        return os.environ.get("CROWDIN_API_TOKEN")
    config_file = os.path.expanduser("~") + os.sep + ".crowdin-freecad-token"
    if os.path.exists(config_file):
        with open(config_file) as file:
            return file.read().strip()
    return None


def process_single_translation_file(source_path: str, target_path: str):
    """Copy a single .ts into the target dir and compile its .qm."""
    basename = os.path.basename(source_path)
    new_path = os.path.join(target_path, basename)
    shutil.copyfile(source_path, new_path)

    print("Generating qm file for", basename, "...")
    try:
        subprocess.run(["lrelease", new_path], timeout=5)
    except Exception as e:
        print(e)
    new_qm = new_path[:-3] + ".qm"
    if not os.path.exists(new_qm):
        print("ERROR: failed to create " + new_qm + ", aborting")
        sys.exit()


temp_folder = tempfile.mkdtemp()


def apply_translations_for_language(language_file: str):
    """Process a single language file from the unzipped Crowdin download."""
    print(f"Processing {language_file}...")
    source_path = os.path.join(temp_folder, CROWDIN_PROJECT_NAME, language_file)
    target_path = os.path.abspath(TS_FILE_PATH)
    process_single_translation_file(source_path, target_path)


def get_language_percentage(language_file: str):
    """Return the fraction of strings that are translated in a .ts file."""
    if not os.path.exists(language_file):
        return 0
    source_counter = 0
    unfinished_counter = 0
    with open(language_file, "r", encoding="utf-8") as f:
        for line in f:
            if "<source>" in line:
                source_counter = source_counter + 1
            elif 'type="unfinished"' in line:
                unfinished_counter = unfinished_counter + 1
    if source_counter > 0:
        return (source_counter - unfinished_counter) / source_counter
    return 0


def rename_locale_to_two_letter_code():
    """Drop the country-code suffix from locale filenames where it's unambiguous.

    Crowdin names files like <CROWDIN_PROJECT_NAME>_<lang>-<country>.ts;
    FreeCAD's locale lookup typically uses just the language code. Where two
    countries share a language (e.g. pt-BR and pt-PT), the disambiguation is
    preserved; otherwise the country code is dropped.
    """
    base_path = os.path.join(temp_folder, CROWDIN_PROJECT_NAME)
    ts_files = sorted(os.listdir(base_path))

    prefix_len = len(CROWDIN_PROJECT_NAME) + 1
    suffix_len = len("-xx.ts")
    codes_only = [f[prefix_len:-suffix_len] for f in ts_files]
    codes_that_need_disambiguation = []
    locale_frequency = collections.Counter(codes_only)
    for code in codes_only:
        if code not in codes_that_need_disambiguation and locale_frequency[code] > 1:
            codes_that_need_disambiguation.append(code)

    for ts_file in ts_files:
        code = ts_file[prefix_len:-suffix_len]
        if code not in codes_that_need_disambiguation:
            new_name = CROWDIN_PROJECT_NAME + "_" + code + ".ts"
            os.rename(os.path.join(base_path, ts_file), os.path.join(base_path, new_name))


def apply_all_available_translations():
    """Process every language file in the Crowdin zip that meets the threshold."""
    base_path = os.path.join(temp_folder, CROWDIN_PROJECT_NAME)
    for language_file in os.listdir(base_path):
        percentage = get_language_percentage(os.path.join(base_path, language_file))
        if percentage >= MIN_TRANSLATION_THRESHOLD:
            apply_translations_for_language(language_file)
        else:
            print(
                "Skipping {} because it is not translated enough ({} %)".format(
                    language_file, round(100 * percentage, 0)
                )
            )


def run_and_download_build(crowdin_updater: CrowdinUpdater):
    """Trigger a Crowdin build if needed, then download the latest translations."""
    build_status = crowdin_updater.build_status()
    last_build_id = None
    last_build_date = None
    for build in build_status:
        if build["status"] == "finished":
            build_id = build["id"]
            build_date = datetime.datetime.fromisoformat(build["finishedAt"])
            if last_build_id is None or last_build_date is None or build_date > last_build_date:
                last_build_id = build_id
                last_build_date = build_date

    if last_build_date is None or datetime.datetime.now(
        tz=datetime.timezone.utc
    ) - last_build_date > datetime.timedelta(hours=1):
        print("Last build was not in the last hour: running a new build", end="")
        crowdin_updater.build()
        crowdin_updater.wait_for_build_completion()

        print("Build complete, waiting ten seconds for translations to be ready...")
        time.sleep(10)

    print(f"Downloading latest translations (build ID {last_build_id})...")
    crowdin_updater.download(last_build_id)


def find_addon_root(starting_path: str) -> str:
    """Walk up from starting_path to find the directory containing package.xml."""
    current = os.path.abspath(starting_path)
    while True:
        if os.path.exists(os.path.join(current, "package.xml")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            print("ERROR: no package.xml found in any parent directory", file=sys.stderr)
            sys.exit(1)
        current = parent


if __name__ == "__main__":
    token = load_token()
    if not token:
        print("ERROR: no API token found, aborting")
        sys.exit(1)

    crowdin = CrowdinUpdater(token, CROWDIN_API_PROJECT_ID)

    # First half of the cycle: download and apply existing translations.
    run_and_download_build(crowdin)
    shutil.unpack_archive(f"{CROWDIN_API_PROJECT_ID}.zip", temp_folder)
    rename_locale_to_two_letter_code()
    apply_all_available_translations()

    # Second half: gather new source strings and send them to Crowdin.
    toplevel_path = find_addon_root(TS_FILE_PATH)

    files_to_translate = []
    for root, dirs, files in os.walk(toplevel_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]
        files = [f for f in files if not f.startswith(".")]
        for file in files:
            if file.endswith(".py") or file.endswith(".ui"):
                files_to_translate.append(os.path.abspath(os.path.join(root, file)))

    list_file = os.path.join(temp_folder, "files_to_extract.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for file in files_to_translate:
            f.write(file + "\n")

    print("Running lupdate to generate new translation files...")
    args = [
        "lupdate",
        "-no-obsolete",
        "-no-ui-lines",
        "-locations",
        "relative",
        f"@{list_file}",
        "-ts",
        os.path.join(TS_FILE_PATH, CROWDIN_FILE_NAME),
    ]
    result = subprocess.run(
        args,
        timeout=30,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout.decode("utf-8"))

    print("Sending new translation file to Crowdin...")
    crowdin.update([CROWDIN_FILE_NAME])

    def try_harder(func, path, _exc_info):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except (OSError, PermissionError, FileNotFoundError):
            pass  # The OS can clean it up.

    shutil.rmtree(temp_folder, onerror=try_harder)

    try:
        os.remove(f"{CROWDIN_API_PROJECT_ID}.zip")
    except (OSError, FileNotFoundError):
        pass  # Already gone.
