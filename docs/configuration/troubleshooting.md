# Configuration Troubleshooting

- `MISSING`: run `/sherpa init` from the intended project root, or add the named project configuration file.
- `PARTIALLY_CONFIGURED`: optional fields are absent; fill only from a reliable source or keep `UNKNOWN`.
- `INVALID`: inspect the reported field/path/line. Diagnostic output never includes secret values.
- Invalid timezone: use a supported IANA timezone name such as `Asia/Kolkata`; validation uses the runtime timezone database.
- `.env` tracked or not ignored: remove it from the Git index through your normal security process, rotate exposed credentials, and check history. The checker does not rewrite Git history.
- Human approval disabled: the checker emits a prominent warning. Restore `true` unless a human intentionally accepts the risk.
- Provider key appears missing: check the variable name and local `.env`/process environment. The utility reports only Configured/Missing and never tests provider connectivity.
- INIT preserves existing files. Back up and review manually before changing an existing value; INIT does not reset project state.
