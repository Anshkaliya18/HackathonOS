#!/usr/bin/env python3
"""Static validation of HackathonOS Stage 1 native command manifests.
Does not invoke an agent model, run a slash command, or mutate project state.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / ".claude/skills/hackathonos/SKILL.md"
KILO_DIR = ROOT / ".kilo/commands"
OPENCODE = ROOT / ".opencode/commands/hackathonos.md"
DOCS = ROOT / "commands/README.md"
ADAPTERS = ("claude", "kilo", "opencode")
KILO_COMMANDS = ("hackathonos", "hackathonos-status", "hackathonos-next", "hackathonos-help", "hackathonos-init", "hackathonos-phase")


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
        assert meta.get("name") == "hackathonos"
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
        assert CLAUDE.is_file() and OPENCODE.is_file() and all((KILO_DIR / f"{name}.md").is_file() for name in KILO_COMMANDS)
    def docs_mapping():
        text = DOCS.read_text(encoding="utf-8-sig")
        lower = text.lower()
        for platform in ADAPTERS: assert platform in lower
        for op in ("status", "next", "help", "init", "phase"): assert f"hackathonos-{op}" in text or f"/hackathonos {op}" in text
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
    return [("Claude Code native skill manifest",claude),("Kilo Code native workflow manifests",kilo),
            ("OpenCode native command manifest",opencode),("Exactly three adapter directories",adapters),
            ("Native project discovery paths exist",native_paths),("Core command map documented",docs_mapping),
            ("SKILL.md remains canonical source",canonical_source),("No command shell side effects",no_automatic_shell),
            ("No universal platform-support claim",no_universal_claim),("Kilo argument limitation stated",argument_capability_honest)]


def main() -> int:
    results=[]
    for name, test in tests():
        try: test(); results.append({"test":name,"status":"PASS","evidence":"executed static assertion"})
        except Exception as exc: results.append({"test":name,"status":"FAIL","evidence":f"{type(exc).__name__}: {exc}"})
    passed=sum(x["status"]=="PASS" for x in results)
    print(json.dumps({"suite":"HackathonOS Stage 1 native command manifests","scope":"static files only; no model execution or state mutation","results":results,"summary":{"total":len(results),"passed":passed,"failed":len(results)-passed}},indent=2))
    return 0 if passed==len(results) else 1

if __name__=="__main__":
    raise SystemExit(main())
