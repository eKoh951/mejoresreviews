"""Phase 5 — SERP + People-Also-Ask research via Serper.dev.

Usage:
    python scripts/05_serp_research.py

Requires .env:
    SERPER_API_KEY

Output:
    data/raw/serp/<YYYY-MM-DD>/results.parquet
    DuckDB table source_documents updated
"""

import os
import json
import uuid
from datetime import date
from pathlib import Path

import duckdb
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(__file__).parent.parent / "data" / "analytics" / "research.duckdb"
RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "serp"
TODAY   = date.today().isoformat()
OUT_DIR = RAW_DIR / TODAY

SERPER_URL = "https://google.serper.dev/search"


def check_env():
    if not os.getenv("SERPER_API_KEY"):
        print("[skip] SERPER_API_KEY not set in .env. Skipping SERP pull.")
        return False
    return True


def serp_query(query: str, gl: str = "mx", hl: str = "es") -> dict:
    headers = {
        "X-API-KEY":    os.environ["SERPER_API_KEY"],
        "Content-Type": "application/json",
    }
    payload = {"q": query, "gl": gl, "hl": hl, "num": 10}
    resp = requests.post(SERPER_URL, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def run():
    if not check_env():
        return

    con = duckdb.connect(str(DB_PATH))
    seeds = [r[0] for r in con.execute(
        "SELECT raw FROM keywords WHERE is_seed = true AND is_risky = false LIMIT 30"
    ).fetchall()]

    print(f"[serp] Querying {len(seeds)} seed keywords (MX/es)...")

    all_rows = []
    paa_rows = []

    for kw in seeds:
        try:
            data = serp_query(kw)
            for r in data.get("organic", []):
                all_rows.append({
                    "query":        kw,
                    "type":         "organic",
                    "title":        r.get("title"),
                    "url":          r.get("link"),
                    "snippet":      r.get("snippet"),
                    "position":     r.get("position"),
                    "collected_at": TODAY,
                })
            for q in data.get("peopleAlsoAsk", []):
                paa_rows.append({
                    "query":        kw,
                    "type":         "paa",
                    "question":     q.get("question"),
                    "snippet":      q.get("snippet"),
                    "url":          q.get("link"),
                    "collected_at": TODAY,
                })
            print(f"  {kw[:50]}: {len(data.get('organic',[]))} results, {len(data.get('peopleAlsoAsk',[]))} PAA")
        except Exception as e:
            print(f"  [warn] failed for '{kw}': {e}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if all_rows:
        df = pd.DataFrame(all_rows)
        out_path = OUT_DIR / "organic.parquet"
        df.to_parquet(out_path, index=False)
        print(f"[serp] Saved {len(df)} organic rows -> {out_path}")
        _load_source_docs(con, df, "organic")

    if paa_rows:
        df_paa = pd.DataFrame(paa_rows)
        out_path_paa = OUT_DIR / "paa.parquet"
        df_paa.to_parquet(out_path_paa, index=False)
        print(f"[serp] Saved {len(df_paa)} PAA rows -> {out_path_paa}")
        _load_source_docs(con, df_paa, "paa")

    con.close()


def _load_source_docs(con, df, doc_type: str):
    rows = []
    for _, r in df.iterrows():
        rows.append((
            str(uuid.uuid4()),
            "serp",
            r.get("url"),
            r.get("title") or r.get("question"),
            None,
            TODAY,
            "inferred",
            r.get("snippet"),
            "es",
        ))
    if rows:
        con.executemany(
            "INSERT INTO source_documents VALUES (?,?,?,?,?,?,?,?,?)",
            rows
        )
        print(f"[serp] Loaded {len(rows)} {doc_type} source_documents into DuckDB")


if __name__ == "__main__":
    run()
