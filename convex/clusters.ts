import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const getByKey = query({
  args: { key: v.string() },
  handler: async (ctx, { key }) => {
    return ctx.db.query("clusters").withIndex("by_key", q => q.eq("key", key)).first();
  },
});

export const insert = mutation({
  args: {
    key: v.string(),
    label: v.string(),
    description: v.string(),
    complianceRisk: v.string(),
  },
  handler: async (ctx, args) => {
    return ctx.db.insert("clusters", args);
  },
});
