#!/usr/bin/env python3
import hashlib
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
ADDON_DIR = ROOT / "ombi"
CONFIG_PATH = ADDON_DIR / "config.yaml"
CHANGELOG_PATH = ADDON_DIR / "CHANGELOG.md"
UPDATER_PATH = ADDON_DIR / "updater.json"
BUILD_PATH = ADDON_DIR / "build.json"
BASE_DIGEST_PATH = ADDON_DIR / "base-image.digest"


class HomeAssistantDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def quoted_string(dumper, data):
    style = '"' if data and re.fullmatch(r"\d+\.\d+\.\d+", data) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


HomeAssistantDumper.add_representer(str, quoted_string)


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def normalize_version(tag: str) -> str | None:
    match = re.fullmatch(r"v?([0-9]+\.[0-9]+\.[0-9]+)", tag)
    return match.group(1) if match else None


def github_json(path: str):
    token = os.environ.get("GITHUB_TOKEN", "")
    request = urllib.request.Request(
        f"https://api.github.com/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "wheemer-ombi-app-updater",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def latest_ombi_version(include_prerelease: bool) -> str:
    releases = github_json("repos/Ombi-app/Ombi/releases?per_page=100")
    versions: list[str] = []
    for release in releases:
        if release.get("draft"):
            continue
        if release.get("prerelease") and not include_prerelease:
            continue
        version = normalize_version(str(release.get("tag_name", "")))
        if version:
            versions.append(version)

    if not versions:
        raise RuntimeError("No matching Ombi releases found")

    return max(versions, key=version_key)


def resolve_base_image(tag: str) -> str:
    registry = "https://ghcr.io"
    repository = "linuxserver/ombi"
    with urllib.request.urlopen(
        f"{registry}/token?service=ghcr.io&scope=repository:{repository}:pull",
        timeout=30,
    ) as response:
        token = json.load(response)["token"]

    request = urllib.request.Request(
        f"{registry}/v2/{repository}/manifests/{tag}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": (
                "application/vnd.oci.image.index.v1+json, "
                "application/vnd.docker.distribution.manifest.list.v2+json"
            ),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        manifest = response.read()
        digest = f"sha256:{hashlib.sha256(manifest).hexdigest()}"
        if digest != response.headers.get("Docker-Content-Digest"):
            raise RuntimeError(f"LinuxServer image digest mismatch for {tag}")

    platforms = {
        (entry["platform"]["os"], entry["platform"]["architecture"])
        for entry in json.loads(manifest)["manifests"]
    }
    if not {("linux", "amd64"), ("linux", "arm64")} <= platforms:
        raise RuntimeError(f"LinuxServer image {tag} must support amd64 and arm64")
    return f"ghcr.io/{repository}:{tag}@{digest}"


def prepend_changelog(addon_version: str, upstream_version: str) -> None:
    today = datetime.now(timezone.utc).date().isoformat()
    existing = CHANGELOG_PATH.read_text(encoding="utf-8")
    heading = f"## {addon_version} ({today})"
    if heading in existing:
        return

    entry = (
        f"{heading}\n\n"
        f"- Updated Ombi upstream version to `{upstream_version}`.\n\n"
    )
    if existing.startswith("# Changelog\n\n"):
        updated = existing.replace("# Changelog\n\n", f"# Changelog\n\n{entry}", 1)
    else:
        updated = f"{entry}{existing}"
    CHANGELOG_PATH.write_text(updated, encoding="utf-8")


def main() -> int:
    updater = json.loads(UPDATER_PATH.read_text(encoding="utf-8"))
    include_prerelease = bool(updater.get("github_beta"))
    current_upstream = str(updater.get("upstream_version", "")).strip()
    latest_upstream = latest_ombi_version(include_prerelease)

    if version_key(latest_upstream) <= version_key(current_upstream):
        print(f"Ombi is current: {current_upstream}")
        return 0

    base_tags = github_json("repos/linuxserver/docker-ombi/releases?per_page=100")
    matching_tags = [
        match
        for release in base_tags
        if not release.get("draft")
        and (match := re.fullmatch(
            rf"(?:development-)?v{re.escape(latest_upstream)}-ls(\d+)",
            release["tag_name"],
        ))
    ]
    if not matching_tags:
        print(f"Waiting for LinuxServer to publish Ombi {latest_upstream}")
        return 0

    base_tag = max(matching_tags, key=lambda match: int(match[1]))[0]
    base_image = resolve_base_image(base_tag)
    base_ref, digest = base_image.rsplit("@", 1)
    build = json.loads(BUILD_PATH.read_text(encoding="utf-8"))
    for arch in build["build_from"]:
        build["build_from"][arch] = base_ref
    BUILD_PATH.write_text(json.dumps(build, indent=4) + "\n", encoding="utf-8")
    BASE_DIGEST_PATH.write_text(digest + "\n", encoding="utf-8")

    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    addon_version = latest_upstream

    config["version"] = addon_version
    CONFIG_PATH.write_text(
        yaml.dump(config, Dumper=HomeAssistantDumper, sort_keys=False),
        encoding="utf-8",
    )

    updater.update(
        {
            "last_update": datetime.now(timezone.utc).date().isoformat(),
            "paused": False,
            "source": "github",
            "upstream_repo": "Ombi-app/Ombi",
            "upstream_version": latest_upstream,
        }
    )
    UPDATER_PATH.write_text(json.dumps(updater, indent=2) + "\n", encoding="utf-8")
    prepend_changelog(addon_version, latest_upstream)

    print(f"Updated Ombi from {current_upstream} to {latest_upstream}")
    print(f"App version: {addon_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
