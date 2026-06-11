import sqlite3
import os

DB_PATH = "/home/claude/otb_analysis/otb_analysis.db"

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ─────────────────────────────────────────────
# TABLE 1: otb_locations
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE otb_locations (
    year            INTEGER PRIMARY KEY,
    location_count  INTEGER,
    ownership_era   TEXT,      -- 'Independent' | 'Brinker' | 'Golden Gate' | 'Argonne' | 'Bankruptcy' | 'Pappas'
    data_quality    TEXT,      -- 'confirmed' | 'estimated'
    source_note     TEXT
)
""")

locations = [
    # Confirmed anchors
    (1982, 1,   'Independent', 'confirmed', 'Founded Dallas TX — first location'),
    (1994, 21,  'Brinker',     'confirmed', 'Encyclopedia.com — Brinker acquisition year'),
    (2001, 100, 'Brinker',     'confirmed', 'Restaurant Dive / bankruptcy docs — confirmed milestone'),
    (2005, 135, 'Brinker',     'confirmed', 'Brinker 2005 Annual Report — "added 8 for total of 135"'),
    (2007, 166, 'Brinker',     'confirmed', 'Multiple sources — peak location count confirmed'),
    (2010, 161, 'Golden Gate', 'confirmed', 'Brinker sale press release — 160-162 at time of sale'),
    (2014, 150, 'Argonne',     'confirmed', 'Argonne Capital acquisition — ~150 locations'),
    (2020, 100, 'Argonne',     'confirmed', 'Wikipedia / Technomic — confirmed'),
    (2021, 125, 'Argonne',     'confirmed', 'Technomic Ignite data — post-COVID rebound'),
    (2023, 120, 'Argonne',     'confirmed', 'Technomic — sales down 3% YoY, 120 locations'),
    (2025, 55,  'Pappas',      'confirmed', 'Post-bankruptcy Pappas acquisition — ~55 surviving locations'),

    # Estimated — interpolated between confirmed anchors
    (1983, 2,   'Independent', 'estimated', 'Est: early growth, Dallas area expansion begins'),
    (1984, 3,   'Independent', 'estimated', 'Est: interpolated'),
    (1985, 5,   'Independent', 'estimated', 'Est: interpolated'),
    (1986, 7,   'Independent', 'estimated', 'Est: interpolated'),
    (1987, 9,   'Independent', 'estimated', 'Est: interpolated'),
    (1988, 11,  'Independent', 'estimated', 'Est: interpolated'),
    (1989, 13,  'Independent', 'estimated', 'Est: interpolated'),
    (1990, 15,  'Independent', 'estimated', 'Est: interpolated'),
    (1991, 17,  'Independent', 'estimated', 'Est: interpolated'),
    (1992, 19,  'Independent', 'estimated', 'Est: interpolated'),
    (1993, 20,  'Independent', 'estimated', 'Est: interpolated — just before Brinker acquisition'),
    (1995, 28,  'Brinker',     'estimated', 'Est: franchising launched 1996; accelerating growth'),
    (1996, 38,  'Brinker',     'estimated', 'Est: franchise program launched March 1996'),
    (1997, 52,  'Brinker',     'estimated', 'Est: franchise expansion — Columbus OH locations confirmed 1997'),
    (1998, 65,  'Brinker',     'estimated', 'Est: interpolated between 1997 and 2001'),
    (1999, 78,  'Brinker',     'estimated', 'Est: interpolated'),
    (2000, 90,  'Brinker',     'estimated', 'Est: interpolated — approaching 100 milestone'),
    (2002, 110, 'Brinker',     'estimated', 'Est: interpolated between 2001 and 2005'),
    (2003, 120, 'Brinker',     'estimated', 'Est: interpolated'),
    (2004, 127, 'Brinker',     'estimated', 'Est: interpolated — approaching 135 in 2005'),
    (2006, 153, 'Brinker',     'estimated', 'Est: interpolated between 2005 and 2007 peak'),
    (2008, 164, 'Brinker',     'estimated', 'Est: slight pullback from 2007 peak — decline begins 2008'),
    (2009, 162, 'Brinker',     'estimated', 'Est: continued slow decline pre-sale'),
    (2011, 158, 'Golden Gate', 'estimated', 'Est: interpolated between 2010 and 2014'),
    (2012, 155, 'Golden Gate', 'estimated', 'Est: interpolated — PE cost-cutting, closures begin'),
    (2013, 152, 'Golden Gate', 'estimated', 'Est: interpolated — approaching Argonne acquisition'),
    (2015, 145, 'Argonne',     'estimated', 'Est: interpolated — Bryce last year, closures accelerating'),
    (2016, 140, 'Argonne',     'estimated', 'Est: Alpharetta closure this year — suburban market exits'),
    (2017, 135, 'Argonne',     'estimated', 'Est: continued rationalization'),
    (2018, 130, 'Argonne',     'estimated', 'Est: interpolated'),
    (2019, 128, 'Argonne',     'estimated', 'Est: interpolated — pre-COVID struggling'),
    (2022, 122, 'Argonne',     'estimated', 'Est: between 2021 rebound (125) and 2023 (120)'),
    (2024, 80,  'Argonne',     'estimated', 'Est: pre-bankruptcy rapid closure acceleration'),
]

c.executemany("""
INSERT INTO otb_locations (year, location_count, ownership_era, data_quality, source_note)
VALUES (?, ?, ?, ?, ?)
""", locations)

# ─────────────────────────────────────────────
# TABLE 2: industry_context
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE industry_context (
    year                    INTEGER PRIMARY KEY,
    fast_casual_locations   INTEGER,   -- Total US fast casual locations
    chipotle_locations      INTEGER,   -- Chipotle US locations (proxy for fast casual Tex-Mex pressure)
    chilis_locations        INTEGER,   -- Chili's US locations (direct casual dining comparison)
    casual_dining_share_pct REAL,      -- Casual dining % share of Top 500 restaurant sales
    data_quality            TEXT,
    source_note             TEXT
)
""")

