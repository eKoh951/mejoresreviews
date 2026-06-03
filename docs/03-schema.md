# 03 — Database Schema

## Two-layer design (deliberate)

- **Analytics layer — DuckDB** (`data/analytics/research.duckdb`): where normalization, dedup, fuzzy-matching, and heavy aggregation happen in Python. Free, local, SQL, fast over Parquet. This is where the *work* is done.
- **Curation/dashboard layer — Convex**: only **curated, human-meaningful records** land here (keywords + final metrics, findings, clusters, content ideas, risks, citations). This is what the dashboard reads.

Raw collected files live in `data/raw/<source>/<YYYY-MM-DD>/` as **immutable Parquet/JSON**, referenced by `source_documents`. Raw is never edited — re-collection writes a new dated folder.

> Rationale: Convex is document/reactive and TS-first; ad-hoc analytical SQL (e.g. "cluster 4,000 keywords by normalized stem and sum bucketed volume") is painful there and trivial in DuckDB. Don't fight the tool — let each layer do what it's good at.

---

## Entity overview

```
regions ──┐
platforms ┤
          ├──< keyword_metrics >── keywords ──< keyword_cluster_map >── clusters
          │                                                              │
source_documents ──< citations >── research_findings >── assumptions     │
          │                              │                               │
          ├──< tiktok_videos >── tiktok_themes                           │
          ├──< gbp_locations >── gbp_search_keywords                     │
          ├──< competitors                                               │
          └──< content_ideas >─────────────────────────────────────────┘
                         risks ──(link to findings/clusters)
```

---

## Convex schema (`convex/schema.ts`)

Convex uses document tables with typed validators and indexes. Foreign keys are `v.id("table")`. Sketch:

```ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  regions: defineTable({
    name: v.string(),                 // "Ciudad Juárez"
    level: v.string(),                // city | state | country
    parentRegionId: v.optional(v.id("regions")),
    googleGeoTargetId: v.optional(v.string()), // Google Ads geo constant
  }).index("by_name", ["name"]),

  platforms: defineTable({
    name: v.string(),                 // google_ads | gbp | trends | tiktok_cc | reddit | youtube | serp | forum
    dataType: v.string(),             // official | inferred | scraped | anecdotal
  }).index("by_name", ["name"]),

  keywords: defineTable({
    raw: v.string(),                  // as collected
    normalized: v.string(),           // lowercased, accent-folded, trimmed
    language: v.string(),             // es | en | mixed
    variantGroupId: v.optional(v.string()), // groups reseñas/reviews/opiniones equivalents
    intent: v.string(),               // informational | commercial | transactional | navigational | risky
    isRiskyIntent: v.boolean(),       // fake/bought/gating → true (studied, never recommended)
    seed: v.boolean(),                // was this an original seed?
  }).index("by_normalized", ["normalized"])
    .index("by_intent", ["intent"]),

  keyword_metrics: defineTable({
    keywordId: v.id("keywords"),
    platformId: v.id("platforms"),
    regionId: v.optional(v.id("regions")),
    avgMonthlySearches: v.optional(v.number()),
    competition: v.optional(v.string()),       // LOW | MEDIUM | HIGH
    competitionIndex: v.optional(v.number()),  // 0–100
    bidLow: v.optional(v.number()),            // currency units
    bidHigh: v.optional(v.number()),
    trend12mo: v.optional(v.array(v.number())),// monthly volumes
    isBucketed: v.boolean(),                   // Google Ads rounding flag
    collectedAt: v.string(),                   // ISO date
    sourceDocumentId: v.optional(v.id("source_documents")),
    confidence: v.number(),                    // 1–3
  }).index("by_keyword", ["keywordId"])
    .index("by_platform_region", ["platformId", "regionId"]),

  clusters: defineTable({
    key: v.string(),                  // get_more_reviews | remove_bad_reviews | ...
    label: v.string(),
    description: v.string(),
    complianceRisk: v.string(),       // none | low | medium | high
  }).index("by_key", ["key"]),

  keyword_cluster_map: defineTable({
    keywordId: v.id("keywords"),
    clusterId: v.id("clusters"),
    weight: v.number(),               // soft membership 0–1
  }).index("by_cluster", ["clusterId"]).index("by_keyword", ["keywordId"]),

  source_documents: defineTable({
    platformId: v.id("platforms"),
    url: v.optional(v.string()),
    title: v.optional(v.string()),
    rawPath: v.optional(v.string()),  // data/raw/... pointer
    collectedAt: v.string(),
    dataType: v.string(),             // official | inferred | scraped | anecdotal
    snippet: v.optional(v.string()),
    lang: v.optional(v.string()),
  }).index("by_platform", ["platformId"]),

  tiktok_videos: defineTable({
    url: v.string(),
    description: v.optional(v.string()),
    hashtags: v.array(v.string()),
    views: v.optional(v.number()),
    likes: v.optional(v.number()),
    comments: v.optional(v.number()),
    creatorNiche: v.optional(v.string()),
    isAd: v.boolean(),                // ads (Creative Center/Top Ads) vs organic
    collectedAt: v.string(),
    sourceDocumentId: v.optional(v.id("source_documents")),
    confidence: v.number(),
  }).index("by_isAd", ["isAd"]),

  // AGGREGATE themes only — never store individual commenter identities/PII
  tiktok_themes: defineTable({
    theme: v.string(),                // "miedo a reseñas falsas", "no sé cómo pedir reseñas"
    type: v.string(),                 // pain | objection | question | desire | misinformation
    examplePhrases: v.array(v.string()), // anonymized representative phrasings
    occurrenceCount: v.number(),
    clusterId: v.optional(v.id("clusters")),
    confidence: v.number(),
  }).index("by_type", ["type"]),

  gbp_locations: defineTable({
    anonId: v.string(),               // "biz_01" — never the real name in shared data
    category: v.string(),             // restaurant | cafe | local_service | ...
    regionId: v.optional(v.id("regions")),
    reviewCount: v.optional(v.number()),
    avgRating: v.optional(v.number()),
    consentRef: v.string(),           // pointer to signed consent record (not the PII itself)
    collectedAt: v.string(),
  }).index("by_category", ["category"]),

  gbp_search_keywords: defineTable({
    locationId: v.id("gbp_locations"),
    keyword: v.string(),
    monthImpressions: v.number(),
    isThresholded: v.boolean(),       // value is the min threshold, not exact
    month: v.string(),                // YYYY-MM
    confidence: v.number(),
  }).index("by_location", ["locationId"]),

  competitors: defineTable({
    name: v.string(),
    url: v.optional(v.string()),
    type: v.string(),                 // saas | agency | freelancer | marketplace
    offer: v.optional(v.string()),
    pricingBand: v.optional(v.string()),
    positioning: v.optional(v.string()),
    market: v.optional(v.string()),   // mx | latam | global
    collectedAt: v.string(),
  }),

  content_ideas: defineTable({
    clusterId: v.id("clusters"),
    channel: v.string(),              // tiktok | seo | landing
    angle: v.string(),
    hook: v.optional(v.string()),
    copy: v.optional(v.string()),
    complianceChecked: v.boolean(),
    confidence: v.number(),
  }).index("by_cluster", ["clusterId"]),

  research_findings: defineTable({
    title: v.string(),
    statement: v.string(),
    clusterId: v.optional(v.id("clusters")),
    dataType: v.string(),             // official | ads | organic | anecdotal
    confidence: v.number(),           // 1–3
    sourceCount: v.number(),          // # independent sources
    status: v.string(),               // draft | challenged | accepted | rejected
    whatWouldChangeOurMind: v.string(),
    createdAt: v.string(),
  }).index("by_status", ["status"]).index("by_cluster", ["clusterId"]),

  citations: defineTable({
    findingId: v.id("research_findings"),
    sourceDocumentId: v.id("source_documents"),
    note: v.optional(v.string()),
  }).index("by_finding", ["findingId"]),

  assumptions: defineTable({
    statement: v.string(),
    basis: v.string(),                // why we assume it
    validated: v.boolean(),
    invalidatedBy: v.optional(v.id("research_findings")),
    createdAt: v.string(),
  }).index("by_validated", ["validated"]),

  risks: defineTable({
    category: v.string(),             // compliance | tos | legal | data_quality | strategic
    description: v.string(),
    severity: v.string(),             // low | medium | high
    relatedFindingId: v.optional(v.id("research_findings")),
    relatedClusterId: v.optional(v.id("clusters")),
    mitigation: v.optional(v.string()),
  }).index("by_category", ["category"]),

  research_log: defineTable({
    phase: v.string(),
    action: v.string(),
    agent: v.string(),
    result: v.optional(v.string()),
    at: v.string(),
  }).index("by_phase", ["phase"]),
});
```

## DuckDB analytics tables (mirror + work tables)

In DuckDB you keep the same logical entities **plus** scratch/work tables that never go to Convex:

- `raw_keyword_ideas` — every row from Google Ads, pre-dedup.
- `kw_norm` — normalized keys (`unidecode` accent-fold + lowercase + whitespace), with `rapidfuzz` near-duplicate clusters.
- `variant_map` — links `reseñas`↔`reviews`↔`opiniones`↔`calificaciones` and common typos.
- `cluster_scores` — the per-cluster aggregation feeding [`05-analysis-framework.md`](05-analysis-framework.md).

Only the **curated** results (deduped keywords, final metrics, cluster scores, findings) are pushed to Convex via the Python `convex` client.

## Normalization rules (Spanish-first)

1. Accent-fold for the **matching key** (`reseña`→`resena`) but **preserve the original** in `keywords.raw` for display.
2. Treat `reseñas / opiniones / calificaciones / valoraciones / reviews` as a **variant group**, not as the same keyword — measure which dominates.
3. Keep common misspellings (`reseñas` vs `resenas` vs `reseñas google`) mapped to the canonical via fuzzy match ≥ threshold, logged for audit.
4. Tag language per keyword (`es`/`en`/`mixed`); MX market is ES-dominant but EN terms appear in agency/SaaS contexts.
