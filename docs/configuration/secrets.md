# Secret Handling

Never commit `.env`, `*.key`, `*.pem`, `credentials.json`, `service-account.json`, or `secrets.json`. The project `.gitignore` protects these names while allowing `.env.example` files.

The secret scanner detects common API-key/token/private-key/password patterns and sensitive credential filenames. It is heuristic and not exhaustive. Reports include finding type and path/line only, never the matched value. `.env` itself is excluded from source-content scanning because it is the designated local secret store; config checking separately verifies that it is ignored and not Git-tracked.

Use bounded wording: “No known secret patterns were detected in the scanned scope.” This is not proof that no secrets exist. External provider connectivity is never inferred from a configured key.
