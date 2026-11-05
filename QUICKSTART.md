# Quickstart

Open the repository in a supported agent and invoke `/sherpa help`, then `/sherpa status` or `/sherpa init`. Project state is created by the init workflow and stored in `.sherpa/`.

Install the published release with `irm https://raw.githubusercontent.com/Anshkaliya18/Sherpa/main/distribution/install.ps1 | iex` on Windows, or `curl -fsSL https://raw.githubusercontent.com/Anshkaliya18/Sherpa/main/distribution/install.sh | bash` on Linux/macOS. See [INSTALLATION.md](INSTALLATION.md) for agent-specific options.

After installing a release package, run `sherpa doctor`, `sherpa --version`, `sherpa audit`, and `sherpa clean --dry-run`.
