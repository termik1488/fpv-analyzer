import sqlite3

DB_PATH = "db/fpv.db"

KNOWN_PLATFORMS = {
    "МОЛНІЯ",
    "SUDNY DEN",
    "VT40",
    "VT 40",
    "UT 40",
    "SIMARGL",
    "UT 40 SIMARGL",
    "MALOY VT 40"
}

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
SELECT
    osd_name,
    flight_distance_km
FROM interceptions
WHERE flight_distance_km IS NOT NULL
""")

rows = cursor.fetchall()

conn.close()

stats = {}

for name, distance in rows:

    if name not in KNOWN_PLATFORMS:
        continue

    stats.setdefault(name, []).append(distance)

print()
print("=" * 60)
print("PLATFORM STATISTICS")
print("=" * 60)

for name, distances in sorted(
    stats.items(),
    key=lambda x: len(x[1]),
    reverse=True
):

    print()
    print(name)
    print(f"  Flights: {len(distances)}")
    print(f"  Avg: {sum(distances)/len(distances):.2f} km")
    print(f"  Max: {max(distances):.2f} km")