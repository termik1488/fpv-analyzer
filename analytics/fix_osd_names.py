import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import sqlite3

from normalizer.osd_normalizer import (
    normalize_osd_name
)

DB_PATH = "db/fpv.db"


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute(
    """
    SELECT id, osd_name
    FROM interceptions
    """
)

rows = cursor.fetchall()

updated = 0

for row in rows:

    record_id = row[0]

    old_name = row[1]

    new_name = normalize_osd_name(
        old_name
    )

    if new_name != old_name:

        cursor.execute(
            """
            UPDATE interceptions
            SET osd_name=?
            WHERE id=?
            """,
            (
                new_name,
                record_id
            )
        )

        updated += 1

conn.commit()

conn.close()

print(
    f"Updated: {updated}"
)