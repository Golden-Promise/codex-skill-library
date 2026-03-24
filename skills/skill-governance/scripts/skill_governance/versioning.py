"""Lightweight version parsing and comparison helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass

SEMVER_RE = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)"
    r"(?:\.(?P<minor>0|[1-9]\d*))?"
    r"(?:\.(?P<patch>0|[1-9]\d*))?"
    r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
    r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
)


@dataclass(frozen=True)
class ParsedVersion:
    raw: str
    normalized: str
    major: int
    minor: int
    patch: int
    prerelease: str | None
    build: str | None

    @property
    def channel(self) -> str:
        return "prerelease" if self.prerelease else "stable"


def parse_version(raw_version: str | None) -> ParsedVersion | None:
    if raw_version is None:
        return None
    value = raw_version.strip()
    if not value:
        return None
    match = SEMVER_RE.match(value)
    if not match:
        return None
    major = int(match.group("major"))
    minor = int(match.group("minor") or 0)
    patch = int(match.group("patch") or 0)
    prerelease = match.group("prerelease") or None
    build = match.group("build") or None
    normalized = f"{major}.{minor}.{patch}"
    if prerelease:
        normalized += f"-{prerelease}"
    if build:
        normalized += f"+{build}"
    return ParsedVersion(
        raw=value,
        normalized=normalized,
        major=major,
        minor=minor,
        patch=patch,
        prerelease=prerelease,
        build=build,
    )


def normalize_version(raw_version: str | None) -> str:
    parsed = parse_version(raw_version)
    return parsed.normalized if parsed is not None else ""


def version_metadata(raw_version: str | None) -> dict[str, object]:
    parsed = parse_version(raw_version)
    if parsed is None:
        value = (raw_version or "").strip()
        return {
            "raw": value,
            "present": bool(value),
            "valid": False,
            "normalized": "",
            "channel": "unknown",
            "major": None,
            "minor": None,
            "patch": None,
            "prerelease": None,
            "build": None,
        }
    return {
        "raw": parsed.raw,
        "present": True,
        "valid": True,
        "normalized": parsed.normalized,
        "channel": parsed.channel,
        "major": parsed.major,
        "minor": parsed.minor,
        "patch": parsed.patch,
        "prerelease": parsed.prerelease,
        "build": parsed.build,
    }


def compare_versions(left: str | None, right: str | None) -> int | None:
    parsed_left = parse_version(left)
    parsed_right = parse_version(right)
    if parsed_left is None or parsed_right is None:
        return None

    left_tuple = (parsed_left.major, parsed_left.minor, parsed_left.patch)
    right_tuple = (parsed_right.major, parsed_right.minor, parsed_right.patch)
    if left_tuple < right_tuple:
        return -1
    if left_tuple > right_tuple:
        return 1

    if parsed_left.prerelease and not parsed_right.prerelease:
        return -1
    if parsed_right.prerelease and not parsed_left.prerelease:
        return 1
    if parsed_left.prerelease and parsed_right.prerelease:
        if parsed_left.prerelease < parsed_right.prerelease:
            return -1
        if parsed_left.prerelease > parsed_right.prerelease:
            return 1
    return 0

