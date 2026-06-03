"""Phase 5 — YouTube Data API v3 research (read-only, public videos).

Finds videos about Google reviews, GBP, local SEO, and reputation management
targeting Mexico/Spanish-speaking business owners.

Usage:
    python scripts/04_youtube_research.py

Requires .env:
    YOUTUBE_API_KEY

Output:
    data/raw/youtube/<YYYY-MM-DD>/videos.parquet
    DuckDB table source_documents updated

Free quota: ~10,000 units/day; search.list costs 100 units/call.
This script issues ≤20 search calls (≤2,000 units) plus cheap videos.list calls.
"""

import os
import uuid
from datetime import date
from pathlib import Path

import duckdb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(__file__).parent.parent / "data" / "analytics" / "research.duckdb"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "youtube"
TODAY   = date.today().isoformat()
OUT_DIR = RAW_DIR / TODAY

SEARCH_QUERIES = [
    # Spanish — core intent
    "cómo conseguir más reseñas en Google",
    "cómo pedir reseñas a clientes restaurante",
    "Google Business Profile México tutorial",
    "cómo aparecer en Google Maps",
    "cómo responder reseñas negativas",
    "eliminar reseña falsa Google",
    "marketing para restaurantes México",
    "posicionamiento Google Maps restaurante",
    "reputación online negocio México",
    # English — research + competitive landscape
    "how to get more Google reviews restaurant",
    "Google Business Profile optimization 2024",
    "local SEO for restaurants",
    "respond to negative Google reviews",
    "reputation management small business",
]

RESULTS_PER_QUERY = 10


def check_env():
    if not os.getenv("YOUTUBE_API_KEY"):
        print("[skip] YOUTUBE_API_KEY not set. Skipping YouTube pull.")
        return False
    return True


def build_youtube():
    from googleapiclient.discovery import build
    return build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])


def search_videos(youtube, query: str) -> list[dict]:
    try:
        response = youtube.search().list(
            q=query,
            part="id,snippet",
            type="video",
            relevanceLanguage="es",
            regionCode="MX",
            maxResults=RESULTS_PER_QUERY,
            order="relevance",
        ).execute()
    except Exception as e:
        print(f"  [warn] search '{query}': {e}")
        return []

    rows = []
    for item in response.get("items", []):
        vid_id = item["id"].get("videoId")
        if not vid_id:
            continue
        snip = item.get("snippet", {})
        rows.append({
            "query":        query,
            "video_id":     vid_id,
            "title":        snip.get("title", ""),
            "description":  (snip.get("description", "") or "")[:500],
            "channel":      snip.get("channelTitle", ""),
            "published_at": snip.get("publishedAt", ""),
            "url":          f"https://www.youtube.com/watch?v={vid_id}",
            "lang":         "es" if any(
                c in (snip.get("title", "") + snip.get("description", "")).lower()
                for c in ["reseña", "negocio", "restaurante", "google maps"]
            ) else "en",
            "collected_at": TODAY,
        })
    return rows


def enrich_stats(youtube, rows: list[dict]) -> list[dict]:
    video_ids = [r["video_id"] for r in rows]
    if not video_ids:
        return rows

    stats_map = {}
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        try:
            resp = youtube.videos().list(
                part="statistics",
                id=",".join(batch),
            ).execute()
            for item in resp.get("items", []):
                s = item.get("statistics", {})
                stats_map[item["id"]] = {
                    "views":    int(s.get("viewCount", 0)),
                    "likes":    int(s.get("likeCount", 0)),
                    "comments": int(s.get("commentCount", 0)),
                }
        except Exception as e:
            print(f"  [warn] stats batch: {e}")

    for r in rows:
        stats = stats_map.get(r["video_id"], {})
        r["views"]    = stats.get("views")
        r["likes"]    = stats.get("likes")
        r["comments"] = stats.get("comments")
    return rows


def run():
    if not check_env():
        return

    youtube = build_youtube()
    all_rows = []

    print(f"[youtube] Searching {len(SEARCH_QUERIES)} queries (MX/es)...")
    for q in SEARCH_QUERIES:
        rows = search_videos(youtube, q)
        all_rows.extend(rows)
        print(f"  '{q[:55]}': {len(rows)} videos")

    if not all_rows:
        print("[youtube] No videos found.")
        return

    df = pd.DataFrame(all_rows).drop_duplicates(subset=["video_id"])
    print(f"[youtube] Enriching stats for {len(df)} unique videos...")
    records = enrich_stats(youtube, df.to_dict("records"))
    df = pd.DataFrame(records)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "videos.parquet"
    df.to_parquet(out_path, index=False)
    print(f"[youtube] Saved {len(df)} videos -> {out_path}")

    _load_source_docs(df)


def _load_source_docs(df):
    if not DB_PATH.exists():
        print("[youtube] DuckDB not found — skipping DB load. Run 00_init_db.py first.")
        return

    con = duckdb.connect(str(DB_PATH))
    existing_urls = {r[0] for r in con.execute("SELECT url FROM source_documents WHERE url IS NOT NULL").fetchall()}

    rows = []
    for _, r in df.iterrows():
        if r["url"] in existing_urls:
            continue
        snippet = f"{r['title']} — {r['description']}" if r.get("description") else r["title"]
        rows.append((
            str(uuid.uuid4()),
            "youtube",
            r["url"],
            r["title"],
            None,
            TODAY,
            "inferred",
            snippet[:1000],
            r["lang"],
        ))

    if rows:
        con.executemany(
            "INSERT INTO source_documents VALUES (?,?,?,?,?,?,?,?,?)",
            rows
        )
        print(f"[youtube] Loaded {len(rows)} new source_documents into DuckDB")
    else:
        print("[youtube] All videos already in DuckDB")

    con.close()


if __name__ == "__main__":
    run()
