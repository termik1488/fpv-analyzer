import sqlite3

DB_PATH = "db/fpv.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
SELECT control_freq
FROM interceptions
WHERE control_freq IS NOT NULL
""")

rows = cursor.fetchall()

conn.close()

ranges = {
    "<300 MHz": 0,
    "300-500 MHz": 0,
    "500-700 MHz": 0,
    "700-1000 MHz": 0,
    "1000-1500 MHz": 0,
    "1500-2000 MHz": 0,
    "2000-2400 MHz": 0,
    "2400-2700 MHz": 0,
    ">2700 MHz": 0
}

for row in rows:

    freq = row[0]
    
    if freq is None:
       continue

    if freq < 300:

        ranges["<300 MHz"] += 1

    elif freq < 500:

        ranges["300-500 MHz"] += 1

    elif freq < 700:

        ranges["500-700 MHz"] += 1

    elif freq < 1000:

        ranges["700-1000 MHz"] += 1

    elif freq < 1500:

        ranges["1000-1500 MHz"] += 1

    elif freq < 2000:

        ranges["1500-2000 MHz"] += 1

    elif freq < 2400:

        ranges["2000-2400 MHz"] += 1

    elif freq <= 2700:

        ranges["2400-2700 MHz"] += 1

    else:

        ranges[">2700 MHz"] += 1

print()
print("=" * 50)
print("CONTROL FREQUENCY RANGES")
print("=" * 50)

for name, count in ranges.items():

    print(
        f"{name:<20} {count}"
    )