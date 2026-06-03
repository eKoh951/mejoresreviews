# 06 — Validation Protocol (anti-hallucination)

The system's bias is **toward disconfirmation**. A finding must survive an attempt to break it.

## Required fields on every `research_findings` record

| Field | Rule |
|---|---|
| `statement` | One falsifiable claim. No vague "people want more reviews." |
| `dataType` | official / ads / organic / anecdotal — explicit. |
| `sourceCount` | # of **independent** sources (different platform OR different author). |
| `confidence` | 1–3, derived from the rule below — not vibes. |
| `whatWouldChangeOurMind` | Concrete observation that would falsify it. Empty = finding rejected. |
| ≥1 `citations` | Each links a `source_documents` row with URL + collection date. |

## Confidence derivation (mechanical)

| Confidence | Requires |
|---|---|
| ⭐⭐⭐ | First-party/official data (Google Ads, GBP) **and** ≥2 independent corroborations, **and** no unresolved contradiction. |
| ⭐⭐ | Third-party modeled (SERP/Trends/TikTok ads) **or** official-but-single-source, with ≥1 corroboration. |
| ⭐ | Single source, or anecdotal/organic only, or N=1–5 GBP generalization. **Cannot** back a primary product recommendation. |

A finding's confidence = **min** of (best data type available, source-count tier). One strong source does not beat the 2-source rule for anything that drives a decision.

## The 2-source rule

- Any finding that **drives a recommendation** needs **≥2 independent sources** wherever possible.
- "Independent" means different platform *or* different author — two Reddit comments by the same person are one source; a Reddit thread + a Google Ads volume + a TikTok theme are three.
- If only one source exists, the finding may be recorded but is capped at ⭐ and labeled **"single-source — needs corroboration."**

## Contradiction checklist (run by Skeptic on every draft)

1. **Counter-search:** actively search for the opposite claim. Log what was found.
2. **Alternative explanation:** is there a simpler reason for the signal? (e.g. high TikTok ad keyword ≠ user demand; it = advertiser demand.)
3. **Type confusion:** are we blending official volume with ads/organic/anecdotal? Separate them.
4. **Sample validity:** is this a small-N or city-level-thin sample being over-generalized? Flag low-N.
5. **Recency:** is the source stale? Record collection date; demand/seasonality shifts.
6. **Localization:** was the query actually MX/es-localized, or did US/EN results leak in?
7. **Survivorship:** TikTok "Top Ads" / viral videos = winners only; absence of failures biases conclusions.
8. **Compliance leakage:** does the recommendation drift toward gating / fake / "remove all negatives"? Hard stop.

Any unresolved item → finding cannot reach `accepted`; it is downgraded or `rejected` with a note.

## Hallucination guards specific to AI agents

- **No invented numbers.** Every metric in a report must trace to a `keyword_metrics` / `gbp_search_keywords` / source row. If an agent can't cite the row, the number is deleted.
- **No invented sources.** Citations must be real URLs that were actually fetched (logged in `source_documents`). Skeptic spot-checks that cited URLs exist and contain the claim.
- **Quote, don't paraphrase, for key claims.** Store the actual snippet that supports a finding.
- **"Don't know" is a valid output.** Gaps are recorded as `assumptions (validated=false)` or open questions, never papered over.
- **Separation enforced in storage.** Raw ≠ normalized ≠ findings (different tables/files); analysis can't silently rewrite raw data.

## Validation gates by phase

- **P2:** bucketed volumes flagged; no exact-number claims.
- **P3:** every generalization beyond the pilot auto-⭐ + Skeptic review.
- **P4:** ads vs organic never merged; Research-API marked unavailable.
- **P5:** no single-source promotion; URL+date on every snippet.
- **P7:** zero open high-severity compliance risks before P8 ships.
