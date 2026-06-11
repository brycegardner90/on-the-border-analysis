import sqlite3

conn = sqlite3.connect("/home/claude/otb_analysis/otb_analysis.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

separator = lambda title: print(f"\n{'─'*60}\n📊 {title}\n{'─'*60}")

# ── 1. Location count by ownership era ───────────────────────
separator("Location Count by Ownership Era")
rows = c.execute("""
    SELECT ownership_era,
           COUNT(*) as years,
           MIN(year) as era_start,
           MAX(year) as era_end,
           MIN(location_count) as min_locations,
           MAX(location_count) as max_locations,
           ROUND(AVG(location_count), 1) as avg_locations
    FROM otb_locations
    GROUP BY ownership_era
    ORDER BY MIN(year)
""").fetchall()
for r in rows:
    print(f"  {r['ownership_era']:12} ({r['era_start']}–{r['era_end']}) | "
          f"Min: {r['min_locations']:>3} | Max: {r['max_locations']:>3} | "
          f"Avg: {r['avg_locations']:>5}")

# ── 2. Peak to bankruptcy decline ─────────────────────────────
separator("Peak to Bankruptcy Decline (2007 onward)")
rows = c.execute("""
    SELECT year, location_count, ownership_era,
           ROUND((location_count - 166.0) / 166.0 * 100, 1) AS pct_change_from_peak
    FROM otb_locations
    WHERE year >= 2007
    ORDER BY year
""").fetchall()
for r in rows:
    bar = "▓" * (r['location_count'] // 5)
    print(f"  {r['year']} | {r['location_count']:>3} locations | "
          f"{r['pct_change_from_peak']:>6}% from peak  {bar}")

# ── 3. Fast casual growth vs OTB decline ─────────────────────
separator("Fast Casual Growth vs OTB Locations (2000 onward)")
rows = c.execute("""
    SELECT i.year,
           o.location_count AS otb_locations,
           i.fast_casual_locations,
           ROUND(CAST(i.fast_casual_locations AS REAL) / o.location_count, 1) AS fast_casual_per_otb
    FROM industry_context i
    JOIN otb_locations o ON i.year = o.year
    WHERE i.year >= 2000 AND i.year % 2 = 0
    ORDER BY i.year
""").fetchall()
for r in rows:
    print(f"  {r['year']} | OTB: {r['otb_locations']:>3} | "
          f"Fast Casual: {r['fast_casual_locations']:>6,} | "
          f"Ratio: {r['fast_casual_per_otb']:>6}x per OTB location")

# ── 4. Events during employment window ───────────────────────
separator("Key Events During Bryce's Employment (2014–2016)")
rows = c.execute("""
    SELECT year, event_label, event_type, event_detail
    FROM key_events
    WHERE year BETWEEN 2014 AND 2016
    ORDER BY year
""").fetchall()
for r in rows:
    print(f"  {r['year']} [{r['event_type']:10}] {r['event_label']}")
    print(f"           → {r['event_detail']}")

# ── 5. All events by type ─────────────────────────────────────
separator("All Key Events by Type")
rows = c.execute("""
    SELECT event_type, COUNT(*) as count,
           GROUP_CONCAT(year, ', ') as years
    FROM key_events
    GROUP BY event_type
    ORDER BY count DESC
""").fetchall()
for r in rows:
    print(f"  {r['event_type']:12} ({r['count']} events): {r['years']}")

# ── 6. Bryce employment summary ───────────────────────────────
separator("Bryce Employment Record")
rows = c.execute("SELECT * FROM bryce_employment").fetchall()
for r in rows:
    print(f"  Location:  {r['location']}, {r['city']}, {r['state']}")
    print(f"  Role:      {r['role']}")
    print(f"  Period:    {r['start_month']}/{r['start_year']} → "
          f"{r['end_month']}/{r['end_year']}")
    print(f"  Notes:     {r['notes']}")

# ── 7. OTB location arc summary ───────────────────────────────
separator("Full Location Arc — Confirmed Data Points Only")
rows = c.execute("""
    SELECT year, location_count, ownership_era, source_note
    FROM otb_locations
    WHERE data_quality = 'confirmed'
    ORDER BY year
""").fetchall()
for r in rows:
    print(f"  {r['year']} | {r['location_count']:>3} locations | "
          f"{r['ownership_era']:12} | {r['source_note'][:50]}")

# ── 8. Chili's vs OTB comparison ─────────────────────────────
separator("Chili's vs OTB Location Comparison")
rows = c.execute("""
    SELECT i.year,
           o.location_count AS otb_locations,
           i.chilis_locations,
           ROUND(CAST(i.chilis_locations AS REAL) / o.location_count, 1) AS chilis_per_otb
    FROM industry_context i
    JOIN otb_locations o ON i.year = o.year
    WHERE i.chilis_locations IS NOT NULL
    ORDER BY i.year
""").fetchall()
for r in rows:
    print(f"  {r['year']} | OTB: {r['otb_locations']:>3} | "
          f"Chili's: {r['chilis_locations']:>5} | "
          f"Chili's is {r['chilis_per_otb']}x larger")

conn.close()
print("\n✅ All OTB analysis queries complete.")
