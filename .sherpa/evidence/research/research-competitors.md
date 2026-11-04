# Research Evidence — GUIDE Core

**Evaluation date:** 2026-11-01 (UTC)  
**Hackathon:** Homingo Hack Days  
**Idea:** GUIDE Core — Travel discovery app surfacing underrated nearby destinations using OpenStreetMap + AI analysis  
**Research query:** competitors

---

## 1. Research Evidence

List all external research used to support dimension scores. Each entry must be tagged FACT / INFERENCE / ASSUMPTION / UNKNOWN with a source.

| # | Claim | Type | Source | Confidence |
|---|-------|------|--------|-----------|
| 1 | Existing competitors in underrated-destination travel app space | UNKNOWN | Web search (no results) | low |
| 2 | Market saturation for travel discovery apps | UNKNOWN | Web search (no results) | low |
| 3 | Similar hackathon projects in this category | UNKNOWN | Web search (no results) | low |
| 4 | Open-source alternatives for OSM-based destination discovery | UNKNOWN | Web search (no results) | low |

## 2. Repository Evidence (FACT — directly inspected)

| # | Claim | Type | Source | Confidence |
|---|-------|------|--------|-----------|
| 1 | Backend: `src/guide_app.py` implements `EarthExplorerEngine` with Nominatim geocoding, Overpass API queries, and geodesic distance scoring | FACT | `src/guide_app.py` lines 390-542 | high |
| 2 | API endpoints: `/api/health`, `/api/geocode`, `/api/reverse`, `/api/search` | FACT | `src/guide_app.py` lines 580-663 | high |
| 3 | Frontend: `web/` contains CesiumJS-based HTML/JS files (`index.html`, `explore.html`, `about.html`, `saved.html`, `chat.html`) | FACT | `web/` directory listing | high |
| 4 | Config: `config/config.json` configures OpenRouter provider (`openai/gpt-oss-120b:free`), search settings, categories, boost factors | FACT | `config/config.json` | high |
| 5 | `EarthExplorerEngine` does NOT call OpenRouter/LLM — it uses Nominatim (OpenStreetMap) and Overpass API only | FACT | `src/guide_app.py` lines 62-74, 390-542 | high |
| 6 | `UnderratedGuideApp` class accepts `api_key` but docstring states it is "stored for completeness but not used in the current test suite" | FACT | `src/guide_app.py` lines 728-730 | high |
| 7 | Two MP4 video files exist in `web/` (~103 MB and ~112 MB) | FACT | `web/` directory listing | high |
| 8 | `.env` file present (gitignored) | FACT | Repository root | high |
| 9 | `package.json` declares `cesium: ^1.142.0` | FACT | `package.json` | high |
| 10 | `requirements.txt` declares `requests>=2.31.0`, `geopy>=2.3.0` | FACT | `requirements.txt` | high |

---

## 3. Research Findings

### What is Known (FACT)

| # | Claim | Source | Confidence |
|---|-------|--------|-----------|
| 1 | The backend `EarthExplorerEngine` queries Nominatim geocoding API at `https://nominatim.openstreetmap.org/search` | `src/guide_app.py` line 62, 399 | high |
| 2 | The backend queries Overpass API at `https://overpass-api.de/api/interpreter` for POI search | `src/guide_app.py` line 64, 471 | high |
| 3 | The backend computes geodesic distance using `geopy.distance.geodesic` | `src/guide_app.py` line 500 | high |
| 4 | The frontend uses CesiumJS `^1.142.0` for 3D map visualization | `package.json` line 3, `web/` directory | high |
| 5 | Results are filtered by quality score threshold `MIN_CURATED_SCORE = 55.0` | `src/guide_app.py` line 102 | high |
| 6 | Results are capped at `MAX_CURATED_RESULTS = 8` curated places | `src/guide_app.py` line 103 | high |
| 7 | Categories include: Viewpoint, Nature, Park, Museum, Historic, Market, Religious, Tourism, Other | `src/guide_app.py` lines 78-88 | high |
| 8 | Quality scoring uses distance (0-40 points) + category weights (18-36 points) + quality metadata bonuses | `src/guide_app.py` lines 368-387 | high |
| 9 | Low-value tags (toilets, parking, benches, etc.) are filtered out with -40 penalty | `src/guide_app.py` lines 126-147 | high |
| 10 | Results are deduplicated by name + coordinates + category | `src/guide_app.py` lines 363-365, 504-507 | high |

