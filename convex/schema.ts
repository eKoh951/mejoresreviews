import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  regions: defineTable({
    name: v.string(),
    level: v.string(),
    parentRegionId: v.optional(v.id("regions")),
    googleGeoTargetId: v.optional(v.string()),
  }).index("by_name", ["name"]),

  platforms: defineTable({
    name: v.string(),
    dataType: v.string(),
  }).index("by_name", ["name"]),

  keywords: defineTable({
    raw: v.string(),
    normalized: v.string(),
    language: v.string(),
    variantGroupId: v.optional(v.string()),
    intent: v.string(),
    isRiskyIntent: v.boolean(),
    isSeed: v.boolean(),
  }).index("by_normalized", ["normalized"])
    .index("by_intent", ["intent"]),

  keyword_metrics: defineTable({
    keywordId: v.id("keywords"),
    platformId: v.id("platforms"),
    regionId: v.optional(v.id("regions")),
    avgMonthlySearches: v.optional(v.number()),
    competition: v.optional(v.string()),
    competitionIndex: v.optional(v.number()),
    bidLow: v.optional(v.number()),
    bidHigh: v.optional(v.number()),
    trend12mo: v.optional(v.array(v.number())),
    isBucketed: v.boolean(),
    collectedAt: v.string(),
    confidence: v.number(),
  }).index("by_keyword", ["keywordId"])
    .index("by_platform_region", ["platformId"]),

  clusters: defineTable({
    key: v.string(),
    label: v.string(),
    description: v.string(),
    complianceRisk: v.string(),
  }).index("by_key", ["key"]),

  keyword_cluster_map: defineTable({
    keywordId: v.id("keywords"),
    clusterKey: v.string(),
    weight: v.number(),
  }).index("by_cluster", ["clusterKey"])
    .index("by_keyword", ["keywordId"]),

  source_documents: defineTable({
    platformId: v.id("platforms"),
    url: v.optional(v.string()),
    title: v.optional(v.string()),
    rawPath: v.optional(v.string()),
    collectedAt: v.string(),
    dataType: v.string(),
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
    isAd: v.boolean(),
    collectedAt: v.string(),
    confidence: v.number(),
  }).index("by_isAd", ["isAd"]),

  tiktok_themes: defineTable({
    theme: v.string(),
    type: v.string(),
    examplePhrases: v.array(v.string()),
    occurrenceCount: v.number(),
    clusterKey: v.optional(v.string()),
    confidence: v.number(),
  }).index("by_type", ["type"]),

  gbp_locations: defineTable({
    anonId: v.string(),
    category: v.string(),
    regionId: v.optional(v.id("regions")),
    reviewCount: v.optional(v.number()),
    avgRating: v.optional(v.number()),
    consentRef: v.string(),
    collectedAt: v.string(),
  }).index("by_category", ["category"]),

  gbp_search_keywords: defineTable({
    locationId: v.id("gbp_locations"),
    keyword: v.string(),
    monthImpressions: v.number(),
    isThresholded: v.boolean(),
    month: v.string(),
    confidence: v.number(),
  }).index("by_location", ["locationId"]),

  competitors: defineTable({
    name: v.string(),
    url: v.optional(v.string()),
    type: v.string(),
    offer: v.optional(v.string()),
    pricingBand: v.optional(v.string()),
    positioning: v.optional(v.string()),
    market: v.optional(v.string()),
    collectedAt: v.string(),
  }),

  content_ideas: defineTable({
    clusterKey: v.string(),
    channel: v.string(),
    angle: v.string(),
    hook: v.optional(v.string()),
    copy: v.optional(v.string()),
    complianceChecked: v.boolean(),
    confidence: v.number(),
  }).index("by_cluster", ["clusterKey"]),

  research_findings: defineTable({
    title: v.string(),
    statement: v.string(),
    clusterKey: v.optional(v.string()),
    dataType: v.string(),
    confidence: v.number(),
    sourceCount: v.number(),
    status: v.string(),
    whatWouldChangeOurMind: v.string(),
    createdAt: v.string(),
  }).index("by_status", ["status"])
    .index("by_cluster", ["clusterKey"]),

  citations: defineTable({
    findingId: v.id("research_findings"),
    sourceDocumentId: v.id("source_documents"),
    note: v.optional(v.string()),
  }).index("by_finding", ["findingId"]),

  assumptions: defineTable({
    statement: v.string(),
    basis: v.string(),
    validated: v.boolean(),
    createdAt: v.string(),
  }).index("by_validated", ["validated"]),

  risks: defineTable({
    category: v.string(),
    description: v.string(),
    severity: v.string(),
    relatedClusterKey: v.optional(v.string()),
    mitigation: v.optional(v.string()),
  }).index("by_category", ["category"])
    .index("by_severity", ["severity"]),

  research_log: defineTable({
    phase: v.string(),
    action: v.string(),
    agent: v.string(),
    result: v.optional(v.string()),
    loggedAt: v.string(),
  }).index("by_phase", ["phase"]),
});
