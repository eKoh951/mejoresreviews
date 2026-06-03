# 04 — Research Workflow (Phases 0–8)

Each phase has: **goal · who · steps · output · gate (what must be true to advance).** Two slow approvals (Google Ads dev token, GBP quota/access) are submitted in Phase 0 and run as background tracks.

---

## Phase 0 — Setup
- **Goal:** repo, secrets hygiene, environments, and *both slow approvals submitted*.
- **Who:** Orchestrator + Data Engineering.
- **Steps:**
  1. `.gitignore` (data/raw large files, `.env`, `.venv`), `.env.example`, `gitleaks` pre-commit.
  2. Python venv + `duckdb pandas pyarrow python-dotenv unidecode rapidfuzz`.
  3. `npm create convex@latest`; deploy `convex/schema.ts` from [`03-schema.md`](03-schema.md).
  4. **Submit Google Ads developer-token application.** ⏳
  5. **Submit GBP API access/quota request** and draft the business-owner consent form. ⏳
  6. Seed the `regions` table (Mexico, Chihuahua, Ciudad Juárez with Google geo IDs) and `platforms`/`clusters` tables.
- **Output:** working repo, deployed empty schema, two pending approvals, research log started.
- **Gate:** schema deploys; secrets scan passes; approvals submitted (not yet granted).

## Phase 1 — Seed keyword discovery
- **Goal:** a clean bilingual seed list with intent + risk labels.
- **Who:** Keyword Agent.
- **Steps:** load the EN + ES seeds from the brief; expand obvious morphology; tag each seed `intent` and `isRiskyIntent`; record variant groups (reseñas/reviews/opiniones/calificaciones).
- **Output:** `keywords` (seeds) in DuckDB + Convex.
- **Gate:** ≥ ~40 seeds across all clusters, every seed labeled.

## Phase 2 — Google search demand
- **Goal:** volume / competition / bids / trend for the universe, MX + Chihuahua + Cd. Juárez, ES.
- **Who:** Keyword Agent + Data Engineering.
- **Steps:** `generateKeywordIdeas` + `generateKeywordHistoricalMetrics` per seed with geo + language targeting; write raw Parquet (dated); normalize + dedup; set `isBucketed`; push curated `keyword_metrics`.
- **Output:** keyword universe with metrics; first cut of `cluster_scores`.
- **Gate:** dev token granted; ≥ N keywords with metrics; bucketing flagged. *If token delayed:* fall back to SERP-API/DataForSEO estimates labeled ⭐⭐ inferred.

## Phase 3 — GBP real search data *(parallel track, never a blocker)*
- **Goal:** ground-truth of what real searches trigger 1–5 consenting local profiles.
- **Who:** GBP Agent.
- **Steps:** OAuth consent capture (store consent ref, **not** PII); pull `searchkeywords` + impressions/calls/clicks/directions/messages/bookings; anonymize to `biz_01…`; load `gbp_locations` + `gbp_search_keywords`; flag `isThresholded`.
- **Output:** anonymized per-business benchmark.
- **Gate:** signed consent on file per business; quota granted.
- **⚠ Honesty gate:** N=1–5 is a **worked example, not a market**. Every generalization from it is auto-labeled ⭐ and routed to the Skeptic.

## Phase 4 — TikTok demand mining
- **Goal:** ad-market signal + informal organic language, kept strictly separate.
- **Who:** TikTok Intelligence Agent.
- **Steps:**
  1. *Ads:* Creative Center Keyword Insights + Top Ads (supervised/manual) → `tiktok_videos (isAd=true)`, hooks/CTAs/offers.
  2. *Organic:* manual, public-only collection → `tiktok_videos (isAd=false)` + aggregated `tiktok_themes`. **No commenter PII.**
- **Output:** ad-pattern set + organic theme set, each confidence-labeled.
- **Gate:** ads vs organic never merged; Research-API assumption explicitly marked "unavailable".

## Phase 5 — Web / forum / social mining
- **Goal:** recurring pains, objections, scams, misinformation, pricing expectations, competitors.
- **Who:** SERP/Web/Forum Agent.
- **Steps:** SERP API for SERP + PAA + competitor URLs; Reddit (`praw`) + YouTube API for ES discussions; manual reads of GBP/local-SEO forums + MX entrepreneur/restaurant communities (public only). Capture URL + date + snippet into `source_documents`; aggregate themes; build `competitors`.
- **Output:** evidence corpus, competitor matrix seed, pain/objection theme set.
- **Gate:** no single-source claims promoted; every snippet has URL + date.

## Phase 6 — Clustering & insight generation
- **Goal:** turn the corpus into the 12 intent clusters with scores.
- **Who:** Data Engineering + Market Strategy Analyst.
- **Steps:** map keywords/themes to clusters (`keyword_cluster_map`, soft weights); compute per-cluster volume/trend/pain/intent/risk (see [`05`](05-analysis-framework.md)); draft `research_findings` with `whatWouldChangeOurMind`.
- **Output:** scored clusters + draft findings (status `draft`).
- **Gate:** every finding has ≥1 citation and a confidence score before it leaves draft.

## Phase 7 — Validation & contradiction search
- **Goal:** actively try to break each finding.
- **Who:** Compliance/Skeptic Agent.
- **Steps:** for each finding seek ≥2 independent sources; run the contradiction checklist ([`06`](06-validation-protocol.md)); flag fake-review/gating/ToS risks into `risks`; downgrade or `reject` unsupported findings.
- **Output:** findings promoted to `accepted` or `rejected`; populated `risks`.
- **Gate:** no `accepted` finding rests on a single anecdotal source; compliance memo has no open high-severity items.

## Phase 8 — Final strategy report
- **Goal:** ship the deliverables in [`07-outputs.md`](07-outputs.md).
- **Who:** Market Strategy Analyst + Orchestrator.
- **Steps:** generate report + CSVs + maps from Convex/DuckDB; build dashboard views; attach compliance risk memo + next-experiment plan.
- **Output:** everything in `outputs/`.
- **Gate:** every headline claim traces to a finding → citation → source with a date and confidence.

---

## Phase dependency & parallelism

```
P0 ──> P1 ──> P2 ─┐
   │              ├──> P6 ──> P7 ──> P8
   ├─> P3 ────────┤   (clustering)  (validate) (report)
   ├─> P4 ────────┤
   └─> P5 ────────┘
P3 (GBP) and P4 (TikTok manual) run in parallel and feed P6 when ready; they never block P2's keyword backbone.
```
