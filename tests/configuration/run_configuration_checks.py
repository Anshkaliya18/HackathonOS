#!/usr/bin/env python3
"""Stage 2 configuration checks; uses temporary fixtures and no external services."""
from __future__ import annotations
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("hackathonos_config", ROOT / "core/configuration/manager.py")
manager = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = manager
SPEC.loader.exec_module(manager)


def run():
    checks=[]
    def check(name, fn):
        try: fn(); checks.append({"test":name,"status":"PASS"})
        except Exception as exc: checks.append({"test":name,"status":"FAIL","evidence":f"{type(exc).__name__}: {exc}"})
    def missing():
        with tempfile.TemporaryDirectory() as d:
            snap=manager.config_snapshot(Path(d),process_env={})
            assert snap["status"]=="MISSING", snap
    def initialize_non_destructive():
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'.hackathon').mkdir(); (root/'.hackathon/settings.json').write_text('{"sentinel":"keep"}')
            (root/'.hackathon/project-state.md').write_text('human state')
            created,preserved=manager.init_project(root)
            assert '.hackathon/settings.json' in preserved and '.hackathon/project-state.md' in preserved
            assert json.loads((root/'.hackathon/settings.json').read_text())=={"sentinel":"keep"}
            assert (root/'.hackathon/project-state.md').read_text()=='human state'
            assert (root/'.hackathon/hackathon.json').exists() and (root/'.env.example').exists()
            second,_=manager.init_project(root)
            assert not second
    def env_parser():
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'.env'; p.write_text('A=one\nexport B="two words"\nC=three # comment\nA=duplicate\nBAD LINE\nD=\'open\n')
            values,issues=manager.parse_env_file(p)
            assert values=={'A':'one','B':'two words','C':'three'}, values
            assert len(issues)==3, issues
    def precedence_and_validation():
        assert manager.resolve_value('override','json','process','dotenv','default')=='override'
        assert manager.resolve_value(None,'json','process','dotenv','default')=='json'
        assert manager.resolve_value(None,None,'process','dotenv','default')=='process'
        assert manager.resolve_value(None,None,None,None,'default')=='default'
        assert manager.resolve_value(None,None,None,None)=='UNKNOWN'
        assert manager.validate_url('https://example.invalid')=='CONFIGURED'
        assert manager.validate_url('javascript:alert(1)')=='INVALID'
        assert manager.validate_deadline('2026-11-01T12:00:00+05:30')=='CONFIGURED'
        assert manager.validate_deadline('soon')=='INVALID'
        assert manager.validate_timezone('Asia/Kolkata')=='CONFIGURED'
        assert manager.validate_timezone('Not/AZone')=='INVALID'
    def scanner_redacts():
        marker='ghp_'+'A'*36
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'notes.md').write_text('token '+marker+'\n')
            (root/'.env').write_text('AI_API_KEY='+marker+'\n')
            findings=manager.scan_secrets(root)
            assert findings and marker not in json.dumps(findings), findings
            assert manager.scan_secrets(root)==findings
    def configured_defaults_and_bad_values():
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); manager.init_project(root)
            snap=manager.config_snapshot(root,process_env={})
            assert snap['status']=='PARTIALLY_CONFIGURED',snap
            assert snap['fields']['Human approval'] is True
            (root/'.env').write_text('ENABLE_AUTO_VERIFY=maybe\nMAX_AUTO_ITERATIONS=999\n')
            snap=manager.config_snapshot(root,process_env={})
            assert snap['status']=='INVALID' and any('expected true or false' in e for e in snap['errors'])
            assert any('between 1 and 20' in e for e in snap['errors'])
            settings=json.loads((root/'.hackathon/settings.json').read_text())
            settings['autonomous_loop']['require_human_approval']=False
            (root/'.hackathon/settings.json').write_text(json.dumps(settings))
            (root/'.env').write_text('MAX_AUTO_ITERATIONS=-1\nREQUIRE_HUMAN_APPROVAL=false\n')
            snap=manager.config_snapshot(root,process_env={})
            assert any('between 1 and 20' in e for e in snap['errors'])
            assert any('Human approval is disabled' in w for w in snap['warnings'])
    def overview_redacts():
        from io import StringIO
        import contextlib
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); manager.init_project(root)
            marker='secret-value-never-print'
            (root/'.env').write_text('AI_API_KEY='+marker+'\n')
            snap=manager.config_snapshot(root,process_env={})
            out=StringIO()
            with contextlib.redirect_stdout(out): manager.print_overview(snap)
            assert marker not in out.getvalue() and 'AI credential: Configured' in out.getvalue()
    def malformed_config_and_adversarial_files():
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); manager.init_project(root)
            (root/'.hackathon/hackathon.json').write_text('{broken')
            (root/'README.md').write_text('Bearer '+'X'*32)
            (root/'service-account.json').write_text('{}')
            json_marker='AIza'+'B'*35
            (root/'config.json').write_text(json.dumps({'credential':json_marker}))
            snap=manager.config_snapshot(root,process_env={})
            assert snap['status']=='INVALID'
            assert any('malformed JSON' in e for e in snap['errors'])
            assert any('Bearer token' in f for f in snap['secret_findings'])
            assert any('sensitive credential file' in f for f in snap['secret_findings'])
            assert any('Google API key' in f and 'config.json' in f for f in snap['secret_findings'])
            assert 'X'*32 not in json.dumps(snap) and json_marker not in json.dumps(snap)
    def tracked_env_and_ignore():
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); manager.init_project(root)
            subprocess.run(['git','init','-q'],cwd=root,check=True)
            assert manager.is_env_ignored(root)
            (root/'.env').write_text('A=1\n')
            subprocess.run(['git','add','-f','.env'],cwd=root,check=True)
            assert manager.tracked_env(root)
            snap=manager.config_snapshot(root,process_env={})
            assert any('tracked by Git' in e for e in snap['errors'])
    def stage2_routes_exist():
        spec=importlib.util.spec_from_file_location('hackathonos_route_contract',ROOT/'core/commands/router.py')
        routes=importlib.util.module_from_spec(spec); sys.modules[spec.name]=routes; spec.loader.exec_module(routes)
        assert routes.resolve('config').operation=='CONFIG'
        assert routes.resolve('config').workflow=='workflows/configuration.md'
        assert routes.resolve('config check').operation=='CONFIG CHECK'
        assert routes.resolve('config check').workflow=='workflows/configuration.md'
        assert routes.resolve('config').workflow=='workflows/configuration.md'
        assert routes.resolve('config check').workflow=='workflows/configuration.md'
        assert routes.resolve('status').operation=='STATUS'
        assert routes.resolve('next').operation=='NEXT'
        assert routes.resolve('help').operation=='HELP'
        assert routes.resolve('init').operation=='INIT'
        assert routes.resolve('phase').operation=='PHASE'
        assert routes.resolve('suggest').operation=='SUGGEST'
        assert not (ROOT/'.kilo/commands/hackathonos-config.md').exists()
        assert not (ROOT/'.kilo/commands/hackathonos-config-check.md').exists()
    def cli_subcommands_work_on_fixture():
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            script=ROOT/'core/configuration/manager.py'
            init=subprocess.run([sys.executable,str(script),'--project-root',str(root),'init'],capture_output=True,text=True)
            assert init.returncode==0 and '.hackathon/settings.json' in init.stdout
            config=subprocess.run([sys.executable,str(script),'--project-root',str(root),'config'],capture_output=True,text=True)
            assert config.returncode==0 and 'HACKATHONOS CONFIGURATION' in config.stdout
            check=subprocess.run([sys.executable,str(script),'--project-root',str(root),'check'],capture_output=True,text=True)
            assert check.returncode==0 and 'Secret scan: PASS' in check.stdout
    def framework_init_refused():
        try: manager.init_project(ROOT)
        except ValueError as exc: assert 'refusing to initialize' in str(exc)
        else: raise AssertionError('framework root was initialized')
    for name,fn in [
        ('missing config status',missing),('INIT preserves existing state and settings',initialize_non_destructive),
        ('dotenv parsing and diagnostics',env_parser),('precedence and field validators',precedence_and_validation),
        ('secret scan redacts matching values and skips .env content',scanner_redacts),
        ('safe defaults and invalid environment values',configured_defaults_and_bad_values),
        ('configuration overview redacts credentials',overview_redacts),('malformed JSON and adversarial secret files',malformed_config_and_adversarial_files),('tracked .env detection and ignore rule',tracked_env_and_ignore),('Stage 2 routes exist on all adapters',stage2_routes_exist),('config, config check, and init CLI operations',cli_subcommands_work_on_fixture),('framework root initialization guard',framework_init_refused)]: check(name,fn)
    total=len(checks); passed=sum(x['status']=='PASS' for x in checks)
    print(json.dumps({'suite':'HackathonOS Stage 2 configuration','scope':'temporary fixtures; standard library; no network or provider calls','results':checks,'summary':{'total':total,'passed':passed,'failed':total-passed}},indent=2))
    return 0 if passed==total else 1

if __name__=='__main__': raise SystemExit(run())
