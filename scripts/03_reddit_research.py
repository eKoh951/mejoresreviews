"""Phase 5 — Reddit research via PRAW (read-only, public posts).

Searches Spanish and English subreddits for discussions about Google reviews,
GBP, local SEO, and reputation management for businesses in Mexico.

Usage:
    python scripts/03_reddit_research.py

Requires .env:
    REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET
    REDDIT_USER_AGENT   (default: mejoresreviews-research/0.1)

Output:
    data/raw/reddit/<YYYY-MM-DD>/posts.parquet
    DuckDB table source_documents updated

Privacy rule: only aggregate themes are stored, never commenter usernames.
The snippet field stores the post title + body excerpt only.
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
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "reddit"
TODAY   = date.today().isoformat()
OUT_DIR = RAW_DIR / TODAY

SEARCH_QUERIES = [
    # Spanish
    "reseñas Google negocio",
    "reseñas falsas Google",
    "como conseguir mas reseñas",
    "Google Business Profile Mexico",
    "eliminar reseña negativa Google",
    "posicionamiento Google Maps",
    # English
    "Google reviews small business Mexico",
    "Google Business Profile reviews",
    "fake Google reviews",
    "how to get more Google reviews restaurant",
    "local SEO restaurant",
    "reputation management small business",
]

SUBREDDITS = [
    "mexico",
    "Entrepreneur",
    "smallbusiness",
    "SEO",
    "marketing",
    "restaurantes",
    "negocios",
]

RESULTS_PER_QUERY = 15


def check_env():
    if not os.getenv("REDDIT_CLIENT_ID") or not os.getenv("REDDIT_CLIENT_SECRET"):
        print("[skip] REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET not set. Skipping Reddit pull.")
        return False
    return True


def build_reddit():
    import praw
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.getenv("REDDIT_USER_AGENT", "mejoresreviews-research/0.1"),
    )


def search_subreddits(reddit, query: str) -> list[dict]:
    rows = []
    for sub in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.search(query, limit=RESULTS_PER_QUERY, sort="relevance"):
                body = (post.selftext or "")[:500].strip()
                rows.append({
                    "query":        query,
                    "subreddit":    sub,
                    "title":        post.title,
                    "url":          f"https://reddit.com{post.permalink}",
                    "snippet":      f"{post.title} — {body}" if body else post.title,
                    "score":        post.score,
                    "num_comments": post.num_comments,
                    "created_utc":  int(post.created_utc),
                    "lang":         "es" if any(
                        c in post.title.lower() for c in ["reseña", "negocio", "google"]
                    ) else "en",
                    "collected_at": TODAY,
                })
        except Exception as e:
            print(f"  [warn] r/{sub} '{query}': {e}")
    return rows


def run():
    if not check_env():
        return

    reddit = build_reddit()
    all_rows = []

    print(f"[reddit] Searching {len(SEARCH_QUERIES)} queries across {len(SUBREDDITS)} subreddits...")
    for q in SEARCH_QUERIES:
        rows = search_subreddits(reddit, q)
        all_rows.extend(rows)
        print(f"  '{q[:50]}': {len(rows)} posts found")

    if not all_rows:
        print("[reddit] No posts found.")
        return

    df = pd.DataFrame(all_rows).drop_duplicates(subset=["url"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "posts.parquet"
    df.to_parquet(out_path, index=False)
    print(f"[reddit] Saved {len(df)} unique posts -> {out_path}")

    _load_source_docs(df)


def _load_source_docs(df):
    if not DB_PATH.exists():
        print("[reddit] DuckDB not found — skipping DB load. Run 00_init_db.py first.")
        return

    con = duckdb.connect(str(DB_PATH))
    existing_urls = {r[0] for r in con.execute("SELECT url FROM source_documents WHERE url IS NOT NULL").fetchall()}

    rows = []
    for _, r in df.iterrows():
        if r["url"] in existing_urls:
            continue
        rows.append((
            str(uuid.uuid4()),
            "reddit",
            r["url"],
            r["title"],
            None,
            TODAY,
            "anecdotal",
            r["snippet"][:1000] if r["snippet"] else None,
            r["lang"],
        ))

    if rows:
        con.executemany(
            "INSERT INTO source_documents VALUES (?,?,?,?,?,?,?,?,?)",
            rows
        )
        print(f"[reddit] Loaded {len(rows)} new source_documents into DuckDB")
    else:
        print("[reddit] All posts already in DuckDB")

    con.close()


if __name__ == "__main__":
    run()
