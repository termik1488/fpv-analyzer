import sqlite3
from collections import Counter


DB_PATH = "db/fpv.db"


def show_top_crews():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT osd_name
        FROM interceptions
        """
    )

    rows = cursor.fetchall()

    conn.close()

    crews = []

    for row in rows:

        if row[0]:

            crews.append(
                row[0]
            )

    counter = Counter(
        crews
    )

    print()

    print("=" * 40)

    print("TOP CREWS")

    print("=" * 40)

    for name, count in counter.most_common(20):

        print(
            f"{name:<20} {count}"
        )


if __name__ == "__main__":

    show_top_crews()