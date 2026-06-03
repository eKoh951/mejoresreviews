"""Phase 0 â€” initialize DuckDB with seed data (regions, platforms, clusters, keywords)."""

import json
from pathlib import Path
import duckdb

DB_PATH = Path(__file__).parent.parent / "data" / "analytics" / "research.duckdb"


def main():
    con = duckdb.connect(str(DB_PATH))
    _create_tables(con)
    _seed_regions(con)
    _seed_platforms(con)
    _seed_clusters(con)
    _seed_keywords(con)
    con.close()
    print(f"DB initialized at {DB_PATH}")


def _create_tables(con):
    con.executemany("", [])  # no-op; tables created via CREATE IF NOT EXISTS below

    con.execute("""
        CREATE TABLE IF NOT EXISTS regions (
            id       VARCHAR PRIMARY KEY,
            name     VARCHAR NOT NULL,
            level    VARCHAR NOT NULL,  -- city | state | country
            parent   VARCHAR,
            geo_id   VARCHAR            -- Google Ads geo constant
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS platforms (
            id        VARCHAR PRIMARY KEY,
            name      VARCHAR NOT NULL,
            data_type VARCHAR NOT NULL   -- official | inferred | scraped | anecdotal
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS clusters (
            key              VARCHAR PRIMARY KEY,
            label            VARCHAR NOT NULL,
            description      VARCHAR,
            compliance_risk  VARCHAR NOT NULL  -- none | low | medium | high
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id            VARCHAR PRIMARY KEY,
            raw           VARCHAR NOT NULL,
            normalized    VARCHAR NOT NULL,
            language      VARCHAR NOT NULL,  -- es | en | mixed
            variant_group VARCHAR,
            intent        VARCHAR NOT NULL,  -- informational | commercial | transactional | navigational | risky
            is_risky      BOOLEAN NOT NULL DEFAULT false,
            is_seed       BOOLEAN NOT NULL DEFAULT true
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS keyword_metrics (
            id                  VARCHAR PRIMARY KEY,
            keyword_id          VARCHAR NOT NULL REFERENCES keywords(id),
            platform_id         VARCHAR NOT NULL REFERENCES platforms(id),
            region_id           VARCHAR REFERENCES regions(id),
            avg_monthly_searches INTEGER,
            competition          VARCHAR,    -- LOW | MEDIUM | HIGH
            competition_index    FLOAT,      -- 0â€“100
            bid_low              FLOAT,
            bid_high             FLOAT,
            trend_12mo           JSON,       -- array of 12 monthly values
            is_bucketed          BOOLEAN NOT NULL DEFAULT true,
            collected_at         DATE NOT NULL,
            confidence           INTEGER NOT NULL  -- 1â€“3
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS keyword_cluster_map (
            keyword_id  VARCHAR NOT NULL REFERENCES keywords(id),
            cluster_key VARCHAR NOT NULL REFERENCES clusters(key),
            weight       FLOAT NOT NULL DEFAULT 1.0,  -- soft membership 0â€“1
            PRIMARY KEY (keyword_id, cluster_key)
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS source_documents (
            id           VARCHAR PRIMARY KEY,
            platform_id  VARCHAR NOT NULL REFERENCES platforms(id),
            url          VARCHAR,
            title        VARCHAR,
            raw_path     VARCHAR,
            collected_at DATE NOT NULL,
            data_type    VARCHAR NOT NULL,  -- official | inferred | scraped | anecdotal
            snippet      VARCHAR,
            lang         VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS research_log (
            id         VARCHAR PRIMARY KEY,
            phase      VARCHAR NOT NULL,
            action     VARCHAR NOT NULL,
            agent      VARCHAR NOT NULL,
            result     VARCHAR,
            logged_at  TIMESTAMP NOT NULL DEFAULT current_timestamp
        )
    """)

    print("  âœ“ tables created")


def _seed_regions(con):
    rows = [
        ("mx",       "Mexico",         "country", None, "2484"),
        ("mx_chih",  "Chihuahua",      "state",   "mx", "21177"),
        ("mx_juarez","Ciudad JuÃ¡rez",  "city",    "mx_chih", "1010166"),
    ]
    existing = {r[0] for r in con.execute("SELECT id FROM regions").fetchall()}
    new = [r for r in rows if r[0] not in existing]
    if new:
        con.executemany("INSERT INTO regions VALUES (?,?,?,?,?)", new)
        print(f"  [ok] regions seeded ({len(new)} new)")
    else:
        print("  [ok] regions already seeded")


