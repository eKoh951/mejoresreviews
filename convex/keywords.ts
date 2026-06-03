import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const getByNormalized = query({
  args: { normalized: v.string() },
  handler: async (ctx, { normalized }) => {
    return ctx.db.query("keywords").withIndex("by_normalized", q => q.eq("normalized", normalized)).first();
  },
});

export const insert = mutation({
  args: {
    raw: v.string(),
    normalized: v.string(),
    language: v.string(),
    variantGroupId: v.optional(v.string()),
    intent: v.string(),
    isRiskyIntent: v.boolean(),
    isSeed: v.boolean(),
  },
  handler: async (ctx, args) => {
    return ctx.db.insert("keywords", args);
  },
});
