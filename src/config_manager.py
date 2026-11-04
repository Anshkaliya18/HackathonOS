"""
Sherpa Configuration Manager

Defines authoritative Phase 1 behavior: initialization, collection, validation,
and persistent storage of project-specific information in `.env.sherpa`.

Design principles:
- `.env.sherpa` lives in the project repository root (NOT in the skill directory).
- `.env.hackathon` is read only as a deprecated fallback when the new file is absent.
- It is the single source of truth for project-specific configuration.
- All fields default to UNKNOWN until explicitly provided.
- Human-editable: users may edit directly; skill must preserve manual edits.
- No secrets: API keys and secrets go in `.env`, never in `.env.sherpa`.
- Idempotent: running init multiple times must not duplicate or destroy data.

Configuration categories:
  HACKATHON_IDENTITY   - hackathon name, platform, URL, dates, rules
  PROBLEM_IDEA         - problem statement, target users, selected idea, MVP
  TECH_STACK           - programming languages, frontend, backend, database, AI/ML
  SUBMISSION           - requirements, demo status, PPT status, deployment
  TECHNICAL_CONSTRAINTS - budget, time, team size, constraints
  ARCHITECTURE_DECISIONS - architecture summary, key differentiators
  PROGRESS             - completed work, current work, blocked work, risks
  DELIVERABLES         - demo status, PPT status, documentation, deployment URL
  SUBMISSION           - submission requirements, team info, team captain
"""

from __future__ import annotations

import configparser
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENV_SHERPA_FILENAME = ".env.sherpa"
LEGACY_ENV_FILENAME = ".env.hackathon"
ENV_FILE = ".env"

# Category -> list of field names
CATEGORY_FIELDS: dict[str, list[str]] = {
    "HACKATHON_IDENTITY": [
        "HACKATHON_NAME",
        "HACKATHON_PLATFORM",
        "HACKATHON_URL",
        "HACKATHON_DASHBOARD_URL",
        "START_DATE_TIME",
        "DEADLINE_DATE_TIME",
        "TIMEZONE",
        "HACKATHON_ORGANIZER",
        "HACKATHON_CONTACT",
        "HACKATHON_THEME",
        "ELIGIBILITY_REQUIREMENTS",
        "PRIZE_INFORMATION",
    ],
    "PROBLEM_IDEA": [
        "PROBLEM_STATEMENT",
        "TARGET_USERS",
        "SELECTED_IDEA",
        "PRODUCT_CONCEPT",
        "MVP_SCOPE",
        "MVP_FEATURES",
        "KEY_DIFFERENTIATORS",
    ],
    "TECH_STACK": [
        "PROGRAMMING_LANGUAGES",
        "FRONTEND_FRAMEWORK",
        "BACKEND_FRAMEWORK",
        "DATABASE",
        "AI_ML_PROVIDER",
        "AI_MODEL_NAME",
        "DEPLOYMENT_PLATFORM",
        "OTHER_TECHNOLOGIES",
    ],
    "SUBMISSION": [
        "DEMO_STATUS",
        "PPT_STATUS",
        "DOCUMENTATION_STATUS",
        "DEPLOYMENT_URL",
        "GITHUB_REPOSITORY_URL",
        "DEMO_URL",
    ],
    "TECHNICAL_CONSTRAINTS": [
        "BUDGET_LIMIT",
        "TIME_LIMIT",
        "TEAM_SIZE",
        "TECHNICAL_CONSTRAINTS",
    ],
    "ARCHITECTURE_DECISIONS": [
        "ARCHITECTURE_SUMMARY",
        "IMPORTANT_DECISIONS",
        "KNOWN_LIMITATIONS",
    ],
    "PROGRESS": [
        "COMPLETED_WORKSTREAMS",
        "CURRENT_WORKSTREAM",
        "BLOCKED_WORKSTREAMS",
        "COMPLETED_FEATURES",
        "MVP_STATUS",
    ],
    "DELIVERABLES": [
        "DEMO_STATUS",
        "PPT_STATUS",
        "DOCUMENTATION_STATUS",
        "DEPLOYMENT_URL",
        "GITHUB_REPOSITORY_URL",
        "DEMO_URL",
    ],
    "SUBMISSION": [
        "SUBMISSION_REQUIREMENTS",
        "OPTIONAL_DELIVERABLES",
        "TEAM_NAME",
        "TEAM_CAPTAIN",
        "TEAM_MEMBERS",
        "TEAM_CONTACT_EMAIL",
        "TEAM_LOCATION",
    ],
}

