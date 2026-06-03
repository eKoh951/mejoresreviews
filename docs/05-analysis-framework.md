# 05 — Analysis Framework

## The 12 intent clusters

| key | label | compliance risk |
|---|---|---|
| `get_more_reviews` | Get more (legitimate) reviews | none |
| `remove_bad_reviews` | Remove / handle a bad review | **medium** (only legitimate flagging of ToS-violating reviews is OK; "remove any negative review" is not) |
| `respond_to_reviews` | Respond to reviews | none |
| `appear_on_maps` | Appear / rank on Google Maps | low |
| `gbp_setup` | Set up / optimize Google Business Profile | none |
| `qr_link_request` | QR / link review requests | low |
| `restaurant_marketing` | Restaurant / food-business marketing | none |
| `local_seo` | Local SEO | none |
| `reputation_management` | Reputation management | low |
| `fake_graymarket` | Fake / bought / gated reviews | **high — studied as demand, NEVER recommended as tactic** |
| `customer_service_recovery` | Service quality & dissatisfied-customer recovery | none |
| `competitor_software_agency` | Competing software / agencies | none |

> `fake_graymarket` exists so we can *measure* the dark demand and design **compliant counter-offers** (e.g. "earn more real reviews" instead of "buy reviews"). It is never an output recommendation.

## Per-cluster scorecard

For each cluster the Analyst produces:

| Field | Definition | Source of truth |
|---|---|---|
| **volume** | Summed Google Ads avg monthly searches (bucketed-flagged), MX + Chihuahua + Cd. Juárez | Google Ads (⭐⭐⭐ relative) |
| **trend** | 12-mo direction + seasonality | Google Ads trend + Trends (⭐⭐) |
| **platform evidence** | Where it shows up (Ads / GBP / TikTok ads / TikTok organic / Reddit / YouTube / SERP) | multi-source |
| **pain intensity** | 1–5 from language strength + repetition in organic/forum/comment themes | qualitative (⭐–⭐⭐) |
| **purchase intent** | informational → commercial → transactional, weighted by competition index + bids | Google Ads + SERP ads presence |
| **compliance risk** | none/low/medium/high per table above | Compliance agent |
| **suggested product angle** | compliant product framing | Analyst (Skeptic-checked) |
| **suggested content angle** | TikTok/SEO theme | Analyst |
| **suggested landing copy angle** | headline/value-prop direction | Analyst |
| **confidence** | 1–3, = min(source quality, source count rule) | Validation protocol |

## Scoring method (transparent, not magic)

- **Demand score** = normalized volume (0–1) × trend factor. Bucketed volumes capped and flagged; never presented as precise.
- **Pain score** = (theme frequency × language intensity), computed only from aggregated organic/forum themes. Explicitly ⭐/⭐⭐ — it is qualitative.
- **Intent score** = blend of competition index + bid range + transactional keyword share. High bids = advertisers paying = commercial intent signal.
- **Opportunity = Demand × Intent × (compliant) ÷ (competition saturation)**, with **pain** as a qualitative modifier and **compliance risk** as a hard gate (high-risk clusters cannot become a primary product recommendation).

> No composite score is reported without its component parts visible. A single number is a story, not evidence.

## Segment cuts

- **By business type:** restaurants / cafés / food / local services / other small business.
- **By geography:** Cd. Juárez vs Chihuahua state vs Mexico national (watch sample thinness at city level — flag low-N).
- **By language variant:** reseñas vs reviews vs opiniones vs calificaciones share.
- **By sophistication:** "no aparezco en Google" (beginner) vs "local SEO / GBP optimization" (advanced) — different products.

## Anti-patterns the framework refuses to output

- Recommending fake/bought reviews, or "remove all negative reviews".
- Presenting Trends or TikTok numbers as search volume.
- Generalizing the N=1–5 GBP pilot to "the market".
- Any headline claim from a single anecdotal source.
