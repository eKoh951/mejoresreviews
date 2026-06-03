"""Phase 2 — pull keyword metrics from Google Ads API (generateKeywordHistoricalMetrics).

Usage:
    python scripts/02_google_ads_keywords.py

Requires these .env vars (see .env.example):
    GOOGLE_ADS_DEVELOPER_TOKEN
    GOOGLE_ADS_CLIENT_ID
    GOOGLE_ADS_CLIENT_SECRET
    GOOGLE_ADS_REFRESH_TOKEN
    GOOGLE_ADS_LOGIN_CUSTOMER_ID

Output:
    data/raw/google_ads/<YYYY-MM-DD>/keyword_metrics.parquet
    DuckDB table keyword_metrics updated
"""

import os
import sys
import json
import uuid
from datetime import date, datetime
from pathlib import Path

import duckdb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_PATH   = Path(__file__).parent.parent / "data" / "analytics" / "research.duckdb"
RAW_DIR   = Path(__file__).parent.parent / "data" / "raw" / "google_ads"
TODAY     = date.today().isoformat()
OUT_DIR   = RAW_DIR / TODAY

# Google Ads geo IDs for our targets
GEO_TARGETS = {
    "mx":        2484,      # Mexico
    "mx_chih":   21177,     # Chihuahua (state)
    "mx_juarez": 1010166,   # Ciudad Juarez
}

LANGUAGE_ID = 1003  # Spanish


def check_env():
    required = [
        "GOOGLE_ADS_DEVELOPER_TOKEN",
        "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET",
        "GOOGLE_ADS_REFRESH_TOKEN",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
    ]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        print(f"[skip] Missing env vars: {', '.join(missing)}")
        print("       Set them in .env and re-run. Skipping Google Ads pull.")
        return False
    return True


def build_google_ads_client():
    from google.ads.googleads.client import GoogleAdsClient
    config = {
        "developer_token":  os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
        "client_id":        os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret":    os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token":    os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
        "login_customer_id":os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"],
        "use_proto_plus":   True,
    }
    return GoogleAdsClient.load_from_dict(config)


def fetch_keyword_metrics(client, keywords: list[str], geo_id: int) -> list[dict]:
    """Call generateKeywordHistoricalMetrics for a batch of keywords."""
    kp_service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    request.customer_id = os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"]
    request.keywords.extend(keywords)
    request.geo_target_constants.append(
        f"geoTargetConstants/{geo_id}"
    )
    request.language = f"languageConstants/{LANGUAGE_ID}"

    rows = []
    response = kp_service.generate_keyword_historical_metrics(request=request)
    for result in response.results:
        metrics = result.keyword_metrics
        monthly = [
            m.monthly_searches
            for m in metrics.monthly_search_volumes
        ] if metrics.monthly_searches else []
        rows.append({
            "keyword":           result.text,
            "avg_monthly":       metrics.avg_monthly_searches,
            "competition":       metrics.competition.name,
            "competition_index": metrics.competition_index,
            "bid_low":           metrics.low_top_of_page_bid_micros / 1e6 if metrics.low_top_of_page_bid_micros else None,
            "bid_high":          metrics.high_top_of_page_bid_micros / 1e6 if metrics.high_top_of_page_bid_micros else None,
            "monthly_volumes":   json.dumps(monthly),
            "geo_id":            geo_id,
            "collected_at":      TODAY,
            "is_bucketed":       True,  # Google Ads always returns bucketed values
        })
    return rows


def run():
    if not check_env():
        return

    con = duckdb.connect(str(DB_PATH))
    keywords = [r[0] for r in con.execute("SELECT raw FROM keywords").fetchall()]
    print(f"[google_ads] Pulling metrics for {len(keywords)} keywords across {len(GEO_TARGETS)} regions...")

    client = build_google_ads_client()
    all_rows = []

    BATCH = 20  # API limit per request
    for region_key, geo_id in GEO_TARGETS.items():
        print(f"  region: {region_key} (geo {geo_id})")
        for i in range(0, len(keywords), BATCH):
            batch = keywords[i:i+BATCH]
            try:
                rows = fetch_keyword_metrics(client, batch, geo_id)
                for r in rows:
                    r["region_key"] = region_key
                all_rows.extend(rows)
            except Exception as e:
                print(f"  [warn] batch {i//BATCH} / {region_key} failed: {e}")

    if not all_rows:
        print("[google_ads] No data returned.")
        return

    df = pd.DataFrame(all_rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "keyword_metrics.parquet"
    df.to_parquet(out_path, index=False)
    print(f"[google_ads] Saved {len(df)} rows -> {out_path}")

    _load_into_duckdb(con, df)
    con.close()


def _load_into_duckdb(con, df):
    platform_id = con.execute(
        "SELECT id FROM platforms WHERE id = 'google_ads'"
    ).fetchone()
    if not platform_id:
        print("[google_ads] Platform 'google_ads' not found in DB. Run 00_init_db.py first.")
        return

    region_map = {r[0]: r[0] for r in con.execute("SELECT id FROM regions").fetchall()}

    rows = []
    for _, row in df.iterrows():
        region_id = region_map.get(row["region_key"])
        kw_row = con.execute(
            "SELECT id FROM keywords WHERE raw = ?", [row["keyword"]]
        ).fetchone()
        if not kw_row:
            continue
        rows.append((
            str(uuid.uuid4()),
            kw_row[0],
            "google_ads",
            region_id,
            int(row["avg_monthly"]) if pd.notna(row["avg_monthly"]) else None,
            row["competition"] if pd.notna(row["competition"]) else None,
            float(row["competition_index"]) if pd.notna(row["competition_index"]) else None,
            float(row["bid_low"]) if pd.notna(row["bid_low"]) else None,
            float(row["bid_high"]) if pd.notna(row["bid_high"]) else None,
            row["monthly_volumes"],
            True,
            TODAY,
            2,  # confidence: official but bucketed = 2
        ))

    if rows:
        con.executemany(
            "INSERT OR IGNORE INTO keyword_metrics VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            rows
        )
        print(f"[google_ads] Loaded {len(rows)} metric rows into DuckDB")


if __name__ == "__main__":
    run()