### What is Reasonable (INFERENCE)

| # | Claim | Reasoning | Evidence | Confidence |
|---|-------|-----------|----------|-----------|
| 1 | The app does NOT use OpenRouter/LLM for location discovery | `EarthExplorerEngine` uses Nominatim + Overpass only; `api_key` "stored for completeness but not used" | `src/guide_app.py` lines 62-74, 390-542, 728-730 | high |
| 2 | The "AI-Powered Analysis" claim in README is misleading regarding actual implementation | README claims "AI-Powered Analysis" but engine uses OSM only | `docs/README.md` line 33; `src/guide_app.py` lines 62-74 | high |
| 3 | The scoring system is distance-weighted (closer = higher score) with category bonuses | `_quality_score()` function at `src/guide_app.py` lines 368-387 | high |
| 4 | Category weights favor Viewpoint (36) and Nature (32) over Other (0) | `QUALITY_CATEGORY_WEIGHTS` at `src/guide_app.py` lines 90-100 | high |
| 5 | Low-value tags (toilets, parking, benches, etc.) are filtered out with -40 penalty | `src/guide_app.py` lines 126-147 | high |

### What is Assumed (ASSUMPTION)

| # | Claim | Why assumed | Must be verified? |
|---|-------|-------------|-------------------|
| 1 | OpenStreetMap data quality is sufficient for travel discovery in most cities | OSM is widely used and has good coverage in urban areas | Yes — verify with test searches |
| 2 | Users will find "underrated" destinations more valuable than popular ones | Problem statement assumes underrated destinations are valuable | Yes — validate with user testing |
| 3 | The scoring system (distance + category weights) produces meaningful rankings | Score combines distance (0-40) + category weights (18-36) + quality bonuses | Yes — validate with user testing |

### What is Unknown (UNKNOWN)

| # | What is unknown | Why it matters |
|---|-----------------|----------------|
| 1 | Competitor products in underrated-destination space | Web search returned no results; need manual research |
| 2 | Market saturation for travel discovery apps | No market research data available |
| 3 | OSM data quality in target Indian cities (Homingo Hack Days is India-based) | Need to verify OSM coverage in Indian cities |
| 4 | User willingness to use underrated destination discovery | No user research conducted yet |
| 5 | OpenRouter API availability and pricing for chatbot feature | Need to check OpenRouter pricing and availability in India |

### Contradictions Found

| # | Claim A | Evidence A | Claim B | Evidence B | Resolution |
|---|---------|------------|---------|------------|------------|
| 1 | README claims "AI-Powered Analysis using OpenRouter API" | `docs/README.md` line 33 | `EarthExplorerEngine` uses Nominatim + Overpass only, not OpenRouter | `src/guide_app.py` lines 62-74, 390-542 | **CONTRADICTION** — README claims AI-powered analysis using OpenRouter API, but backend engine does not call OpenRouter at all. The `api_key` field is "stored for completeness but not used." |

---

## 4. Decision-Relevant Fields

**Recommended outcome:** The idea (GUIDE Core) has technical feasibility but the AI claim is unsupported by implementation. The backend engine (`EarthExplorerEngine`) implements OSM-based discovery with scoring, dedup, and category filtering. However, the README claims "AI-Powered Analysis using OpenRouter API" which is not implemented in the engine. The `api_key` field exists but is not used.

**Why this outcome:** The backend engine (`EarthExplorerEngine`) implements OSM-based discovery with scoring, dedup, and category filtering. However, the README claims "AI-Powered Analysis using OpenRouter API" which is not implemented in the engine. The `api_key` field exists but is not used.

**What must be true for this to succeed:**
1. Either implement real OpenRouter/LLM integration for AI-powered analysis
2. Or remove the AI claim from README and reposition as pure OSM-based discovery
3. Verify OSM data quality in Indian cities (Homingo Hack Days is India-based)

**Recommended next action:** Resolve the AI claim (implement OpenRouter integration OR remove the AI claim), then re-evaluate the idea.

---

## 5. Human Confirmation

**Human confirmation status:** pending  
**Confirmed by:** pending  
**Confirmed at:** pending

**Rule:** Only explicit human confirmation can act on research findings. The engine recommends; the human decides. No automatic overwrite.
