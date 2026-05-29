import sqlite3


DB_PATH = "db/fpv.db"


def show_top_distances():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            osd_name,
            flight_distance_km
        FROM interceptions
        WHERE flight_distance_km IS NOT NULL
        ORDER BY flight_distance_km DESC
        LIMIT 30
        """
    )

    rows = cursor.fetchall()

    conn.close()

    print()

    print("=" * 50)
    print("TOP DISTANCES")
    print("=" * 50)

    for osd_name, distance in rows:

        print(
            f"{distance:>6.2f} km   {osd_name}"
        )


if __name__ == "__main__":

    show_top_distances()