# Quickstart

Open the repository in a supported agent and invoke `/hackathonos help`, then `/hackathonos status` or `/hackathonos init`. Project state is created by the init workflow and stored in `.hackathon/`.

Install the published release with `irm https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.ps1 | iex` on Windows, or `curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/HackathonOS/main/distribution/install.sh | bash` on Linux/macOS. See [INSTALLATION.md](INSTALLATION.md) for agent-specific options.

After installing a release package, run `hackathonos doctor`, `hackathonos --version`, `hackathonos audit`, and `hackathonos clean --dry-run`.
