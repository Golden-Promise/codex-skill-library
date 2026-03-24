"""Configuration and path resolution helpers for skill-governance."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .constants import (
    ALLOWED_EXPOSURE_MODES,
    DEFAULT_COMPAT_ENV,
    DEFAULT_CONFIG_FILENAMES,
    DEFAULT_LIBRARY_DIRNAME,
    DEFAULT_LIBRARY_ENV,
    DEFAULT_PLATFORM_DIRNAME,
)


class ConfigError(Exception):
    """Raised when repo config is missing or invalid."""


@dataclass
class WorkflowConfig:
    path: Path | None
    shared_root: Path | None
    project_library_root: Path | None
    exposure_root: Path | None
    exposure_mode: str | None
    workspace_root: Path | None
    platform_root: Path | None


def resolve_configured_path(raw_value: object, config_dir: Path) -> Path | None:
    if raw_value is None:
        return None
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise ConfigError(
            "[ERROR] skill_registry paths in the config file must be non-empty strings."
        )
    candidate = Path(raw_value).expanduser()
    if not candidate.is_absolute():
        candidate = (config_dir / candidate).resolve()
    else:
        candidate = candidate.resolve()
    return candidate


def discover_workflow_config_path(
    explicit_path: str | None,
    project_root: Path | None,
) -> Path | None:
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()
    if project_root is None:
        return None
    for filename in DEFAULT_CONFIG_FILENAMES:
        candidate = project_root / filename
        if candidate.exists():
            return candidate.resolve()
    return None


def load_workflow_config(config_path: Path | None) -> WorkflowConfig:
    if config_path is None:
        return WorkflowConfig(None, None, None, None, None, None, None)
    if not config_path.exists():
        raise ConfigError(f"[ERROR] Config file does not exist: {config_path}")
    try:
        data = tomllib.loads(config_path.read_text())
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"[ERROR] Could not parse config file {config_path}: {error}") from error

    registry = data.get("skill_registry")
    if registry is None:
        return WorkflowConfig(config_path, None, None, None, None, None, None)
    if not isinstance(registry, dict):
        raise ConfigError("[ERROR] [skill_registry] in the config file must be a table.")

    config_dir = config_path.parent
    exposure_mode = registry.get("exposure_mode")
    if exposure_mode is not None:
        if not isinstance(exposure_mode, str) or exposure_mode not in ALLOWED_EXPOSURE_MODES:
            allowed = ", ".join(sorted(ALLOWED_EXPOSURE_MODES))
            raise ConfigError(
                f"[ERROR] skill_registry.exposure_mode must be one of: {allowed}."
            )

    return WorkflowConfig(
        path=config_path,
        shared_root=resolve_configured_path(registry.get("shared_root"), config_dir),
        project_library_root=resolve_configured_path(registry.get("project_root"), config_dir),
        exposure_root=resolve_configured_path(registry.get("exposure_root"), config_dir),
        exposure_mode=exposure_mode,
        workspace_root=resolve_configured_path(registry.get("workspace_root"), config_dir),
        platform_root=resolve_configured_path(registry.get("platform_root"), config_dir),
    )


def detect_library_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    project_root: Path | None = None,
    bootstrap_project_layout: bool = False,
    prefer_project_library: bool = False,
    current_script: Path | None = None,
) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    env_root = os.environ.get(DEFAULT_LIBRARY_ENV)
    if env_root:
        return Path(env_root).expanduser().resolve()
    if (bootstrap_project_layout or prefer_project_library) and config.project_library_root:
        return config.project_library_root
    if (bootstrap_project_layout or prefer_project_library) and project_root is not None:
        return (project_root / DEFAULT_LIBRARY_DIRNAME).resolve()
    if config.shared_root:
        return config.shared_root
    if current_script is None:
        raise ConfigError(
            "[ERROR] current_script is required when no explicit or configured library root is available."
        )
    return current_script.resolve().parents[2]


def detect_compat_root(
    explicit_root: str | None,
    library_root: Path,
    allow_default: bool,
) -> Path | None:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    env_root = os.environ.get(DEFAULT_COMPAT_ENV)
    if env_root:
        return Path(env_root).expanduser().resolve()
    if not allow_default:
        return None
    candidate = library_root.parent
    if (candidate / ".agents" / "skills").exists():
        return candidate
    return None


def detect_exposure_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    project_root: Path | None,
) -> Path | None:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    if config.exposure_root:
        return config.exposure_root
    if project_root is None:
        return None
    return (project_root / ".agents" / "skills").resolve()


def resolve_exposure_mode(
    requested_mode: str | None,
    config: WorkflowConfig,
) -> str:
    mode = requested_mode or config.exposure_mode or "auto"
    if mode not in ALLOWED_EXPOSURE_MODES:
        allowed = ", ".join(sorted(ALLOWED_EXPOSURE_MODES))
        raise ConfigError(f"[ERROR] Exposure mode must be one of: {allowed}.")
    if mode != "auto":
        return mode
    if os.environ.get("CI"):
        return "manifest"
    if os.name == "nt":
        return "copy"
    return "symlink"


def detect_workspace_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    project_root: Path | None,
) -> Path | None:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    if config.workspace_root:
        return config.workspace_root
    if project_root is not None:
        return project_root.parent.resolve()
    return None


def detect_platform_root(
    explicit_root: str | None,
    config: WorkflowConfig,
    workspace_root: Path | None,
    project_root: Path | None,
    library_root: Path,
) -> Path:
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    if config.platform_root:
        return config.platform_root
    if workspace_root is not None:
        return (workspace_root / DEFAULT_PLATFORM_DIRNAME).resolve()
    if project_root is not None:
        return (project_root / DEFAULT_PLATFORM_DIRNAME).resolve()
    return (library_root.parent / DEFAULT_PLATFORM_DIRNAME).resolve()


def find_project_config_path(project_root: Path) -> Path | None:
    for filename in DEFAULT_CONFIG_FILENAMES:
        candidate = project_root / filename
        if candidate.exists():
            return candidate
    return None

