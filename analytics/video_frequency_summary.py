import sqlite3
from collections import Counter

DB_PATH = "db/fpv.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
SELECT video_freq
FROM interceptions
WHERE video_freq IS NOT NULL
""")

rows = cursor.fetchall()

conn.close()

frequencies = []

for row in rows:

    freq = row[0]

    if freq:
        frequencies.append(freq)

counter = Counter(frequencies)

print()
print("=" * 50)
print("VIDEO FREQUENCY SUMMARY")
print("=" * 50)

for freq, count in counter.most_common():

    if count < 2:
        continue

    print(
        f"{freq:<10} {count}"
    )