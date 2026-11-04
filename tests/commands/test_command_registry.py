#!/usr/bin/env python3
"""Static validation of sherpa Stage 1 native command manifests.
Does not invoke an agent model, run a slash command, or mutate project state.
"""
from __future__ import annotations
import json
import copy
import importlib.util
import shutil
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / ".claude/skills/sherpa/SKILL.md"
KILO_DIR = ROOT / ".kilo/commands"
OPENCODE = ROOT / ".opencode/commands/sherpa.md"
DOCS = ROOT / "commands/README.md"
ADAPTERS = ("claude", "kilo", "opencode")
MANIFEST = json.loads((ROOT / "commands/manifest.json").read_text(encoding="utf-8-sig"))
COMMANDS = tuple(item["command"] for item in MANIFEST["implemented"])
KILO_COMMANDS = ("sherpa", *COMMANDS)
CLAUDE_SKILLS = ROOT / ".claude/skills"
ROUTER_SPEC = importlib.util.spec_from_file_location("sherpa_manifest_router", ROOT / "core/commands/router.py")
ROUTER = importlib.util.module_from_spec(ROUTER_SPEC)
sys.modules[ROUTER_SPEC.name] = ROUTER
ROUTER_SPEC.loader.exec_module(ROUTER)


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise AssertionError("frontmatter must begin on first line")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise AssertionError("frontmatter closing delimiter missing") from exc
    data = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data, "\n".join(lines[end + 1:])


