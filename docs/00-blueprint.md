# 00 — Research System Blueprint

## Design principles

1. **Separation of layers.** Raw collected data ≠ normalized data ≠ analysis ≠ conclusions. Each lives in its own place and is never silently overwritten.
2. **Every claim is sourced.** No insight survives without a URL/API origin, a collection date, a confidence score, and a data-type label (official / ads / organic / anecdotal).
3. **Skeptic has veto.** The Compliance/Skeptic agent can block any conclusion and force a "what would change our mind" note.
4. **Compliant-by-construction.** Fake reviews and bought reviews are filtered *at intake* as a labeled intent, never as a recommended tactic.
5. **Automate the safe and boring; keep humans on the risky and ambiguous.** Anything touching ToS-gray scraping or personal data is manual/semi-manual by default.

## Architecture (text diagram)

```
                         ┌───────────────────────────────────────────────┐
                         │           RESEARCH ORCHESTRATOR                 │
                         │  research plan · task routing · research log    │
                         │  assumptions register · dedup of work           │
                         └───────────────┬───────────────────────────────┘
                                         │ assigns tasks
        ┌────────────────┬───────────────┼───────────────┬─────────────────┐
        ▼                ▼               ▼               ▼                 ▼
 ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ ┌─────────────┐  ┌──────────────┐
 │  KEYWORD    │  │    GBP      │  │   TIKTOK    │ │  SERP/WEB   │  │  (collectors)│
 │   AGENT     │  │   AGENT     │  │   AGENT     │ │   /FORUM    │  │  Trends, YT  │
 │ Google Ads  │  │ Perf. API   │  │ Creative    │ │   AGENT     │  │              │
 │ API         │  │ (consented) │  │ Center +    │ │ SERP API +  │  │              │
 │             │  │             │  │ manual org. │ │ manual      │  │              │
 └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ └──────┬──────┘  └──────┬───────┘
        │ raw CSV/JSON   │ raw JSON       │ raw notes      │ snippets+URLs  │
        └────────────────┴───────────────┴────────────────┴────────────────┘
                                         ▼
                         ┌───────────────────────────────────────┐
                         │          DATA ENGINEERING AGENT         │
                         │  RAW (Parquet, immutable, dated)        │
                         │   → normalize (accents/casing/variants) │
                         │   → dedup → confidence score            │
                         │   → DuckDB analytical tables            │
                         │   → push CURATED records to Convex      │
                         └───────────────┬───────────────────────┘
                                         ▼
                ┌────────────────────────┴────────────────────────┐
                ▼                                                  ▼
   ┌───────────────────────────┐                    ┌───────────────────────────┐
   │  MARKET STRATEGY ANALYST   │  ◄── challenged ──► │   COMPLIANCE / SKEPTIC     │
   │  clusters · pains · offers │                    │   counter-evidence · ToS   │
   │  product/content/SEO angles│                    │   weak-data flags · veto   │
   └─────────────┬──────────────┘                    └─────────────┬─────────────┘
                 └──────────────────────┬──────────────────────────┘
                                        ▼
                         ┌───────────────────────────────┐
                         │   OUTPUTS (docs/07)            │
                         │   report · CSVs · maps ·       │
                         │   Convex dashboard · risk memo │
                         └───────────────────────────────┘
```

## Agents and responsibilities

In Claude Code these map to **subagents** (spawned per task) plus **per-phase prompt templates** stored in `agents/`. They are not always-on services; the Orchestrator role is effectively *you + me* driving the phase plan and the research log.

| Agent | Core responsibility | Inputs | Outputs | Tools it uses |
|---|---|---|---|---|
| **Orchestrator** | Owns the plan, routes tasks, prevents duplicate work, keeps the research log + assumptions register | research questions | task assignments, `research_log` entries | filesystem, git |
| **Keyword** | Seed → expand via Google Ads API → volume/competition/bids/trend → cluster by intent → flag risky intent | seed phrases (ES+EN) | `keywords`, `keyword_metrics` CSV/JSON | Google Ads API (Python) |
| **GBP** | OAuth flow design, pull Performance API metrics + per-business search keywords, anonymize, benchmark | consented business OAuth | `gbp_locations`, `gbp_search_keywords` | Business Profile Performance API |
| **TikTok Intelligence** | Creative Center keyword insights + Top Ads; semi-manual organic mining; extract hooks/pains/objections; label confidence; keep ads ≠ organic | seed phrases, hashtags | `tiktok_videos`, `tiktok_themes` | Browser automation (assisted), manual |
| **SERP/Web/Forum** | Find discussions, guides, complaints, competitors, agency pages; extract recurring language + evidence; multi-source | seed phrases, questions | `source_documents`, snippets | SERP API, Reddit API, YouTube API, fetch |
| **Data Engineering** | Data model, ingest scripts, normalize ES/EN/accents/typos, dedup, source metadata, confidence scoring | all raw outputs | DuckDB tables, Convex curated records | Python (pandas/duckdb), Convex client |
| **Market Strategy Analyst** | Turn data into segments, pain clusters, offer angles, product/content/SEO/landing recommendations | curated data | `content_ideas`, `research_findings` | analysis (read-only over DuckDB/Convex) |
| **Compliance/Skeptic** | Challenge every conclusion, find counter-evidence, flag fake-review/gating/ToS/weak-data, require citations, "what would change our mind" | draft findings | `risks`, contradiction notes, veto flags | read-only + web search |

## Data flow (one sentence per hop)

1. Collectors write **immutable, dated raw files** (`data/raw/<source>/<date>/...`) — never edited after write.
2. Data Engineering reads raw → **normalizes & dedups** into DuckDB (`data/analytics/research.duckdb`).
3. Analyst queries DuckDB to produce **draft findings** with confidence scores.
4. Skeptic reviews drafts, attaches counter-evidence and risk flags; unresolved → finding downgraded or killed.
5. Survivors are written as **curated records to Convex** (`research_findings`, `content_ideas`, `risks`, `citations`).
6. Convex powers the **dashboard**; Python emits the **CSV/report deliverables** into `outputs/`.

## Setup order (dependency-correct)

1. **Repo + secrets hygiene** — `.gitignore`, `.env.example`, pre-commit secret scan. (Phase 0)
2. **Filesystem + git/GitHub MCP** — lowest risk, enables everything else.
3. **Python env + DuckDB** — analytics layer; works with zero external creds.
4. **Convex project** — schema deploy; dashboard backend.
5. **Google Ads API connector** — longest lead time (developer-token approval can take days) → start the application early.
6. **SERP API + Reddit + YouTube connectors** — cheap, fast to wire.
7. **Google Trends collector** — unofficial; isolate so breakage doesn't block the pipeline.
8. **Browser automation MCP (Playwright)** — for Creative Center; sandbox, no personal accounts.
9. **GBP Performance API connector** — needs consenting businesses + quota approval; runs as a parallel track, never a blocker.

> **Critical-path warning:** Google Ads developer-token approval and GBP quota/access approval are both *human-gated and slow*. Submit both applications on Day 1 of Phase 0 even though you won't use them until Phases 2–3.

## What's automated vs. manual

| Fully automated (safe) | Semi-automated (assisted) | Manual (required) |
|---|---|---|
| Google Ads keyword metrics pull | Creative Center / Top Ads collection via Playwright with human in the loop | TikTok organic theme reading & judgement |
| SERP API queries, YouTube Data API, Reddit API | Trends export (unofficial lib, watch for breakage) | Reading Facebook groups (no compliant API) |
| Normalization, dedup, DuckDB rollups | GBP OAuth consent capture | Business owner outreach & consent |
| CSV/report generation, Convex writes | | Final judgement on ambiguous intent / compliance |