industry = [
    # year, fast_casual, chipotle, chilis, casual_share, quality, source
    (2000, 8000,  None, 800,  None, 'estimated', 'Est fast casual; Chili\'s pre-1000 milestone'),
    (2004, 11000, 500,  1000, None, 'estimated', 'Chili\'s hits 1,000 locations; Chipotle ~500 units'),
    (2010, 17000, 1084, 1200, 20.3, 'confirmed', 'Technomic/SEC; Chipotle 10-K 2010; casual share 2013 baseline'),
    (2013, 19231, 1595, 1400, 20.3, 'confirmed', 'NPD Group; Chipotle 10-K; Technomic Top 500 2013 share'),
    (2015, 27925, 1931, 1500, 18.7, 'confirmed', 'Technomic; Chipotle 10-K 2015; Top 500 share declining'),
    (2017, 25118, 2198, 1400, 18.0, 'confirmed', 'NPD Fall 2017 ReCount; Chipotle 10-K 2017'),
    (2018, 28000, 2452, 1350, 18.7, 'confirmed', 'Technomic Top 500; Chipotle 10-K 2018'),
    (2019, 30000, 2580, 1228, 18.0, 'estimated', 'Brinker 10-K 2019; Chipotle 10-K 2019'),
    (2020, 32000, 2724, 1610, 17.5, 'estimated', 'COVID year; Chipotle 10-K 2020; Chili\'s Wikipedia'),
    (2021, 35000, 2966, 1400, 18.0, 'estimated', 'Post-COVID rebound estimates'),
    (2023, 40000, 3315, 1231, 18.0, 'estimated', 'Chipotle 10-K 2023; Chili\'s Statista 2023'),
    (2025, 44098, 3700, 1300, 18.5, 'estimated', 'Technomic projection; Chili\'s resurgence era'),
]

c.executemany("""
INSERT INTO industry_context
    (year, fast_casual_locations, chipotle_locations, chilis_locations,
     casual_dining_share_pct, data_quality, source_note)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", industry)

# ─────────────────────────────────────────────
# TABLE 3: key_events
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE key_events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    year         INTEGER NOT NULL,
    event_label  TEXT NOT NULL,
    event_type   TEXT NOT NULL,  -- 'founding' | 'acquisition' | 'bankruptcy' | 'external' | 'brand' | 'employment'
    event_detail TEXT
)
""")

