from database.database import (
    get_all_interceptions
)


def analyze_early_detections():

    rows = get_all_interceptions()

    print("\n=== EARLY DETECTIONS ===\n")

    early_rows = []

    for row in rows:

        battery_start = row[
            "battery_start"
        ]

        if (
            battery_start
            and battery_start < 1000
        ):

            early_rows.append(row)

    # SORT BY LOWEST BATTERY

    early_rows = sorted(
        early_rows,
        key=lambda x: x["battery_start"]
    )

    print(
        f"Found: {len(early_rows)}"
    )

    for row in early_rows[:30]:

        print(
            f"\nOSD: {row['osd_name']}"
        )

        print(
            f"Video: {row['video_freq']}"
        )

        print(
            f"Battery: "
            f"{row['battery_start']} "
            f"-> "
            f"{row['battery_end']}"
        )

        print(
            f"Estimated launch distance: "
            f"{row['estimated_launch_distance_m']} m"
        )

        print(
            f"Status: {row['status']}"
        )

        print(
            f"Date: {row['datetime']}"
        )
        