# Fields that must never contain secrets
SECRET_FIELD_PATTERNS = [
    re.compile(r".*API_KEY", re.IGNORECASE),
    re.compile(r".*API_SECRET", re.IGNORECASE),
    re.compile(r".*PASSWORD", re.IGNORECASE),
    re.compile(r".*SECRET", re.IGNORECASE),
    re.compile(r".*TOKEN", re.IGNORECASE),
    re.compile(r".*PRIVATE_KEY", re.IGNORECASE),
    re.compile(r".*CREDENTIAL", re.IGNORECASE),
]

# Default values for all known fields
DEFAULT_VALUES: dict[str, str] = {
    # Hackathon Identity
    "HACKATHON_NAME": "UNKNOWN",
    "HACKATHON_PLATFORM": "UNKNOWN",
    "HACKATHON_URL": "UNKNOWN",
    "HACKATHON_DASHBOARD_URL": "UNKNOWN",
    "START_DATE_TIME": "UNKNOWN",
    "DEADLINE_DATE_TIME": "UNKNOWN",
    "TIMEZONE": "UNKNOWN",
    "HACKATHON_ORGANIZER": "UNKNOWN",
    "HACKATHON_CONTACT": "UNKNOWN",
    "HACKATHON_THEME": "UNKNOWN",
    "ELIGIBILITY_REQUIREMENTS": "UNKNOWN",
    "PRIZE_INFORMATION": "UNKNOWN",
    # Problem & Idea
    "PROBLEM_STATEMENT": "UNKNOWN",
    "TARGET_USERS": "UNKNOWN",
    "SELECTED_IDEA": "UNKNOWN",
    "PRODUCT_CONCEPT": "UNKNOWN",
    "MVP_SCOPE": "UNKNOWN",
    "MVP_FEATURES": "UNKNOWN",
    "KEY_DIFFERENTIATORS": "UNKNOWN",
    # Tech Stack
    "PROGRAMMING_LANGUAGES": "UNKNOWN",
    "FRONTEND_FRAMEWORK": "UNKNOWN",
    "BACKEND_FRAMEWORK": "UNKNOWN",
    "DATABASE": "UNKNOWN",
    "AI_ML_PROVIDER": "UNKNOWN",
    "AI_MODEL_NAME": "UNKNOWN",
    "DEPLOYMENT_PLATFORM": "UNKNOWN",
    "OTHER_TECHNOLOGIES": "UNKNOWN",
    # Submission
    "DEMO_STATUS": "UNKNOWN",
    "PPT_STATUS": "UNKNOWN",
    "DOCUMENTATION_STATUS": "UNKNOWN",
    "DEPLOYMENT_URL": "UNKNOWN",
    "GITHUB_REPOSITORY_URL": "UNKNOWN",
    "DEMO_URL": "UNKNOWN",
    # Technical Constraints
    "BUDGET_LIMIT": "UNKNOWN",
    "TIME_LIMIT": "UNKNOWN",
    "TEAM_SIZE": "UNKNOWN",
    "TECHNICAL_CONSTRAINTS": "UNKNOWN",
    # Architecture Decisions
    "ARCHITECTURE_SUMMARY": "UNKNOWN",
    "IMPORTANT_DECISIONS": "UNKNOWN",
    "KNOWN_LIMITATIONS": "UNKNOWN",
    # Progress
    "COMPLETED_WORKSTREAMS": "UNKNOWN",
    "CURRENT_WORKSTREAM": "UNKNOWN",
    "BLOCKED_WORKSTREAMS": "UNKNOWN",
    "COMPLETED_FEATURES": "UNKNOWN",
    "MVP_STATUS": "UNKNOWN",
    # Deliverables
    "DEMO_STATUS": "UNKNOWN",
    "PPT_STATUS": "UNKNOWN",
    "DOCUMENTATION_STATUS": "UNKNOWN",
    "DEPLOYMENT_URL": "UNKNOWN",
    "GITHUB_REPOSITORY_URL": "UNKNOWN",
    "DEMO_URL": "UNKNOWN",
    # Submission
    "SUBMISSION_REQUIREMENTS": "UNKNOWN",
    "OPTIONAL_DELIVERABLES": "UNKNOWN",
    "TEAM_NAME": "UNKNOWN",
    "TEAM_CAPTAIN": "UNKNOWN",
    "TEAM_MEMBERS": "UNKNOWN",
    "TEAM_CONTACT_EMAIL": "UNKNOWN",
    "TEAM_LOCATION": "UNKNOWN",
}


