import sqlite3
from collections import Counter

DB_PATH = "db/fpv.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
SELECT
    video_freq,
    osd_name
FROM interceptions
WHERE
    video_freq IS NOT NULL
    AND osd_name IS NOT NULL
""")

rows = cursor.fetchall()

conn.close()

channels = {}

for video_freq, osd_name in rows:

    if video_freq not in channels:
        channels[video_freq] = []

    channels[video_freq].append(
        osd_name
    )

for freq in sorted(channels):

    print()
    print("=" * 50)
    print(f"VIDEO {freq} MHz")
    print("=" * 50)

    counter = Counter(
        channels[freq]
    )

    for name, count in counter.most_common():

        print(
            f"{name:<20} {count}"
        )