# 08 — Compliance, ToS, Legal & Ethical Risk Memo

This memo separates **legal/ToS risk to the research process** from **compliance risk in the recommendations the project might ship**. It is informational risk disclosure, not legal advice — confirm specifics with counsel for the Mexican market and any other markets you operate in.

## A. Risks in the research process itself

| Risk | Where | Severity | Mitigation |
|---|---|---|---|
| **Scraping against platform ToS** | TikTok, Google Maps, Facebook | 🔴 high | Prefer first-party APIs; for TikTok use manual/supervised public-only collection; never automate logged-in sessions; respect robots.txt/ToS. |
| **Collecting personal data (PII)** of commenters/reviewers | TikTok, Reddit, forums, FB groups | 🔴 high | Store **aggregate themes only**; no usernames, no profile data; this also aligns with data-protection norms (incl. Mexico's LFPDPPP). |
| **Private/closed-group data** | Facebook groups | 🔴 high | Manual reading only where you're a legitimate member; never scrape private groups; do not store member identities. |
| **Google Ads API misuse / over-quota** | Keyword Agent | 🟡 medium | Read-only KeywordPlan services; stay within basic-access limits; no campaign mutations. |
| **GBP data handling without proper consent** | GBP Agent | 🔴 high | Written consent per business before OAuth; store a consent reference, not the PII; anonymize to `biz_NN`; let owners revoke. |
| **Unofficial scraper (`pytrends`) breakage / blocking** | Trends | 🟡 medium (reliability) | Isolate; prefer manual export; treat failures as non-blocking. |
| **Secret leakage** | all connectors | 🔴 high | `.env` only, git-ignored; `gitleaks` pre-commit; minimal scopes; never paste keys into prompts. |
| **Untrusted third-party MCP** | tooling | 🔴 high | Vet repo/commits/issues; pin versions; sandbox; prefer first-party SDK + script over convenience MCPs. |

## B. Compliance risk in the *recommendations*

The product angle on record is compliant: **earn more legitimate reviews, respond better, improve service, recover dissatisfied customers, improve local visibility.** The following tactics carry policy/legal risk and must be flagged by the Skeptic agent if any recommendation drifts toward them:

| Tactic | Risk | Why |
|---|---|---|
| **Fake / bought reviews** | 🔴 severe | Violates Google policy; in many markets (incl. US FTC rules) generating or buying fake reviews is unlawful; reputational and account-termination risk. The system studies this demand only to design compliant counter-offers — never to recommend it. |
| **Review gating** (soliciting only happy customers, or intercepting dissatisfied customers before they post a public review) | 🟡–🔴 medium-high | Against Google's review policies and, in some jurisdictions (e.g. US FTC), treated as a deceptive practice. Even where enforcement is uncertain in Mexico, it carries platform and reputational risk. **Document it as a risk; if the project chooses to study or use solicitation flows, route every such flow through this memo and verify against current Google policy + local law before shipping.** |
| **"Remove any negative review"** | 🟡 medium | Only reviews that violate Google's content policies can legitimately be flagged for removal. Promising removal of *honest* negative reviews is misleading and usually impossible. |
| **Incentivizing reviews** (discounts for reviews) | 🟡 medium | Google prohibits review incentives; FTC requires clear disclosure of material connections. Recommend non-incentivized solicitation. |
| **Misrepresenting ranking guarantees** | 🟡 medium | "Guaranteed #1 on Maps" is not deliverable and risks deceptive-advertising exposure. |

## C. Compliant alternatives the system *should* recommend

- Ask **all** customers for honest feedback (not just happy ones), via QR/link at the natural moment.
- Make reviewing frictionless (direct GBP review link, short instructions).
- Respond to **every** review, positive and negative, professionally.
- Use negative feedback as a **service-recovery** loop (contact the customer, fix the issue).
- Improve GBP completeness, categories, photos, hours, posts.
- Build genuinely useful local content (local SEO) targeting real questions found in research.

## D. Data provenance discipline (anti-overclaim)

- Always label **official vs inferred vs scraped vs anecdotal** on stored data and in outputs.
- Trends and TikTok numbers are **never** presented as search volume.
- Google Ads volumes are **bucketed**; GBP keywords are **thresholded** — both flagged in outputs.
- The **N=1–5 GBP pilot is a worked example, not a market**; no statistical generalization.

## E. "What could change our mind" (project-level)

- If Google Ads volume for the core Spanish terms in Cd. Juárez / Chihuahua is negligible, the *local-only* thesis weakens (consider broader MX/LatAm).
- If real GBP search keywords from consenting businesses don't match the keyword-tool universe, trust GBP and revise the universe.
- If TikTok demand is purely advertiser-driven with no organic pull, the content-led acquisition thesis weakens.
- If competitor/agency saturation is high with low pricing, the market may be commoditized — revisit the product angle.

## F. Open compliance questions to resolve before shipping any go-to-market

1. Current Google review-solicitation policy language (re-verify at ship time — policies change).
2. Mexican consumer-protection (PROFECO) and data-protection (LFPDPPP) implications of review-solicitation and customer-data handling.
3. Any market-specific rules if expanding beyond Mexico (e.g. US FTC rules on reviews/endorsements).
4. TikTok commercial-use terms for any data retained from Creative Center / organic collection.