class VerificationError(Exception):
    """Raised when configuration validation fails."""


class ProjectConfig:
    """
    Manages `.env.sherpa` — the persistent project state file.

    Responsibilities:
    - Initialize `.env.sherpa` if missing
    - Load all fields into memory
    - Update fields from user input or repository evidence
    - Write changes back to disk (preserving comments and unknown fields)
    - Validate values against expected formats
    - Never write secrets to this file
    """

    def __init__(self, project_root: str | None = None):
        self.project_root = Path(project_root or os.getcwd())
        self.env_path = self.project_root / ENV_SHERPA_FILENAME
        self.legacy_env_path = self.project_root / LEGACY_ENV_FILENAME
        self.env_file = self.project_root / ".env"
        self._config: dict[str, str] = {}
        self._raw_lines: list[str] = []
        self._loaded = False
        self._changes: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Loading / Saving
    # ------------------------------------------------------------------

    def load(self) -> dict[str, str]:
        """Load .env.sherpa, or read the old filename as a deprecated fallback."""
        self.env_path = self.project_root / ENV_SHERPA_FILENAME
        source_path = self.env_path
        if not source_path.exists() and self.legacy_env_path.exists():
            import warnings
            warnings.warn(".env.hackathon is deprecated; copy it to .env.sherpa. The original is preserved.", DeprecationWarning)
        self._config = {}
        self._raw_lines = []

        if source_path.exists():
            self._load_from_file(source_path)
        else:
            # Initialize with defaults
            self._config = dict(DEFAULT_VALUES)
            self._raw_lines = self._build_initial_lines()
            self._write()

        self._loaded = True
        return dict(self._config)

    def _load_from_file(self, path: Path) -> None:
        """Parse a Sherpa project environment file, preserving comments and blank lines."""
        raw = path.read_text(encoding="utf-8")
        self._raw_lines = raw.splitlines(keepends=True)

        for line in self._raw_lines:
            stripped = line.strip()
            # Skip blank lines and comments
            if not stripped or stripped.startswith("#"):
                continue
            # Parse KEY=VALUE
            if "=" in stripped:
                key, _, value = stripped.partition("=")
                key = key.strip()
                value = value.strip()
                # Strip surrounding quotes
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                self._config[key] = value

        # Fill in defaults for missing fields
        for key, default_val in DEFAULT_VALUES.items():
            if key not in self._config:
                self._config[key] = default_val

    def _build_initial_lines(self) -> list[str]:
        """Build initial .env.sherpa content from defaults."""
        lines: list[str] = []
        lines.append("# =============================================================================")
        lines.append("# Hackathon Project State")
        lines.add("")
        lines.add("# This file is the persistent state for a sherpa-managed project.")
        lines.add("# It lives in .sherpa/project-state.md inside the hackathon project's repository.")
        lines.add("")
        lines.add("# Any field whose value is not known must be set to UNKNOWN.")
        lines.add("# Never invent or guess missing information.")
        lines.add("")
        lines.add("# =============================================================================")
        lines.add("")

        # Add sections based on categories
        for category, fields in CATEGORY_FIELDS.items():
            lines.append(f"# =============================================================================")
            lines.append(f"# {category}")
            lines.add(f"# =============================================================================")
            lines.add("")
            for field in fields:
                value = DEFAULT_VALUES.get(field, "UNKNOWN")
                lines.append(f'{field}="{value}"')
            lines.append("")

        return lines

    def save(self) -> None:
        """Write current state to .env.sherpa, preserving comments and unknown fields."""
        if not self.env_path:
            raise RuntimeError("Verifier not initialized: call load() first")

        lines: list[str] = []
        seen_keys: set[str] = set()

        # Preserve existing lines, updating values where we have new data
        for line in self._raw_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                lines.append(line.rstrip("\n"))
                continue

            if "=" in stripped:
                key, _, _ = stripped.partition("=")
                key = key.strip()
                if key in self._config:
                    lines.append(f'{key}="{self._config[key]}"')
                    seen_keys.add(key)
                else:
                    lines.append(line.rstrip("\n"))
            else:
                lines.append(line.rstrip("\n"))

        # Add any new keys not in original file
        for key, value in self._config.items():
            if key not in seen_keys:
                lines.append(f'{key}="{value}"')

        self._raw_lines = lines
        self.env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------
    # Get / Set
    # ------------------------------------------------------------------

    def get(self, key: str, default: str | None = None) -> str | None:
        """Get a configuration value."""
        if not self._loaded:
            self.load()
        return self._config.get(key, default)

    def set(self, key: str, value: str, source: str = "user") -> None:
        """Set a configuration value. Marks it as changed."""
        if not self._loaded:
            self.load()
        self._config[key] = value
        self._changes[key] = value

    def get_all(self) -> dict[str, str]:
        """Return all configuration values."""
        if not self._loaded:
            self.load()
        return dict(self._config)

    def has(self, key: str) -> bool:
        """Check if a key exists."""
        if not self._loaded:
            self.load()
        return key in self._config

    def is_unknown(self, key: str) -> bool:
        """Check if a field is UNKNOWN."""
        val = self.get(key)
        return val == "UNKNOWN" or val == ""

    def get_changes(self) -> dict[str, str]:
        """Return changes since last load."""
        return dict(self._changes)

    def mark_synced(self) -> None:
        """Mark all pending changes as synced."""
        self._changes.clear()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Validate all current values. Returns list of warning messages."""
        warnings: list[str] = []

        for key, value in self._config.items():
            if not value or value == "UNKNOWN":
                continue  # Skip unknowns

            # Check for potential secrets in non-secret fields
            for pattern in _SECRET_PATTERNS:
                if pattern.search(key):
                    warnings.append(
                        f"WARNING: '{key}' appears to contain a secret. "
                        f"Move to .env file instead."
                    )
                    break

        return warnings

    def validate_all(self) -> list[str]:
        """Alias for validate()."""
        return self.validate()

    # ------------------------------------------------------------------
    # Convenience methods for common fields
    # ------------------------------------------------------------------

    def get_hackathon_name(self) -> str | None:
        return self.get("HACKATHON_NAME")

    def get_problem_statement(self) -> str | None:
        return self.get("PROBLEM_STATEMENT")

    def get_target_users(self) -> str | None:
        return self.get("TARGET_USERS")

    def get_selected_idea(self) -> str | None:
        return self.get("SELECTED_IDEA")

    def get_tech_stack(self) -> dict[str, str]:
        return {
            "programming_languages": self.get("PROGRAMMING_LANGUAGES"),
            "frontend_framework": self.get("FRONTEND_FRAMEWORK"),
            "backend_framework": self.get("BACKEND_FRAMEWORK"),
            "database": self.get("DATABASE"),
            "ai_ml_provider": self.get("AI_ML_PROVIDER"),
            "ai_model_name": self.get("AI_MODEL_NAME"),
            "deployment_platform": self.get("DEPLOYMENT_PLATFORM"),
            "other_technologies": self.get("OTHER_TECHNOLOGIES"),
        }

    def get_submission_info(self) -> dict[str, str]:
        return {
            "deadline": self.get("DEADLINE_DATE_TIME"),
            "requirements": self.get("SUBMISSION_REQUIREMENTS"),
            "demo_status": self.get("DEMO_STATUS"),
            "ppt_status": self.get("PPT_STATUS"),
            "deployment_url": self.get("DEPLOYMENT_URL"),
            "github_url": self.get("GITHUB_REPOSITORY_URL"),
            "demo_url": self.get("DEMO_URL"),
        }


# Singleton instance
_verifier: ProjectConfig | None = None


def get_verifier(project_root: str | None = None) -> ProjectConfig:
    """Get or create the global verifier instance."""
    global _verifier
    if _verifier is None:
        _verifier = ProjectConfig(project_root)
    return _verifier


def reset_verifier() -> None:
    """Reset the verifier singleton (mainly for testing)."""
    global _verifier
    _verifier = None
