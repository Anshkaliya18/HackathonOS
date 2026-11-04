# From sherpa to Sherpa

Sherpa changes the product command to `/sherpa`, the management binary to `sherpa`, and project state to `.sherpa/`.

If an older project has `.hackathon/` and no `.sherpa/`, Sherpa reads the old directory for one release and reports a deprecation notice. Run `sherpa migrate` to copy the full tree after confirmation. Migration refuses to overwrite `.sherpa/` and leaves the source untouched. Do not remove the legacy folder until you have reviewed the copied data.

Use the uppercase `SHERPA_*` installer variables. Former `sherpa_*` names remain accepted as fallbacks for this release. Generic event variables such as `HACKATHON_NAME` are unchanged.

The deprecated `sherpa` CLI shim prints “sherpa is now Sherpa” and forwards to `sherpa`. The npm package is `sherpa-skill` because the `sherpa` package name is taken. Runtime support statuses remain as recorded in the [compatibility guide](/agents/).

See the complete [migration reference](https://github.com/Anshkaliya18/HackathonOS/blob/main/MIGRATION.md).