def tests() -> list[tuple[str, object]]:
    def claude():
        meta, body = frontmatter(CLAUDE.read_text(encoding="utf-8-sig"))
        assert meta.get("name") == "sherpa"
        assert meta.get("disable-model-invocation") == "true"
        assert "$ARGUMENTS" in body and "SKILL.md" in body
    def kilo():
        for name in KILO_COMMANDS:
            meta, body = frontmatter((KILO_DIR / f"{name}.md").read_text(encoding="utf-8-sig"))
            assert meta.get("description"), name
            assert "SKILL.md" in body, name
    def opencode():
        meta, body = frontmatter(OPENCODE.read_text(encoding="utf-8-sig"))
        assert meta.get("description") and "$ARGUMENTS" in body and "@SKILL.md" in body
    def adapters():
        present = tuple(sorted(p.name for p in (ROOT / "adapters").iterdir() if p.is_dir()))
        assert present == tuple(sorted(ADAPTERS)), present
    def native_paths():
        assert CLAUDE.is_file() and OPENCODE.is_file()
        assert all((CLAUDE_SKILLS / name / "SKILL.md").is_file() for name in COMMANDS)
        assert all((ROOT / ".opencode/commands" / f"{name}.md").is_file() for name in COMMANDS)
        assert all((KILO_DIR / f"{name}.md").is_file() for name in KILO_COMMANDS)
    def docs_mapping():
        text = DOCS.read_text(encoding="utf-8-sig")
        lower = text.lower()
        for platform in ADAPTERS: assert platform in lower
        for op in ("status", "next", "help", "init", "phase"): assert f"sherpa-{op}" in text or f"/sherpa {op}" in text
    def canonical_source():
        for path in [CLAUDE, OPENCODE, *(KILO_DIR / f"{name}.md" for name in KILO_COMMANDS)]:
            assert "SKILL.md" in path.read_text(encoding="utf-8-sig"), str(path)
    def no_automatic_shell():
        for path in [CLAUDE, OPENCODE, *(KILO_DIR / f"{name}.md" for name in KILO_COMMANDS)]:
            content=path.read_text(encoding="utf-8-sig")
            assert "!`" not in content and "!{" not in content, str(path)
    def no_universal_claim():
        assert "exactly Claude Code, Kilo Code, and OpenCode" in DOCS.read_text(encoding="utf-8-sig")
    def argument_capability_honest():
        kilo_docs=(ROOT/"adapters/kilo/README.md").read_text(encoding="utf-8-sig")
        assert "does not document argument substitution" in kilo_docs

    def manifest_routes_and_adapters():
        commands = [item["command"] for item in MANIFEST["implemented"]]
        assert len(commands) == len(set(commands)), "duplicate implemented command"
        minimum = {"sherpa-status", "sherpa-next", "sherpa-help", "sherpa-init",
                   "sherpa-phase", "sherpa-config", "sherpa-config-check",
                   "sherpa-suggest", "sherpa-verify"}
        assert minimum <= set(commands), f"required command missing: {minimum - set(commands)}"
        planned = [item["command"] for item in MANIFEST["planned"]]
        assert not set(commands) & set(planned), "planned command collides with implemented command"
        for item in MANIFEST["implemented"]:
            workflow = item["workflow"].split("#", 1)[0]
            assert (ROOT / workflow).is_file(), f"missing workflow: {item['command']} -> {workflow}"
            assert item["operation"] and item["router_key"] and item["group"]
            assert all((ROOT / p).is_file() for p in (
                f".claude/skills/{item['command']}/SKILL.md",
                f".opencode/commands/{item['command']}.md",
                f".kilo/commands/{item['command']}.md"))
            for adapter in (ROOT / ".claude/skills" / item["command"] / "SKILL.md",
                            ROOT / ".opencode/commands" / f"{item['command']}.md",
                            ROOT / ".kilo/commands" / f"{item['command']}.md"):
                body = adapter.read_text(encoding="utf-8-sig")
                assert item["command"] in body and "SKILL.md" in body
                assert "!`" not in body and "!{" not in body
        for item in MANIFEST["planned"]:
            assert item["status"] == "planned"
            assert not (ROOT / ".opencode/commands" / f"{item['command']}.md").exists()
            assert not (KILO_DIR / f"{item['command']}.md").exists()
            assert not (CLAUDE_SKILLS / item["command"] / "SKILL.md").exists()

    def manifest_rejects_adversarial_registry_changes():
        cases = []
        duplicate = copy.deepcopy(MANIFEST); duplicate["implemented"].append(copy.deepcopy(duplicate["implemented"][0])); cases.append((duplicate, "duplicate canonical"))
        missing = copy.deepcopy(MANIFEST); missing["implemented"][0]["workflow"] = "workflows/not-real.md"; cases.append((missing, "missing workflow"))
        adapter = copy.deepcopy(MANIFEST); adapter["implemented"][0]["adapters"].remove("kilo"); cases.append((adapter, "all three host adapters"))
        name = copy.deepcopy(MANIFEST); name["implemented"][0]["command"] = "sherpa_Status"; cases.append((name, "invalid canonical"))
        collision = copy.deepcopy(MANIFEST); collision["implemented"][1]["legacy_aliases"] = collision["implemented"][0]["legacy_aliases"]; cases.append((collision, "duplicate command alias"))
        planned = copy.deepcopy(MANIFEST); planned["planned"][0]["command"] = planned["implemented"][0]["command"]; cases.append((planned, "colliding planned"))
        for mutated, expected in cases:
            errors = ROUTER.validate_manifest(mutated)
            assert any(expected in error for error in errors), (expected, errors)

    def command_docs_match_registry_and_runtime_limits():
        docs = (ROOT / "docs/commands/README.md").read_text(encoding="utf-8-sig")
        for item in MANIFEST["implemented"]:
            assert f"/{item['command']}" in docs
            assert item["workflow"] in docs
        for item in MANIFEST["planned"]:
            assert f"/{item['command']}" in docs and "PLANNED" in docs
        plain_docs = docs.replace("`", "")
        for host, record in MANIFEST["host_runtime_status"].items():
            assert record["status"] in {"PASS", "FAIL", "UNKNOWN", "NOT VERIFIED"}
            assert host.capitalize() in docs or host == "opencode" and "OpenCode" in docs
            assert record["evidence"] in plain_docs

    def framework_only_global_bundle_validates_without_adapter_folders():
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copy2(ROOT / "SKILL.md", root / "SKILL.md")
            for item in MANIFEST["implemented"]:
                relative = item["workflow"].split("#", 1)[0]
                source = ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            errors = ROUTER.validate_manifest(MANIFEST, root=root, check_adapter_files=False)
            assert not errors, errors

    return [("Claude Code native skill manifest",claude),("Kilo Code native workflow manifests",kilo),
            ("OpenCode native command manifest",opencode),("Exactly three adapter directories",adapters),
            ("Native project discovery paths exist",native_paths),("Core command map documented",docs_mapping),
            ("SKILL.md remains canonical source",canonical_source),("No command shell side effects",no_automatic_shell),
            ("No universal platform-support claim",no_universal_claim),("Kilo argument limitation stated",argument_capability_honest),
            ("Manifest mappings and three native adapter sets",manifest_routes_and_adapters),
            ("Manifest rejects duplicate, broken, colliding, and malformed records",manifest_rejects_adversarial_registry_changes),
            ("Command documentation matches registry and runtime evidence",command_docs_match_registry_and_runtime_limits),
            ("Framework-only global bundle validates without adapter folders",framework_only_global_bundle_validates_without_adapter_folders)]


def main() -> int:
    results=[]
    for name, test in tests():
        try: test(); results.append({"test":name,"status":"PASS","evidence":"executed static assertion"})
        except Exception as exc: results.append({"test":name,"status":"FAIL","evidence":f"{type(exc).__name__}: {exc}"})
    passed=sum(x["status"]=="PASS" for x in results)
    print(json.dumps({"suite":"sherpa Stage 1 native command manifests","scope":"static files only; no model execution or state mutation","results":results,"summary":{"total":len(results),"passed":passed,"failed":len(results)-passed}},indent=2))
    return 0 if passed==len(results) else 1

if __name__=="__main__":
    raise SystemExit(main())