events = [
    (1982, 'Founded in Dallas',                     'founding',    'First location opens Oct 29, 1982 — "On The Border South Texas Café"'),
    (1994, 'Brinker International acquires OTB',    'acquisition', 'Acquired for undisclosed sum; 21 units at time of sale; franchise program follows'),
    (1996, 'Franchise program launches',            'brand',       'Brinker begins franchising OTB — accelerates national expansion'),
    (2001, '100 domestic locations milestone',      'brand',       'Chain crosses 100 US locations under Brinker ownership'),
    (2005, '135 locations — first $2M day',         'brand',       'Cinco de Mayo sets all-time single-day sales record; 8 new locations added'),
    (2007, 'Peak: 166 locations',                   'brand',       'All-time high location count; casual dining still dominant'),
    (2008, 'Casual dining decline begins',          'external',    'Fast casual growth accelerates; OTB sales and unit count begin falling'),
    (2010, 'Brinker sells OTB to Golden Gate',      'acquisition', '$180M sale to Golden Gate Capital PE; Brinker refocuses on Chili\'s'),
    (2013, 'Fast casual hits 19,231 US locations',  'external',    'NPD Group — fast casual growing at 7% CAGR; casual dining losing share'),
    (2014, 'Golden Gate sells to Argonne Capital',  'acquisition', 'Second PE sale in 4 years; Argonne also owns Applebee\'s/IHOP franchises'),
    (2014, 'Bryce starts at Alpharetta location',   'employment',  'Jan 2014 — 1st Assistant Manager, Alpharetta GA; Argonne acquisition same month'),
    (2015, 'Understaffing/cheap promo era peaks',   'brand',       '$3 meltdown margarita push; tortilla station chronically unstaffed; FOH stretched'),
    (2016, 'Bryce leaves; Alpharetta closes',       'employment',  'Jan 2016 departure; Alpharetta location subsequently closed — suburban market exit'),
    (2018, 'OTB sales 36% below 2006 peak',        'external',    'Technomic data — decade of decline confirmed; never recovered to Brinker-era levels'),
    (2020, 'COVID accelerates decline',             'external',    'Dining room closures devastate full-service casual dining; OTB drops to ~100 locations'),
    (2021, 'Brief post-COVID rebound',              'brand',       'Locations tick back up to 125; sales recover partially but not to pre-COVID levels'),
    (2023, 'Sales down 3% — 120 locations',        'external',    'Technomic: OTB still below pre-COVID volumes; inflation and traffic decline continue'),
    (2025, 'Chapter 11 bankruptcy filed',           'bankruptcy',  'March 5, 2025 — $19.6M debt; 77 locations closed pre-filing; blames inflation/labor'),
    (2025, 'Pappas Restaurants acquires OTB',       'acquisition', 'May 2025 — Houston-based Pappas wins auction; ~55 surviving locations; brand continues'),
]

c.executemany("""
INSERT INTO key_events (year, event_label, event_type, event_detail)
VALUES (?, ?, ?, ?)
""", events)

# ─────────────────────────────────────────────
# TABLE 4: bryce_employment
# ─────────────────────────────────────────────
c.execute("""
CREATE TABLE bryce_employment (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    location    TEXT,
    city        TEXT,
    state       TEXT,
    start_year  INTEGER,
    start_month INTEGER,
    end_year    INTEGER,
    end_month   INTEGER,
    role        TEXT,
    notes       TEXT
)
""")

c.execute("""
INSERT INTO bryce_employment
    (location, city, state, start_year, start_month, end_year, end_month, role, notes)
VALUES (
    'On The Border Alpharetta',
    'Alpharetta', 'GA',
    2014, 1, 2016, 1,
    '1st Assistant Manager',
    'Location subsequently closed. Argonne Capital had just acquired the brand. Chronic FOH understaffing, $3 meltdown rita promotions, tortilla station rarely staffed. High suburban competition from fast casual.'
)
""")

conn.commit()
conn.close()
print("✅ OTB database built:", DB_PATH)
