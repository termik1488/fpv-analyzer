import sqlite3
import pandas as pd
from pathlib import Path


def export_csv(db_path="db/fpv.db",
               csv_path="data/interceptions.csv"):

    Path("data").mkdir(exist_ok=True)

    conn = sqlite3.connect(db_path)

    df = pd.read_sql_query(
        "SELECT * FROM interceptions ORDER BY datetime DESC",
        conn
    )

    df.to_csv(
        "db/csv/fpv_database.csv",
        index=False,
        encoding="utf-8-sig"
    )

    conn.close()

    print(
        "[OK] CSV exported: db/csv/fpv_database.csv"
    )