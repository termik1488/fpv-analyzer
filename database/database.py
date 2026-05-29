import sqlite3


DB_PATH = "db/fpv.db"


def init_db():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interceptions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            datetime TEXT,

            osd_name TEXT,

            flight_distance_km REAL,

            video_freq INTEGER,

            control_freq INTEGER,

            control_bandwidth INTEGER,

            protocol TEXT,

            lora_rate INTEGER,

            spreading_factor INTEGER,

            battery_start INTEGER,

            battery_end INTEGER,

            status TEXT,

            estimated_launch_distance_m INTEGER
        )
        """
    )

    conn.commit()

    conn.close()


def insert_interception(data):

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interceptions (

            datetime,

            osd_name,

            flight_distance_km,

            video_freq,

            control_freq,

            control_bandwidth,

            protocol,

            lora_rate,

            spreading_factor,

            battery_start,

            battery_end,

            status,

            estimated_launch_distance_m

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (

            data["datetime"],

            data["osd_name"],

            data["flight_distance_km"],

            data["video_freq"],

            data["control_freq"],

            data["control_bandwidth"],

            data["protocol"],

            data["lora_rate"],

            data["spreading_factor"],

            data["battery_start"],

            data["battery_end"],

            data["status"],

            data["estimated_launch_distance_m"]
        )
    )

    conn.commit()

    conn.close()


def get_all_interceptions():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM interceptions
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows