# Name options

These alternatives emphasize an installable agent skill rather than a project built during a hackathon. Availability checks were run on 2026-11-04 using `npm view <name>` and the GitHub repository endpoint `https://api.github.com/repos/Anshkaliya18/<name>`. npm returned `E404` for each; GitHub returned HTTP 404 for each under the current owner. These results are a snapshot, not a reservation or trademark check.

| Name | Rationale | npm check | GitHub repo check |
|---|---|---|---|
| `hackathon-mentor-skill` | Says both what it does and that it is an installable skill. | `npm view hackathon-mentor-skill` → E404, no package found | `Anshkaliya18/hackathon-mentor-skill` → HTTP 404 |
| `hackathonos-skill` | Keeps the existing product identity and identifies the global skill. | `npm view hackathonos-skill` → E404, no package found | `Anshkaliya18/hackathonos-skill` → HTTP 404 |
| `hackathonos-cli` | Clear fit for the `npx … install` entry point while retaining HackathonOS. | `npm view hackathonos-cli` → E404, no package found | `Anshkaliya18/hackathonos-cli` → HTTP 404 |
| `hackathon-agent-coach` | Signals an agent-facing coaching tool with broad hackathon coverage. | `npm view hackathon-agent-coach` → E404, no package found | `Anshkaliya18/hackathon-agent-coach` → HTTP 404 |
| `hackathon-coach` | Short and understandable as an agent skill that coaches hackathon teams. | `npm view hackathon-coach` → E404, no package found | `Anshkaliya18/hackathon-coach` → HTTP 404 |
| `hackathon-mentor` | Directly describes the globally reusable mentor role. | `npm view hackathon-mentor` → E404, no package found | `Anshkaliya18/hackathon-mentor` → HTTP 404 |
| `judging-impact` | Centers the skill's decision lens: improving judging outcomes with limited time. | `npm view judging-impact` → E404, no package found | `Anshkaliya18/judging-impact` → HTTP 404 |
| `build-for-hackathons` | Describes the work the skill supports without implying a single event project. | `npm view build-for-hackathons` → E404, no package found | `Anshkaliya18/build-for-hackathons` → HTTP 404 |

## Recommendation

`hackathon-mentor-skill` is the clearest public-facing alternative for a globally installed agent skill. `hackathonos-cli` is a practical package name for the current npx installer while preserving HackathonOS; it does not rename the GitHub repository or the skill. Confirm availability again immediately before publishing or selecting a final public brand.
