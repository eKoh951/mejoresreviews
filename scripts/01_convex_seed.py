"""Phase 1 — push seed data from DuckDB into Convex (regions, platforms, clusters, keywords).

Run AFTER 00_init_db.py and AFTER Convex is deployed (npx convex dev/deploy).

Usage:
    python scripts/01_convex_seed.py

Requires .env:
    CONVEX_URL
    CONVEX_DEPLOY_KEY   (or CONVEX_URL alone for anonymous write via HTTP)

This script is idempotent: it only inserts records that don't already exist in Convex.
"""

import os
import sys
from pathlib import Path
from datetime import date

import duckdb
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(__file__).parent.parent / "data" / "analytics" / "research.duckdb"


def get_client():
    url = os.getenv("CONVEX_URL")
    if not url:
        print("[skip] CONVEX_URL not set. Skipping Convex seed.")
        return None
    try:
        from convex import ConvexClient
        client = ConvexClient(url)
        return client
    except ImportError:
        print("[error] convex package not installed. Run: pip install convex")
        sys.exit(1)


def seed_regions(client, con):
    rows = con.execute("SELECT id, name, level, parent, geo_id FROM regions").fetchall()
    inserted = 0
    for (rid, name, level, parent, geo_id) in rows:
        try:
            existing = client.query("regions:getByName", {"name": name})
        except Exception:
            existing = None
        if existing:
            continue
        try:
            client.mutation("regions:insert", {
                "name": name,
                "level": level,
                "googleGeoTargetId": geo_id,
            })
            inserted += 1
        except Exception as e:
            print(f"  [warn] region '{name}': {e}")
    print(f"  [ok] regions: {inserted} inserted ({len(rows) - inserted} already present)")


def seed_platforms(client, con):
    rows = con.execute("SELECT id, name, data_type FROM platforms").fetchall()
    inserted = 0
    for (pid, name, data_type) in rows:
        try:
            existing = client.query("platforms:getByName", {"name": name})
        except Exception:
            existing = None
        if existing:
            continue
        try:
            client.mutation("platforms:insert", {
                "name": name,
                "dataType": data_type,
            })
            inserted += 1
        except Exception as e:
            print(f"  [warn] platform '{name}': {e}")
    print(f"  [ok] platforms: {inserted} inserted ({len(rows) - inserted} already present)")


def seed_clusters(client, con):
    rows = con.execute("SELECT key, label, description, compliance_risk FROM clusters").fetchall()
    inserted = 0
    for (key, label, description, risk) in rows:
        try:
            existing = client.query("clusters:getByKey", {"key": key})
        except Exception:
            existing = None
        if existing:
            continue
        try:
            client.mutation("clusters:insert", {
                "key": key,
                "label": label,
                "description": description,
                "complianceRisk": risk,
            })
            inserted += 1
        except Exception as e:
            print(f"  [warn] cluster '{key}': {e}")
    print(f"  [ok] clusters: {inserted} inserted ({len(rows) - inserted} already present)")


def seed_keywords(client, con):
    rows = con.execute(
        "SELECT id, raw, normalized, language, variant_group, intent, is_risky, is_seed FROM keywords"
    ).fetchall()
    inserted = 0
    for (kid, raw, normalized, lang, variant_group, intent, is_risky, is_seed) in rows:
        try:
            existing = client.query("keywords:getByNormalized", {"normalized": normalized})
        except Exception:
            existing = None
        if existing:
            continue
        doc = {
            "raw": raw,
            "normalized": normalized,
            "language": lang,
            "intent": intent,
            "isRiskyIntent": bool(is_risky),
            "isSeed": bool(is_seed),
        }
        if variant_group:
            doc["variantGroupId"] = variant_group
        try:
            client.mutation("keywords:insert", doc)
            inserted += 1
        except Exception as e:
            print(f"  [warn] keyword '{raw}': {e}")
    print(f"  [ok] keywords: {inserted} inserted ({len(rows) - inserted} already present)")


def run():
    client = get_client()
    if not client:
        return

    if not DB_PATH.exists():
        print(f"[error] DuckDB not found at {DB_PATH}. Run 00_init_db.py first.")
        sys.exit(1)

    con = duckdb.connect(str(DB_PATH))
    print("[convex_seed] Syncing seed data to Convex...")
    seed_regions(client, con)
    seed_platforms(client, con)
    seed_clusters(client, con)
    seed_keywords(client, con)
    con.close()
    print("[convex_seed] Done.")


if __name__ == "__main__":
    run()