def _seed_platforms(con):
    rows = [
        ("google_ads",  "Google Ads / Keyword Planner", "official"),
        ("gbp",         "Google Business Profile",      "official"),
        ("trends",      "Google Trends",                "official"),
        ("tiktok_cc",   "TikTok Creative Center (Ads)", "inferred"),
        ("tiktok_org",  "TikTok Organic",               "anecdotal"),
        ("reddit",      "Reddit",                       "anecdotal"),
        ("youtube",     "YouTube",                      "inferred"),
        ("serp",        "SERP API",                     "inferred"),
        ("forum",       "Forums / Communities",         "anecdotal"),
        ("manual",      "Manual / Primary Research",    "anecdotal"),
    ]
    existing = {r[0] for r in con.execute("SELECT id FROM platforms").fetchall()}
    new = [r for r in rows if r[0] not in existing]
    if new:
        con.executemany("INSERT INTO platforms VALUES (?,?,?)", new)
        print(f"  [ok] platforms seeded ({len(new)} new)")
    else:
        print("  [ok] platforms already seeded")


def _seed_clusters(con):
    rows = [
        ("get_more_reviews",        "Get more (legitimate) reviews",                 "Demand for earning more authentic reviews from real customers",             "none"),
        ("remove_bad_reviews",      "Remove / handle a bad review",                  "Handling, flagging, or responding to negative reviews",                    "medium"),
        ("respond_to_reviews",      "Respond to reviews",                            "Best practices for replying to reviews",                                   "none"),
        ("appear_on_maps",          "Appear / rank on Google Maps",                  "Improving visibility and position in Maps/local search",                   "low"),
        ("gbp_setup",               "GBP setup & optimization",                      "Creating, completing, and optimizing Google Business Profile",             "none"),
        ("qr_link_request",         "QR / link review request",                      "Tools and flows to make leaving a review frictionless",                    "low"),
        ("restaurant_marketing",    "Restaurant / food-business marketing",           "General marketing for restaurants, cafÃ©s, food businesses",                "none"),
        ("local_seo",               "Local SEO",                                     "On-site and off-site tactics to improve local search ranking",             "none"),
        ("reputation_management",   "Reputation management",                         "Monitoring and improving overall online reputation",                       "low"),
        ("fake_graymarket",         "Fake / bought / gated reviews",                 "Demand for non-compliant tactics â€” studied to design counter-offers ONLY", "high"),
        ("customer_service_recovery","Service quality & customer recovery",           "Using feedback to improve service and recover dissatisfied customers",     "none"),
        ("competitor_software_agency","Competing software / agencies",               "Understanding the competitive landscape",                                  "none"),
    ]
    existing = {r[0] for r in con.execute("SELECT key FROM clusters").fetchall()}
    new = [r for r in rows if r[0] not in existing]
    if new:
        con.executemany("INSERT INTO clusters VALUES (?,?,?,?)", new)
        print(f"  [ok] clusters seeded ({len(new)} new)")
    else:
        print("  [ok] clusters already seeded")


