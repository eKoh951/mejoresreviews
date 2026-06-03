# 01 — Installation Plan

Per tool: **why · source · install · credentials · permissions · risk level · safer alternative.** Tools are ordered by setup priority. Risk levels: 🟢 low · 🟡 medium · 🔴 high.

> **Vetting rule for ANY third-party MCP:** before install, check repo activity, recent commits, open security issues, and stars; pin an exact version/commit; run sandboxed; grant the narrowest permission; never expose secrets in args. If you can't verify it, prefer a first-party SDK called from a Python script over a random MCP.

---

## Tier 1 — Core local (install first, lowest risk)

### Filesystem MCP
- **Why:** read/write datasets, markdown reports, CSV exports in this repo.
- **Source:** `@modelcontextprotocol/server-filesystem` (official MCP servers org).
- **Install:** configure in `~/.claude/settings.json` `mcpServers`, scope it to `C:\Users\great\Documents\code\mejoresreviews` only.
- **Credentials:** none.
- **Permissions:** restrict root to the project dir. Do **not** grant access to the home directory.
- **Risk:** 🟢 (🟡 if rooted too broadly — your home dir contains many private folders; scope tightly).
- **Safer alternative:** Claude Code's built-in Read/Write/Edit tools already cover this; the MCP is optional.

