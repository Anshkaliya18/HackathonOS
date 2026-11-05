# Record the 30-second demo

Save the finished GIF as `docs/public/sherpa.gif`, replacing the clearly labeled placeholder. Record only a real agent session; do not add scripted or invented verification output.

## Before recording

1. Use a disposable demo project opened in Claude Code or OpenCode. Install sherpa first with the pinned command in [INSTALLATION.md](../INSTALLATION.md); npmjs.org currently publishes `sherpa-skill@2.0.5`.
2. Give the demo project one small, inspectable feature and run its actual test command. Keep the source, test, and terminal result visible in the project so the agent can refer to them.
3. Close unrelated windows and hide secrets, personal paths, and notifications. Set the terminal font large enough to read at 1280×720 or larger.
4. Start a screen recorder (OBS, Kap, or another recorder) and capture the agent terminal and the demo project. VHS is not included because the interactive agent session requires a signed-in host and produces variable output; a scripted tape would not reliably show a genuine recommendation.

## Capture these moments

Keep the final edit to about 30 seconds. Use a shortened wait or edit out response latency, but keep the agent's actual words and test result intact.

| Time | Show |
|---|---|
| 0–4 s | Project name and “installed once, used in this project” context. Briefly show the successful installation result if it fits. |
| 4–10 s | Invoke `/sherpa init`; show the project state being initialized. |
| 10–17 s | Invoke `/sherpa suggest`; ask for a next step based on the current project and its test result. |
| 17–26 s | Show the recommendation and its evidence. It must cite the file or command output you actually showed, and label any missing evidence as unknown. |
| 26–30 s | Hold on the one-line install command and the repository/docs URL. |

## Export

Export a readable GIF at 960–1280 pixels wide, 12–18 fps, and about 30 seconds. Optimize the palette and keep the file small enough for GitHub. Save it to `docs/public/sherpa.gif`, then check the animation at its final display size and replace the first-screen placeholder in the README.
