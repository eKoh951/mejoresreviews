import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const getByName = query({
  args: { name: v.string() },
  handler: async (ctx, { name }) => {
    return ctx.db.query("platforms").withIndex("by_name", q => q.eq("name", name)).first();
  },
});

export const insert = mutation({
  args: {
    name: v.string(),
    dataType: v.string(),
  },
  handler: async (ctx, args) => {
    return ctx.db.insert("platforms", args);
  },
});
