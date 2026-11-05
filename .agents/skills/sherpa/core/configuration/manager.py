#!/usr/bin/env python3
"""sherpa project configuration utility (Python standard library only).
Never prints, logs, or persists secret values. Use from the target project root.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

UNKNOWN = "UNKNOWN"
STATE_DIRECTORY = ".sherpa"
LEGACY_STATE_DIRECTORY = ".hackathon"
BOOLEAN_KEYS = {
    "ENABLE_WEB_RESEARCH", "ENABLE_AUTO_VERIFY", "ENABLE_RED_TEAM", "ENABLE_VIDEO_ASSIST",
    "REQUIRE_HUMAN_APPROVAL",
}
INTEGER_LIMITS = {"MAX_AUTO_ITERATIONS": (1, 20), "MAX_AUTO_FIXES": (0, 50)}
SECRET_ENV_KEYS = ("AI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GITHUB_TOKEN")
SECRET_FILE_NAMES = {"credentials.json", "service-account.json", "secrets.json"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "coverage", "__pycache__"}
SECRET_PATTERNS = (
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("Bearer token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("password or secret assignment", re.compile(r"(?i)\b(?:password|passwd|client_secret|api[_-]?key)\s*[:=]\s*[\"']?[^\s\"'<>]{8,}")),
    ("database URL with password", re.compile(r"(?i)\b(?:postgres|mysql|mongodb)(?:ql)?://[^:\s/]+:[^@\s/]{4,}@")),
)


def parse_env_file(path: Path) -> tuple[dict[str, str], list[str]]:
    """Parse a small dotenv subset; diagnostics never include source values."""
    values: dict[str, str] = {}
    issues: list[str] = []
    if not path.exists():
        return values, issues
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError):
        return values, [".env could not be read as UTF-8"]
    key_re = re.compile(r"^[A-Z_][A-Z0-9_]*$")
    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            issues.append(f".env line {number}: expected KEY=value")
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key_re.fullmatch(key):
            issues.append(f".env line {number}: invalid variable name")
            continue
        if key in values:
            issues.append(f".env line {number}: duplicate variable {key}")
            continue
        value = value.strip()
        if value.startswith(('"', "'")):
            quote = value[0]
            if len(value) < 2 or not value.endswith(quote):
                issues.append(f".env line {number}: unterminated quoted value for {key}")
                continue
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        values[key] = value
    return values, issues


def resolve_value(explicit: Any, project: Any, process_env: Any, dotenv: Any, default: Any = None) -> Any:
    """Precedence: explicit > project > process env > .env > default > UNKNOWN.
    Empty and UNKNOWN values are unresolved and fall through; literal UNKNOWN is
    returned when no lower-precedence source supplies a value.
    """
    for value in (explicit, project, process_env, dotenv, default):
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        if isinstance(value, str) and value.strip().upper() == UNKNOWN:
            continue
        return value
    return UNKNOWN


def load_json(path: Path) -> tuple[dict[str, Any], list[str]]:
    if not path.exists():
        return {}, [f"Missing {path.name}"]
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(value, dict):
            return {}, [f"{path.name}: top level must be a JSON object"]
        return value, []
    except (json.JSONDecodeError, UnicodeError, OSError) as exc:
        if isinstance(exc, json.JSONDecodeError):
            return {}, [f"{path.name}:{exc.lineno}: malformed JSON"]
        return {}, [f"{path.name}: could not be read"]


def nonempty(value: Any) -> bool:
    return value is not None and not (isinstance(value, str) and value.strip() in ("", UNKNOWN))


def validate_url(value: Any) -> str:
    if not nonempty(value):
        return "UNKNOWN"
    try:
        parsed = urlparse(str(value))
        return "CONFIGURED" if parsed.scheme in ("http", "https") and parsed.hostname else "INVALID"
    except ValueError:
        return "INVALID"


def validate_timezone(value: Any) -> str:
    if not nonempty(value):
        return "UNKNOWN"
    try:
        ZoneInfo(str(value))
        return "CONFIGURED"
    except ZoneInfoNotFoundError:
        return "INVALID"
    except (ValueError, OSError):
        return "INVALID"


def validate_deadline(value: Any) -> str:
    if not nonempty(value):
        return "UNKNOWN"
    try:
        dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return "CONFIGURED"
    except (ValueError, TypeError):
        return "INVALID"


def git_output(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    except (OSError, subprocess.SubprocessError):
        return subprocess.CompletedProcess(["git", *args], 127, "", "git unavailable")


def is_git_root(root: Path) -> bool:
    result = git_output(root, "rev-parse", "--show-toplevel")
    if result.returncode:
        return False
    try:
        return Path(result.stdout.strip()).resolve() == root.resolve()
    except OSError:
        return False


def is_env_ignored(root: Path) -> bool:
    result = git_output(root, "check-ignore", "--quiet", ".env")
    if result.returncode == 0:
        return True
    ignore = root / ".gitignore"
    if not ignore.is_file():
        return False
    patterns = [x.strip() for x in ignore.read_text(encoding="utf-8-sig").splitlines() if x.strip() and not x.lstrip().startswith("#")]
    ignored = ".env" in patterns or ".env.*" in patterns
    if "!.env" in patterns:
        ignored = False
    return ignored


def tracked_env(root: Path) -> bool:
    if not is_git_root(root):
        return False
    result = git_output(root, "ls-files", "--error-unmatch", ".env")
    return result.returncode == 0


def scan_secrets(root: Path) -> list[str]:
    """Return redacted type/path/line indicators; never return matched text."""
    findings: list[str] = []
    for directory, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(directory)
        for name in files:
            path = base / name
            rel = path.relative_to(root).as_posix()
            if name in SECRET_FILE_NAMES or path.suffix.lower() in (".pem", ".key", ".p12", ".pfx", ".jks"):
                findings.append(f"sensitive credential file: {rel}")
                continue
            if name == ".env" or (name.startswith(".env.") and not name.endswith(".example")):
                continue
            if path.suffix.lower() not in (".md", ".txt", ".json", ".jsonc", ".yaml", ".yml", ".toml", ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".xml", ".sh", ".ps1", ".env", ".example"):
                continue
            try:
                if path.stat().st_size > 1_000_000:
                    continue
                lines = path.read_text(encoding="utf-8-sig").splitlines()
            except (OSError, UnicodeError):
                continue
            for number, line in enumerate(lines, 1):
                for label, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        findings.append(f"{label}: {rel}:{number}")
                        break
    return findings


def env_value(key: str, dotenv: dict[str, str], process_env: dict[str, str]) -> Any:
    return resolve_value(None, None, process_env.get(key), dotenv.get(key))


def project_state_dir(root: Path) -> Path:
    """Prefer Sherpa state; read the former directory as a one-release fallback."""
    current = root / STATE_DIRECTORY
    legacy = root / LEGACY_STATE_DIRECTORY
    if current.exists():
        return current
    if legacy.exists():
        return legacy
    return current


def legacy_state_warning(root: Path) -> str | None:
    if not (root / STATE_DIRECTORY).exists() and (root / LEGACY_STATE_DIRECTORY).exists():
        return ("Deprecated .hackathon/ state is being read. Run `sherpa migrate` to copy it "
                "to .sherpa/; the original directory will be preserved.")
    return None


def config_snapshot(root: Path, process_env: dict[str, str] | None = None) -> dict[str, Any]:
    process_env = dict(os.environ if process_env is None else process_env)
    state_root = project_state_dir(root)
    hackathon, h_errors = load_json(state_root / "hackathon.json")
    settings, s_errors = load_json(state_root / "settings.json")
    dotenv, env_errors = parse_env_file(root / ".env")
    # Missing configuration is an expected pre-INIT state, not a malformed one.
    errors = [e for e in h_errors + s_errors + env_errors if not e.startswith("Missing ")]
    result: dict[str, Any] = {"errors": errors, "warnings": [], "fields": {}, "secret_findings": [], "secret_configured": False}
    warning = legacy_state_warning(root)
    if warning:
        result["warnings"].append(warning)

    def value(path: tuple[str, ...], env_key: str | None = None, default: Any = None) -> Any:
        current: Any = hackathon
        for segment in path:
            current = current.get(segment) if isinstance(current, dict) else None
        return resolve_value(None, current, process_env.get(env_key) if env_key else None,
                             dotenv.get(env_key) if env_key else None, default)

    if not (state_root / "project-state.md").exists():
        result["warnings"].append("Missing project-state.md")
        result["fields"]["Current phase"] = UNKNOWN
    else:
        try:
            state_text = (state_root / "project-state.md").read_text(encoding="utf-8-sig")
            phase_match = re.search(r"(?im)^\|\s*Phase\s*\|\s*([^|]+?)\s*\|", state_text)
            result["fields"]["Current phase"] = phase_match.group(1).strip() if phase_match and phase_match.group(1).strip().upper() != UNKNOWN else UNKNOWN
        except (OSError, UnicodeError):
            result["fields"]["Current phase"] = UNKNOWN
    result["fields"]["Hackathon name"] = value(("name",), "HACKATHON_NAME")
    result["fields"]["Hackathon URL status"] = validate_url(value(("url",), "HACKATHON_URL"))
    result["fields"]["Platform"] = value(("platform",), "HACKATHON_PLATFORM")
    result["fields"]["Edition"] = value(("edition",), "HACKATHON_EDITION")
    result["fields"]["Deadline status"] = validate_deadline(value(("deadline", "datetime"), "HACKATHON_DEADLINE"))
    result["fields"]["Timezone status"] = validate_timezone(value(("deadline", "timezone"), "HACKATHON_TIMEZONE"))
    for check_name in ("Hackathon URL status", "Deadline status", "Timezone status"):
        if result["fields"][check_name] == "INVALID": result["errors"].append(f"{check_name}: invalid value")
    for label, field, env_key in (("Project name", ("project", "name"), "PROJECT_NAME"),
                                  ("Project path", ("project", "path"), "PROJECT_PATH"),
                                  ("Repository", ("project", "repository"), "GITHUB_REPOSITORY"),
                                  ("Deployment URL status", ("project", "deployment"), "DEPLOYMENT_URL")):
        val = value(field, env_key)
        if label == "Project path" and nonempty(val):
            path = Path(str(val)); path = path if path.is_absolute() else (root / path)
            result["fields"][label] = "CONFIGURED" if path.exists() else "INVALID"
        elif label == "Repository" and nonempty(val):
            result["fields"][label] = "CONFIGURED" if (validate_url(val) == "CONFIGURED" or re.fullmatch(r"[\w.-]+/[\w.-]+", str(val))) else "INVALID"
        elif label == "Deployment URL status":
            result["fields"][label] = validate_url(val)
        else:
            result["fields"][label] = "CONFIGURED" if nonempty(val) else "UNKNOWN"

    setting_fields = (
        ("Agent platform", ("agent_platform",), "AGENT_PLATFORM", None),
        ("AI provider", ("ai_provider",), "AI_PROVIDER", None),
        ("AI model", ("ai_model",), "AI_MODEL", None),
        ("Verification", ("verification", "enabled"), "ENABLE_AUTO_VERIFY", True),
        ("Red team", ("red_team", "enabled"), "ENABLE_RED_TEAM", True),
        ("Research", ("research", "enabled"), "ENABLE_WEB_RESEARCH", True),
        ("Video assist", ("video", "enabled"), "ENABLE_VIDEO_ASSIST", True),
        ("Max iterations", ("autonomous_loop", "max_iterations"), "MAX_AUTO_ITERATIONS", 5),
        ("Max auto fixes", ("autonomous_loop", "max_auto_fixes"), "MAX_AUTO_FIXES", 10),
        ("Human approval", ("autonomous_loop", "require_human_approval"), "REQUIRE_HUMAN_APPROVAL", True),
    )
    for label, path, env_key, default in setting_fields:
        current: Any = settings
        for segment in path:
            current = current.get(segment) if isinstance(current, dict) else None
        resolved = resolve_value(None, current, process_env.get(env_key), dotenv.get(env_key), default)
        if label in ("Max iterations", "Max auto fixes"):
            try:
                number = int(resolved)
                low, high = INTEGER_LIMITS[env_key]
                result["fields"][label] = number if low <= number <= high else "INVALID"
            except (ValueError, TypeError): result["fields"][label] = "INVALID" if resolved != UNKNOWN else UNKNOWN
        elif label in ("Verification", "Red team", "Research", "Video assist", "Human approval"):
            if isinstance(resolved, bool): result["fields"][label] = resolved
            elif str(resolved).lower() in ("true", "false"): result["fields"][label] = str(resolved).lower() == "true"
            else: result["fields"][label] = "INVALID" if resolved != UNKNOWN else UNKNOWN
        else:
            result["fields"][label] = resolved if nonempty(resolved) else UNKNOWN
        if result["fields"].get(label) == "INVALID": result["errors"].append(f"{label}: invalid value")

    result["fields"]["Git repository"] = "CONFIGURED" if is_git_root(root) else "MISSING"
    result["secret_configured"] = any(nonempty(process_env.get(k)) or nonempty(dotenv.get(k)) for k in SECRET_ENV_KEYS)

    for key in BOOLEAN_KEYS:
        raw = process_env.get(key, dotenv.get(key))
        if raw is not None and str(raw).strip() and str(raw).lower() not in ("true", "false"):
            result["errors"].append(f"{key}: expected true or false")
    for key, (low, high) in INTEGER_LIMITS.items():
        raw = process_env.get(key, dotenv.get(key))
        if raw is not None and str(raw).strip():
            try: number = int(raw)
            except (ValueError, TypeError): result["errors"].append(f"{key}: expected an integer"); continue
            if not low <= number <= high: result["errors"].append(f"{key}: must be between {low} and {high}")
    if result["fields"].get("Human approval") is False:
        result["warnings"].append("WARNING: Human approval is disabled for autonomous operations.")
    if (root / ".env").exists() and not is_env_ignored(root):
        result["errors"].append(".env exists but is not ignored by Git")
    if tracked_env(root):
        result["errors"].append(".env is tracked by Git; remove it from the index and rotate any exposed credentials")
    result["secret_findings"] = scan_secrets(root)
    if result["secret_findings"]:
        result["errors"].append(f"Secret scan found {len(result['secret_findings'])} indicator(s) in scanned files")
    if result["errors"]:
        result["status"] = "INVALID"
    elif not (state_root / "hackathon.json").exists() and not (state_root / "settings.json").exists():
        result["status"] = "MISSING"
    else:
        unknowns = sum(1 for val in result["fields"].values() if val == UNKNOWN)
        result["status"] = "CONFIGURED" if unknowns == 0 else "PARTIALLY_CONFIGURED"
    return result


def print_overview(snapshot: dict[str, Any]) -> None:
    f = snapshot["fields"]
    print("Sherpa CONFIGURATION")
    print(f"Status: {snapshot['status']}")
    print(f"Current phase: {f.get('Current phase', UNKNOWN)}")
    for label in ("Hackathon name", "Platform", "Edition", "Project name", "Project path"):
        value = f.get(label, UNKNOWN)
        print(f"{label}: {value if nonempty(value) else UNKNOWN}")
    for label in ("Hackathon URL status", "Deadline status", "Timezone status", "Repository", "Deployment URL status"):
        print(f"{label}: {f.get(label, UNKNOWN)}")
    print(f"AI provider: {f.get('AI provider', UNKNOWN)}")
    print(f"AI credential: {'Configured' if snapshot.get('secret_configured') else 'Missing'}")
    for label in ("Verification", "Red team", "Research", "Video assist"):
        value=f.get(label, UNKNOWN); print(f"{label}: {value if value is not UNKNOWN else 'UNKNOWN'}")
    print(f"Max iterations: {f.get('Max iterations', UNKNOWN)}")
    print(f"Max auto fixes: {f.get('Max auto fixes', UNKNOWN)}")
    print(f"Human approval: {'REQUIRED' if f.get('Human approval') is True else 'DISABLED' if f.get('Human approval') is False else UNKNOWN}")
    for warning in snapshot["warnings"]: print(warning)


def print_check(snapshot: dict[str, Any], root: Path) -> None:
    print(f"Configuration: {snapshot['status']}")
    for label, value in snapshot["fields"].items(): print(f"{label}: {value}")
    dotenv, _ = parse_env_file(root / ".env")
    for key in SECRET_ENV_KEYS: print(f"{key}: {'Configured' if nonempty(os.environ.get(key)) or nonempty(dotenv.get(key)) else 'Missing'}")
    print(f".env ignored: {'YES' if is_env_ignored(root) else 'NO / NOT APPLICABLE'}")
    print(f".env tracked: {'YES' if tracked_env(root) else 'NO'}")
    if snapshot["secret_findings"]:
        print("Secret scan: FAIL — indicators found (values redacted)")
        for finding in snapshot["secret_findings"]: print(f"  {finding}")
    else:
        print("Secret scan: PASS — no known secret patterns detected in the scanned scope")
    for warning in snapshot["warnings"]: print(warning)
    for error in snapshot["errors"]: print(f"ERROR: {error}")
    if not snapshot["errors"]:
        print("No configuration errors detected. External provider connectivity was not tested.")
    elif snapshot["status"] == "MISSING":
        print("Configuration files are missing; run INIT to create them without overwriting existing data.")


def ensure_gitignore(root: Path) -> list[str]:
    path = root / ".gitignore"
    original = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    required = (".env", ".env.*", "!.env.sherpa.example", "!.env.*.example", "*.key", "*.pem",
                "credentials.json", "service-account.json", "secrets.json")
    present = set(line.strip() for line in original.splitlines())
    additions = [line for line in required if line not in present]
    if additions:
        prefix = original
        if prefix and not prefix.endswith(("\n", "\r")): prefix += "\n"
        if prefix and not prefix.endswith("\n\n"): prefix += "\n"
        path.write_text(prefix + "# sherpa local environment and credentials\n" + "\n".join(additions) + "\n", encoding="utf-8")
    return additions


def init_project(root: Path, create_env: bool = False) -> tuple[list[str], list[str]]:
    root = root.resolve()
    if not root.is_dir(): raise ValueError("project root does not exist")
    if ((root / "SKILL.md").exists() and (root / "workflows" / "lifecycle.md").exists()
            and (root / "commands" / "manifest.json").exists()):
        raise ValueError("refusing to initialize the sherpa framework repository; run from a hackathon project root")
    template_root = Path(__file__).resolve().parents[2]
    created: list[str] = []; preserved: list[str] = []
    state_root = project_state_dir(root)
    warning = legacy_state_warning(root)
    if warning:
        raise ValueError(warning + " Run `sherpa migrate` before initializing or writing state.")
    state_root = root / STATE_DIRECTORY
    destinations = {
        ".env.sherpa.example": template_root / ".env.sherpa.example",
        f"{state_root.name}/hackathon.json": template_root / "templates/configuration/hackathon.json",
        f"{state_root.name}/settings.json": template_root / "templates/configuration/settings.json",
        f"{state_root.name}/config/project.env.example": template_root / "templates/configuration/project.env.example",
        f"{state_root.name}/config/providers.env.example": template_root / "templates/configuration/providers.env.example",
        f"{state_root.name}/config/integrations.env.example": template_root / "templates/configuration/integrations.env.example",
        f"{state_root.name}/project-state.md": template_root / "templates/project-state.md",
    }
    for relative, source in destinations.items():
        target = root / relative
        if target.exists():
            preserved.append(relative)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_text(encoding="utf-8-sig")
        if relative == f"{state_root.name}/hackathon.json":
            data=json.loads(content); data["project"]["path"]=str(root); content=json.dumps(data,indent=2)+"\n"
        if relative == f"{state_root.name}/project-state.md":
            content=content.replace("| Phase | UNKNOWN |", "| Phase | Understand Rules |", 1)
            content=content.replace("| State last updated | UNKNOWN |", f"| State last updated | {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')} |", 1)
        target.write_text(content,encoding="utf-8")
        created.append(relative)
    if create_env:
        target=root/".env"
        if target.exists(): preserved.append(".env")
        else:
            target.write_text((template_root/".env.sherpa.example").read_text(encoding="utf-8-sig"),encoding="utf-8")
            created.append(".env")
    additions=ensure_gitignore(root)
    if additions: created.append(".gitignore rules: "+", ".join(additions))
    else: preserved.append(".gitignore (required protection already present)")
    return created,preserved


def parse_overrides(values: list[str]) -> dict[str, str]:
    result={}
    for item in values:
        if "=" not in item: raise ValueError("--override must use KEY=VALUE; value omitted from diagnostics")
        key,value=item.split("=",1)
        if not re.fullmatch(r"[A-Z_][A-Z0-9_]*",key): raise ValueError("invalid --override variable name")
        result[key]=value
    return result


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description="Sherpa project configuration utility")
    parser.add_argument("--project-root",default=".",help="hackathon project root (default: current directory)")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("config",help="show redacted configuration overview")
    check=sub.add_parser("check",help="validate config, environment, Git protection, and secrets")
    check.add_argument("--override",action="append",default=[],metavar="KEY=VALUE",help="transient non-secret precedence override")
    init=sub.add_parser("init",help="create missing project configuration without overwriting")
    init.add_argument("--create-env",action="store_true",help="also create an empty-placeholder .env from .env.example")
    args=parser.parse_args(argv)
    root=Path(args.project_root).expanduser().resolve()
    if not root.is_dir(): print("ERROR: project root does not exist"); return 2
    if args.command=="init":
        try:
            created,preserved=init_project(root,args.create_env)
            print("Sherpa configuration initialization")
            print("Created: "+(", ".join(created) if created else "nothing; all configuration already existed"))
            print("Preserved: "+(", ".join(preserved) if preserved else "none"))
            return 0
        except (OSError,ValueError,json.JSONDecodeError) as exc:
            print(f"ERROR: {exc}"); return 2
    snapshot=config_snapshot(root)
    if args.command=="config": print_overview(snapshot); return 0
    try: overrides=parse_overrides(args.override)
    except ValueError as exc: print(f"ERROR: {exc}"); return 2
    # Overrides affect validation only and are never persisted or printed.
    dotenv,env_errors=parse_env_file(root/".env")
    for key,value in overrides.items():
        if key in SECRET_ENV_KEYS: print("ERROR: secret overrides are not allowed on the command line"); return 2
        dotenv[key]=value
    if overrides:
        isolated=config_snapshot(root,process_env={**os.environ,**overrides})
        snapshot=isolated
    print_check(snapshot, root)
    return 1 if snapshot["errors"] else 0

if __name__=="__main__":
    raise SystemExit(main())