### Git / GitHub MCP (or just `gh` CLI — already installed)
- **Why:** version scripts, datasets, docs; issues for the research log; PRs for review.
- **Source:** `gh` CLI is installed and authenticated (account `eKoh951`). Official GitHub MCP server exists if you want tool-level access.
- **Install:** `gh` already works. GitHub MCP: `github/github-mcp-server` (check it's the official one).
- **Credentials:** existing `gh` token (scopes: repo, read:org, workflow, gist).
- **Permissions:** fine as-is. For automation prefer a fine-grained PAT limited to this repo.
- **Risk:** 🟢.
- **Safer alternative:** plain `gh` + git via the Bash tool (recommended — no extra MCP surface).

### Python environment + DuckDB
- **Why:** all ETL, normalization, and analytics. DuckDB = free, fast, local SQL over Parquet/CSV; no server.
- **Source:** PyPI.
- **Install:** `python -m venv .venv` then `pip install duckdb pandas pyarrow python-dotenv unidecode rapidfuzz`.
- **Credentials:** none.
- **Risk:** 🟢.
- **Alternative:** SQLite (less analytical power) — DuckDB is the right call here.

---

## Tier 2 — Storage & dashboard

### Convex
- **Why:** curated store + reactive dashboard backend (your choice).
- **Source:** `convex` (npm) for schema/functions; `convex` (PyPI) HTTP client for Python writes.
- **Install:** `npm create convex@latest` for the project; `pip install convex` for the ETL writer.
- **Credentials:** Convex deploy key in `.env` (`CONVEX_URL`, `CONVEX_DEPLOY_KEY`). Never in prompts.
- **Permissions:** ETL uses a write-scoped function key; dashboard read uses public/queries only.
- **Risk:** 🟡 — Convex schema is TypeScript-first; Python writes go through generated HTTP mutations, which adds a moving part. **Honest note:** keep heavy analytics in DuckDB, use Convex only for curated records + dashboard (see [`03-schema.md`](03-schema.md)).
- **Safer alternative for analytics:** none needed — DuckDB already covers it; Convex is the presentation/curation layer.

---

## Tier 3 — Demand & search data connectors (Python scripts, not MCPs)

### Google Ads API connector  ⏳ start approval Day 1
- **Why:** the only first-party source of keyword search volume, competition index, and bid ranges with geo + language targeting.
- **Source:** official `google-ads` Python library (PyPI).
- **Install:** `pip install google-ads`.
- **Credentials:** Google Ads account + **developer token** (apply in API Center), OAuth2 client (client_id/secret/refresh_token), login-customer-id. All in `.env`.
- **Permissions:** read-only use of `KeywordPlanIdeaService` (generateKeywordIdeas / generateKeywordHistoricalMetrics). No campaign mutations.
- **Risk:** 🟡 — developer-token approval is human-gated and can take days; **basic access** has limited daily operations. Volume numbers are **bucketed/rounded** — directional, not exact (see matrix).
- **Safer alternative:** if approval stalls, use SERP-API keyword endpoints or DataForSEO for volume estimates (clearly label as third-party inferred, lower confidence).

### SERP / Web search connector
- **Why:** programmatic SERP, related questions, competitor pages, snippet+URL capture.
- **Source (fits $50–150/mo):** **Serper.dev** (cheapest, ~$50/50k queries) or **DataForSEO**; **SerpApi** if you want richer parsing (pricier).
- **Install:** plain HTTP via `requests`; or their Python SDK.
- **Credentials:** API key in `.env`.
- **Permissions:** read-only query API. Respect their rate limits.
- **Risk:** 🟢 (compliant — these vendors handle Google ToS on their side).
- **Safer alternative:** manual Google searches with screenshot + URL logging (slow, free).

### Reddit connector
- **Why:** exact phrasing, pains, objections, agency complaints, DIY workflows.
- **Source:** official Reddit API via `praw` (PyPI).
- **Install:** `pip install praw`.
- **Credentials:** Reddit OAuth app (client_id/secret, user-agent) in `.env`.
- **Permissions:** read-only. Store **aggregated themes**, not personal usernames.
- **Risk:** 🟡 — Reddit API has rate limits and commercial-use terms; keep volume low and research-only.
- **Safer alternative:** manual reading of threads with URL + date capture.

### YouTube Data API connector
- **Why:** find local-SEO/review-tutorial videos, titles, descriptions, comment themes (Spanish phrasing).
- **Source:** YouTube Data API v3 (`google-api-python-client`).
- **Install:** `pip install google-api-python-client`.
- **Credentials:** API key in `.env`. Free quota ~10k units/day.
- **Permissions:** read-only `search.list`, `videos.list`, `commentThreads.list`.
- **Risk:** 🟢.
- **Alternative:** SERP API video results.

### Google Trends collector  (isolate)
- **Why:** relative demand, regional comparison, seasonality, "reseñas" vs "reviews" vs "opiniones".
- **Source:** **no official API.** `pytrends` (unofficial) or manual CSV export from trends.google.com.
- **Install:** `pip install pytrends` — but treat as fragile.
- **Credentials:** none.
- **Permissions:** n/a.
- **Risk:** 🔴 *reliability* (unofficial, breaks/blocks without warning) — **not** a legal risk for public Trends data, but never treat Trends as exact volume.
- **Safer alternative:** **manual export** from the Trends UI is the reliable path; run `pytrends` as a convenience only, isolated so failure can't break the pipeline.

---

## Tier 4 — Browser automation & TikTok

### Browser automation MCP (Playwright)
- **Why:** assisted collection of TikTok Creative Center / Top Ads and public pages; screenshots for evidence.
- **Source:** official Playwright MCP (`@playwright/mcp` / `microsoft/playwright-mcp`) — verify it's the Microsoft one.
- **Install:** per its README; `playwright install` for browsers.
- **Credentials:** none — **do not** log into personal accounts in the automation browser.
- **Permissions:** start with **no** persistent profile; human-in-the-loop confirmation for each navigation in gray areas.
- **Risk:** 🔴 — automating logged-in or rate-limited sites can violate ToS and get IPs blocked. Use only on **public** pages, human-supervised, and respect robots/ToS.
- **Safer alternative:** fully manual collection (open the page yourself, paste data) — slower but unambiguous.

### TikTok Creative Center (Keyword Insights + Top Ads)
- **Why:** ad keyword popularity, top creatives, hooks, CTAs, offers, formats.
- **Source:** `ads.tiktok.com/business/creativecenter` — **no official public API**; access via supervised Playwright or manual.
- **Credentials:** none for public Creative Center views.
- **Risk:** 🔴 ToS — automated extraction is gray. Prefer **manual/semi-manual**; keep volumes tiny; label everything **ads-based, not organic search volume**.
- **Safer alternative:** manual browsing with structured note capture into `tiktok_videos`/`tiktok_themes`.

### TikTok Research API
- **Status:** **likely unavailable** for this project. Gated to vetted academic/nonprofit researchers in eligible regions; **not** intended for commercial market research. Do not assume access.
- **Action:** treat TikTok organic data as **manual, public-only, aggregate-theme** collection. No personal data on commenters.

---

## Do NOT install without explicit vetting

Any community MCP for "TikTok scraping", "Google Maps scraping", "review automation", or "keyword volume" that is not a first-party SDK. These are the highest-risk surface (credential theft, ToS violation, malware). Default to **first-party API + Python script** instead of a convenience MCP.

## Secrets & security checklist (applies to all)

- [ ] `.env` git-ignored; `.env.example` committed with empty keys.
- [ ] Pre-commit secret scanner (e.g. `gitleaks`) before first push.
- [ ] Read-only / minimal-scope credentials everywhere.
- [ ] Browser automation never uses personal logins.
- [ ] Pin MCP/tool versions; re-vet on upgrade.
- [ ] Log source URL + collection date for every record.
- [ ] No personal data from commenters stored — aggregate themes only.
