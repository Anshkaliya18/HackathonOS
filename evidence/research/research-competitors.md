# Research Evidence — GUIDE Core

**Evaluation date:** 2026-10-30 (UTC)  
**Hackathon:** Homingo Hack Days  
**Idea:** GUIDE Core — Travel discovery app surfacing underrated nearby destinations using OpenStreetMap + AI analysis

---

## External Research (Competitors, Existing Solutions, Market Saturation)

Web search was attempted for: "travel app discover hidden gems nearby destinations OpenStreetMap", "underrated travel destinations app discovery", "underrated locations guide travel app GitHub OpenStreetMap Overpass". No results were returned. Per the IDEA-EVALUATE workflow rules, all external claims are marked `UNKNOWN`.

| # | Claim | Type | Source | Confidence |
|---|-------|------|--------|------------|
| 1 | Existing competitors in the underrated-destination travel app space | UNKNOWN | Web search (no results) | low |
| 2 | Market saturation for travel discovery apps | UNKNOWN | Web search (no results) | low |
| 3 | Similar hackathon projects in this category | UNKNOWN | Web search (no results) | low |
| 4 | Open-source alternatives for OSM-based destination discovery | UNKNOWN | Web search (no results) | low |

## Repository Evidence (FACT — directly inspected)

| # | Claim | Type | Source | Confidence |
|---|-------|------|--------|------------|
| 1 | Backend: `src/guide_app.py` implements `EarthExplorerEngine` with Nominatim geocoding, Overpass API queries, and geodesic distance scoring | FACT | `src/guide_app.py` lines 390-542 | high |
| 2 | API endpoints: `/api/health`, `/api/geocode`, `/api/reverse`, `/api/search` | FACT | `src/guide_app.py` lines 580-663 | high |
| 3 | Frontend: `web/` contains CesiumJS-based HTML/JS files (`index.html`, `explore.html`, `about.html`, `saved.html`, `chat.html`) | FACT | `web/` directory listing | high |
| 4 | Tests: `tests/test_guide_app.py` — 9/9 tests passed (executed) | FACT | `tests/test_guide_app.py` execution result | high |
| 5 | Config: `config/config.json` configures OpenRouter provider (`openai/gpt-oss-120b:free`), search settings, categories, boost factors | FACT | `config/config.json` | high |
| 6 | `EarthExplorerEngine` does NOT call OpenRouter/LLM — it uses Nominatim (OpenStreetMap) and Overpass API only | FACT | `src/guide_app.py` lines 62-74, 390-542 | high |
| 7 | `UnderratedGuideApp` class accepts `api_key` but docstring states it is "stored for completeness but not used in the current test suite" | FACT | `src/guide_app.py` lines 728-730 | high |
| 8 | README claims "AI-Powered Analysis - Uses OpenRouter API with advanced LLMs" | FACT | `docs/README.md` lines 33, 48-56 | high |
| 9 | Two MP4 video files exist in `web/` (~103 MB and ~112 MB) | FACT | `web/` directory listing | high |
| 10 | `.env` file present (gitignored) for secrets | FACT | Repository root | high |
| 11 | No deployment configuration found in repository | FACT | Repository inspection | high |
| 12 | `package.json` declares `cesium: ^1.142.0` | FACT | `package.json` | high |
| 13 | `requirements.txt` declares `requests>=2.31.0`, `geopy>=2.3.0` | FACT | `requirements.txt` | high |

## Team Input (source: team input via /hackathonos init and idea-evaluate)

| # | Claim | Type | Source | Confidence |
|---|-------|------|--------|------------|
| 1 | Problem: "GUIDE is a travel discovery platform designed to help users discover interesting and underrated destinations through an interactive exploration experience" | INFERENCE | team input / `.hackathon/project-state.md` | medium |
| 2 | Target users: "Travelers, explorers, and users looking for underrated destinations and travel discovery" | INFERENCE | team input / `.hackathon/project-state.md` | medium |
| 3 | Solution includes "AI analysis" component | INFERENCE | team input (idea description) | medium |
| 4 | Hackathon: Homingo Hack Days, submission deadline 6 Dec 2026 11:59 PM IST, registration deadline 15 Nov 2026 | INFERENCE | team input / `.hackathon/project-state.md` | medium |
| 5 | Judging criteria: Track-specific (Agents, Automation, LLM Apps) + Cross-track (problem fit, technical depth, demo quality) | FACT | team input / `.hackathon/project-state.md` | high |
