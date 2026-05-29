def calculate_launch_distance(
    battery_start,
    battery_end,
    flight_distance_km
):

    try:

        used_mah = (
            battery_end - battery_start
        )

        if used_mah <= 0:

            return None

        flight_distance_m = (
            flight_distance_km * 1000
        )

        mah_per_meter = (
            used_mah / flight_distance_m
        )

        estimated_distance = (
            battery_start / mah_per_meter
        )

        return round(
            estimated_distance
        )

    except:

        return None