def _seed_keywords(con):
    """Load seed keywords (Phase 1). Each seed covers one or more clusters."""
    seeds = [
        # (id, raw, normalized, language, variant_group, intent, is_risky, cluster_keys)

        # â”€â”€ get_more_reviews â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_001", "cÃ³mo conseguir mÃ¡s reseÃ±as",             "como conseguir mas resenas",         "es", "get_reviews", "informational", False, ["get_more_reviews"]),
        ("kw_002", "cÃ³mo pedir reseÃ±as a clientes",          "como pedir resenas a clientes",      "es", "get_reviews", "informational", False, ["get_more_reviews"]),
        ("kw_003", "cÃ³mo obtener mÃ¡s reseÃ±as en Google",     "como obtener mas resenas en google", "es", "get_reviews", "informational", False, ["get_more_reviews"]),
        ("kw_004", "get more Google reviews",                "get more google reviews",            "en", "get_reviews", "commercial",    False, ["get_more_reviews"]),
        ("kw_005", "how to get more reviews on Google Maps", "how to get more reviews on google maps","en","get_reviews","informational", False, ["get_more_reviews"]),
        ("kw_006", "mÃ¡s reseÃ±as Google Maps",                "mas resenas google maps",            "es", "get_reviews", "commercial",    False, ["get_more_reviews"]),
        ("kw_007", "cÃ³mo mejorar mi calificaciÃ³n en Google", "como mejorar mi calificacion en google","es","rating_improve","informational",False,["get_more_reviews","reputation_management"]),
        ("kw_008", "increase Google reviews",                "increase google reviews",            "en", "get_reviews", "commercial",    False, ["get_more_reviews"]),

        # â”€â”€ remove_bad_reviews â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_009", "cÃ³mo quitar una mala reseÃ±a de Google",  "como quitar una mala resena de google","es","remove_review","commercial",  False, ["remove_bad_reviews"]),
        ("kw_010", "eliminar reseÃ±a negativa Google",        "eliminar resena negativa google",    "es", "remove_review","commercial",   False, ["remove_bad_reviews"]),
        ("kw_011", "me dejaron una reseÃ±a falsa",            "me dejaron una resena falsa",        "es", "remove_review","informational", False, ["remove_bad_reviews","fake_graymarket"]),
        ("kw_012", "remove bad Google review",               "remove bad google review",           "en", "remove_review","commercial",   False, ["remove_bad_reviews"]),
        ("kw_013", "how to delete a Google review",          "how to delete a google review",      "en", "remove_review","informational", False, ["remove_bad_reviews"]),
        ("kw_014", "reportar reseÃ±a falsa Google",           "reportar resena falsa google",       "es", "remove_review","informational", False, ["remove_bad_reviews"]),

        # â”€â”€ respond_to_reviews â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_015", "cÃ³mo responder reseÃ±as de Google",       "como responder resenas de google",   "es", None,           "informational", False, ["respond_to_reviews"]),
        ("kw_016", "responder reseÃ±as negativas",            "responder resenas negativas",        "es", None,           "informational", False, ["respond_to_reviews"]),
        ("kw_017", "respond to Google reviews",              "respond to google reviews",          "en", None,           "informational", False, ["respond_to_reviews"]),

        # â”€â”€ appear_on_maps â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_018", "cÃ³mo salir primero en Google Maps",      "como salir primero en google maps",  "es", None,           "commercial",    False, ["appear_on_maps"]),
        ("kw_019", "mi negocio no aparece en Google",        "mi negocio no aparece en google",    "es", None,           "informational", False, ["appear_on_maps","gbp_setup"]),
        ("kw_020", "aparecer primero en Google Maps",        "aparecer primero en google maps",    "es", None,           "commercial",    False, ["appear_on_maps"]),
        ("kw_021", "appear first on Google Maps",            "appear first on google maps",        "en", None,           "commercial",    False, ["appear_on_maps"]),
        ("kw_022", "cÃ³mo posicionarme en Google Maps",       "como posicionarme en google maps",   "es", None,           "commercial",    False, ["appear_on_maps","local_seo"]),

        # â”€â”€ gbp_setup â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_023", "Google Business Profile MÃ©xico",         "google business profile mexico",     "es", None,           "navigational",  False, ["gbp_setup"]),
        ("kw_024", "crear perfil de negocio en Google",      "crear perfil de negocio en google",  "es", None,           "informational", False, ["gbp_setup"]),
        ("kw_025", "Google Business Profile reviews",        "google business profile reviews",    "en", None,           "informational", False, ["gbp_setup","get_more_reviews"]),
        ("kw_026", "optimizar perfil de Google Mi Negocio",  "optimizar perfil de google mi negocio","es",None,          "informational", False, ["gbp_setup"]),

        # â”€â”€ qr_link_request â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_027", "cÃ³digo QR para reseÃ±as Google",          "codigo qr para resenas google",      "es", None,           "commercial",    False, ["qr_link_request"]),
        ("kw_028", "QR code for Google reviews",             "qr code for google reviews",         "en", None,           "commercial",    False, ["qr_link_request"]),
        ("kw_029", "link para dejar reseÃ±a Google",          "link para dejar resena google",      "es", None,           "commercial",    False, ["qr_link_request"]),
        ("kw_030", "cÃ³mo pedir reseÃ±as con QR",              "como pedir resenas con qr",          "es", None,           "informational", False, ["qr_link_request"]),

        # â”€â”€ restaurant_marketing â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_031", "marketing para restaurantes",            "marketing para restaurantes",        "es", None,           "commercial",    False, ["restaurant_marketing"]),
        ("kw_032", "cÃ³mo atraer mÃ¡s clientes a mi restaurante","como atraer mas clientes a mi restaurante","es",None,    "informational", False, ["restaurant_marketing"]),
        ("kw_033", "publicidad para restaurantes en MÃ©xico",  "publicidad para restaurantes en mexico","es",None,        "commercial",    False, ["restaurant_marketing"]),
        ("kw_034", "marketing for restaurants",              "marketing for restaurants",          "en", None,           "commercial",    False, ["restaurant_marketing"]),
        ("kw_035", "cÃ³mo atraer clientes a mi cafÃ©",         "como atraer clientes a mi cafe",     "es", None,           "informational", False, ["restaurant_marketing"]),

        # â”€â”€ local_seo â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_036", "SEO local para restaurantes",            "seo local para restaurantes",        "es", None,           "commercial",    False, ["local_seo","restaurant_marketing"]),
        ("kw_037", "local SEO for restaurants",              "local seo for restaurants",          "en", None,           "commercial",    False, ["local_seo","restaurant_marketing"]),
        ("kw_038", "posicionamiento local Google",           "posicionamiento local google",       "es", None,           "commercial",    False, ["local_seo"]),

        # â”€â”€ reputation_management â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_039", "manejo de reputaciÃ³n online",            "manejo de reputacion online",        "es", None,           "commercial",    False, ["reputation_management"]),
        ("kw_040", "reputation management for small businesses","reputation management for small businesses","en",None,  "commercial",    False, ["reputation_management"]),
        ("kw_041", "cÃ³mo mejorar la reputaciÃ³n de mi negocio","como mejorar la reputacion de mi negocio","es",None,      "informational", False, ["reputation_management"]),

        # â”€â”€ fake_graymarket (studied only â€” NEVER recommended) â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_042", "comprar reseÃ±as Google",                 "comprar resenas google",             "es", None,           "risky",         True,  ["fake_graymarket"]),
        ("kw_043", "buy Google reviews",                     "buy google reviews",                 "en", None,           "risky",         True,  ["fake_graymarket"]),
        ("kw_044", "reseÃ±as falsas Google",                  "resenas falsas google",              "es", None,           "risky",         True,  ["fake_graymarket"]),
        ("kw_045", "cÃ³mo quitar todas las reseÃ±as negativas", "como quitar todas las resenas negativas","es",None,       "risky",         True,  ["fake_graymarket","remove_bad_reviews"]),

        # â”€â”€ customer_service_recovery â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_046", "cÃ³mo recuperar a un cliente insatisfecho","como recuperar a un cliente insatisfecho","es",None,      "informational", False, ["customer_service_recovery"]),
        ("kw_047", "cÃ³mo responder a una queja de cliente",  "como responder a una queja de cliente","es",None,         "informational", False, ["customer_service_recovery","respond_to_reviews"]),

        # â”€â”€ variant group â€” review terms â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ("kw_048", "reseÃ±as para restaurante",               "resenas para restaurante",           "es", "reviews_term", "informational", False, ["get_more_reviews","restaurant_marketing"]),
        ("kw_049", "opiniones de restaurantes en Google",    "opiniones de restaurantes en google","es", "reviews_term", "informational", False, ["get_more_reviews"]),
        ("kw_050", "calificaciones Google Maps restaurante",  "calificaciones google maps restaurante","es","reviews_term","informational",False,["get_more_reviews","appear_on_maps"]),
    ]

    existing = {r[0] for r in con.execute("SELECT id FROM keywords").fetchall()}

    kw_rows    = [(s[0],s[1],s[2],s[3],s[4],s[5],s[6],True) for s in seeds if s[0] not in existing]
    map_rows   = [(s[0], ck) for s in seeds if s[0] not in existing for ck in s[7]]

    if kw_rows:
        con.executemany("INSERT INTO keywords VALUES (?,?,?,?,?,?,?,?)", kw_rows)
        con.executemany("INSERT INTO keyword_cluster_map (keyword_id, cluster_key) VALUES (?,?)", map_rows)
        print(f"  [ok] keywords seeded ({len(kw_rows)} new, {len(map_rows)} cluster mappings)")
    else:
        print("  [ok] keywords already seeded")


if __name__ == "__main__":
    main()

