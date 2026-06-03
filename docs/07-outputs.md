# 07 — Final Outputs

All outputs land in `outputs/` and are **regenerable** from Convex + DuckDB (no hand-edited numbers). Every output carries a generation date and a data-vintage note.

| # | Output | Format | Generated from | Key columns / sections |
|---|---|---|---|---|
| 1 | **Market research report** | Markdown + PDF | findings + clusters | exec summary · per-cluster scorecards · segment cuts · risks · open questions · "what would change our mind" |
| 2 | **Keyword universe** | CSV | `keywords` + `keyword_metrics` | raw, normalized, lang, variant_group, intent, is_risky, avg_searches, competition, comp_index, bid_low, bid_high, is_bucketed, region, confidence, source |
| 3 | **Keyword clusters** | CSV | `clusters` + `keyword_cluster_map` + scores | cluster, total_volume, trend, pain, intent, compliance_risk, keyword_count, confidence |
| 4 | **TikTok content insights** | CSV | `tiktok_videos` + `tiktok_themes` | is_ad, hook, cta, offer, format, theme, type, example_phrases, occurrence, confidence |
| 5 | **Competitor matrix** | CSV + MD | `competitors` | name, type (saas/agency/freelancer), offer, pricing_band, positioning, market, gaps |
| 6 | **User pain map** | MD + diagram | `tiktok_themes` + forum/reddit themes | pain → frequency → intensity → cluster → compliant response |
| 7 | **Product opportunity map** | MD + table | analyst over clusters | opportunity, demand, intent, compliance gate, effort, confidence, recommendation |
| 8 | **Landing page messaging recs** | MD | findings | per-segment headline, subhead, value props, objections-handled, proof needed — **compliant framing only** |
| 9 | **TikTok content calendar ideas** | CSV | `content_ideas (channel=tiktok)` | week, cluster, hook, angle, format, CTA, compliance_checked |
| 10 | **Local SEO content cluster map** | MD + diagram | `content_ideas (channel=seo)` | pillar → cluster → supporting topics → target keywords → intent |
| 11 | **Compliance risk memo** | MD | `risks` | see [`08-compliance-risk-memo.md`](08-compliance-risk-memo.md) |
| 12 | **Next experiment plan** | MD | gaps + assumptions | hypothesis, test, metric, cost, decision rule |

## Dashboard (Convex-backed)

A lightweight web dashboard reading Convex queries, with these views:

- **Cluster overview** — the 12 clusters with volume/trend/pain/intent/compliance, filterable by region & business type.
- **Keyword explorer** — search/filter the universe; variant-group toggle (reseñas vs reviews vs opiniones vs calificaciones).
- **Evidence panel** — for any finding, show its citations (URL + date + snippet + data type + confidence).
- **Risk board** — open risks by severity; high-severity items gate the report.
- **Assumptions register** — validated vs open, with what would close each.

## Presentation rules (carried into every output)

1. Show **component metrics**, never a lone composite score.
2. Label **data type** (official / ads / organic / anecdotal) and **confidence** on every claim.
3. Flag **bucketed** Google Ads volumes and **thresholded** GBP keywords visibly.
4. Mark the **N=1–5 GBP pilot** as a worked example wherever it appears.
5. Include a **"What would change our mind"** box in the report and product map.
6. Keep a **data-vintage** line: which sources, collected when.
