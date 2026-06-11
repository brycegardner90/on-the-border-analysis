import sqlite3
import csv
import os

DB_PATH = "/home/claude/otb_analysis/otb_analysis.db"
OUT_DIR = "/home/claude/otb_analysis/csv"
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

def write_csv(filename, rows, fieldnames):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([dict(r) for r in rows])
    print(f"  ✅ {filename}  ({len(rows)} rows)")

print("\n📁 Exporting OTB Tableau CSVs...\n")

# ── CSV 1: OTB Location Arc ───────────────────────────────────
rows = c.execute("""
    SELECT
        l.year,
        l.location_count,
        l.ownership_era,
        l.data_quality,
        CASE
            WHEN l.year >= 2014 AND l.year <= 2016 THEN 'Bryce Employment'
            ELSE 'Outside Employment'
        END AS employment_period,
        l.source_note
    FROM otb_locations l
    ORDER BY l.year
""").fetchall()
write_csv("01_otb_locations.csv", rows,
    ["year","location_count","ownership_era","data_quality","employment_period","source_note"])

# ── CSV 2: Industry Comparison ────────────────────────────────
rows = c.execute("""
    SELECT
        year,
        fast_casual_locations,
        chipotle_locations,
        chilis_locations,
        casual_dining_share_pct,
        data_quality,
        source_note
    FROM industry_context
    ORDER BY year
""").fetchall()
write_csv("02_industry_context.csv", rows,
    ["year","fast_casual_locations","chipotle_locations","chilis_locations",
     "casual_dining_share_pct","data_quality","source_note"])

# ── CSV 3: Key Events Timeline ────────────────────────────────
rows = c.execute("""
    SELECT
        id, year, event_label, event_type, event_detail,
        CASE
            WHEN year >= 2014 AND year <= 2016 THEN 1
            ELSE 0
        END AS during_bryce_tenure
    FROM key_events
    ORDER BY year, id
""").fetchall()
write_csv("03_key_events.csv", rows,
    ["id","year","event_label","event_type","event_detail","during_bryce_tenure"])

# ── CSV 4: OTB vs Chili's Comparison ─────────────────────────
# Normalize both to index 100 at 2007 (OTB peak) for direct comparison
rows = c.execute("""
    SELECT
        i.year,
        o.location_count AS otb_locations,
        i.chilis_locations,
        i.fast_casual_locations,
        i.chipotle_locations,
        ROUND(CAST(o.location_count AS REAL) / 166 * 100, 1) AS otb_index,
        ROUND(CAST(i.chilis_locations AS REAL) / 1500 * 100, 1) AS chilis_index
    FROM industry_context i
    LEFT JOIN otb_locations o ON i.year = o.year
    ORDER BY i.year
""").fetchall()
write_csv("04_otb_vs_industry.csv", rows,
    ["year","otb_locations","chilis_locations","fast_casual_locations",
     "chipotle_locations","otb_index","chilis_index"])

# ── CSV 5: Employment overlay ─────────────────────────────────
rows = c.execute("""
    SELECT
        id, location, city, state,
        start_year, start_month, end_year, end_month,
        role,
        ROUND(start_year + (start_month - 1.0) / 12.0, 2) AS start_decimal,
        ROUND(end_year + (end_month - 1.0) / 12.0, 2) AS end_decimal,
        notes
    FROM bryce_employment
""").fetchall()
write_csv("05_bryce_employment.csv", rows,
    ["id","location","city","state","start_year","start_month",
     "end_year","end_month","role","start_decimal","end_decimal","notes"])

conn.close()
print("\n✅ All OTB CSVs exported to:", OUT_DIR)
