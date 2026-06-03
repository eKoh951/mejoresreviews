# Mejores Reviews — Research Operating System

A research pipeline to understand how business owners in **Mexico (Ciudad Juárez / Chihuahua first)** search for help with Google Maps reviews, Google Business Profile visibility, local SEO, online reputation, and legitimate customer-review generation.

> **Goal:** find what is *actually true and commercially useful* — not to confirm a hypothesis. Weak evidence is marked. Counter-evidence is sought on purpose.

## Hard constraints (compliance — non-negotiable)

This system **will not** design, recommend, or support:

- ❌ Fake review generation
- ❌ Buying reviews
- ❌ Scraping private/personal data

The only compliant business angle: help businesses earn **more legitimate reviews**, **respond better**, **improve service quality**, **recover dissatisfied customers**, and **improve local visibility**. See [`docs/08-compliance-risk-memo.md`](docs/08-compliance-risk-memo.md).

## Decisions on record (2026-06-02)

| Decision | Choice |
|---|---|
| Budget for paid data APIs | Low (~$50–150/mo) |
| GBP benchmark access | 1–5 consenting businesses (pilot) |
| Structured storage | Convex (curated/dashboard) + DuckDB/Parquet (analytics) |
| Implementation stack | Python (ETL/connectors) + TS (Convex schema/dashboard) |

## Document index

| # | Doc | What it is |
|---|---|---|
| 00 | [Blueprint](docs/00-blueprint.md) | Architecture, agents, data flow, setup order |
| 01 | [Installation plan](docs/01-installation-plan.md) | Each MCP/tool: why, source, install, creds, risk, alternative |
| 02 | [Data source matrix](docs/02-data-source-matrix.md) | Source × official/inferred/scraped × cost × confidence |
| 03 | [Database schema](docs/03-schema.md) | Convex tables + DuckDB analytics layer |
| 04 | [Research workflow](docs/04-research-workflow.md) | Phases 0–8 |
| 05 | [Analysis framework](docs/05-analysis-framework.md) | Intent clusters + per-cluster scoring |
| 06 | [Validation protocol](docs/06-validation-protocol.md) | Anti-hallucination rules |
| 07 | [Final outputs](docs/07-outputs.md) | Reports, CSVs, maps to produce |
| 08 | [Compliance & risk memo](docs/08-compliance-risk-memo.md) | ToS / legal / ethical risks |

## Scripts

| Script | Phase | Purpose |
|---|---|---|
| `scripts/00_init_db.py` | 0/1 | Initialize DuckDB + seed regions, platforms, clusters, keywords |
| `scripts/01_convex_seed.py` | 1 | Sync seed data from DuckDB → Convex |
| `scripts/02_google_ads_keywords.py` | 2 | Pull keyword metrics via Google Ads API |
| `scripts/03_reddit_research.py` | 5 | Reddit research via PRAW (read-only) |
| `scripts/04_youtube_research.py` | 5 | YouTube Data API research |
| `scripts/05_serp_research.py` | 5 | SERP + People-Also-Ask via Serper.dev |

## Phase 0 — Getting started

```bash
# 1. Python environment
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Convex (dashboard backend)
npm install
npx convex dev                  # follow prompts; sets CONVEX_URL

# 3. Copy and fill .env
copy .env.example .env          # then add your API keys

# 4. Initialize the database
python scripts/00_init_db.py

# 5. Sync seeds to Convex (after Convex mutations are deployed)
python scripts/01_convex_seed.py
```

## Status

Scripts written. **Phase 0 execution is the next step** — see [`docs/04-research-workflow.md`](docs/04-research-workflow.md).

Google Ads developer-token application should be submitted on Day 1 (approval is slow).
