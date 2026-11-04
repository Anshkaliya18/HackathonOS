# Quickstart

Open the repository in a supported agent and invoke `/hackathonos help`, then `/hackathonos status` or `/hackathonos init`. Project state is created by the init workflow and stored in `.hackathon/`.

A public one-line installer is not currently usable: the checked-in release manifest is a template with no published artifacts or real checksums. See [INSTALLATION.md](INSTALLATION.md) for source setup and release prerequisites.

After installing a release package, run `hackathonos doctor`, `hackathonos --version`, `hackathonos audit`, and `hackathonos clean --dry-run`.
