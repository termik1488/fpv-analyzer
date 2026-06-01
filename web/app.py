from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
import sqlite3

app = FastAPI()

@app.get("/export")
def export_report():

    from export.export_excel import export_to_excel

    file_path = export_to_excel()

    return FileResponse(
        file_path,
        filename="FPV_Report.xlsx"
    )


@app.get("/", response_class=HTMLResponse)
def dashboard(search: str = ""):

    conn = sqlite3.connect("db/fpv.db")
    cursor = conn.cursor()

    # Загальна кількість
    cursor.execute("""
    SELECT COUNT(*)
    FROM interceptions
    """)
    total = cursor.fetchone()[0]

    # Подавлено
    cursor.execute("""
    SELECT COUNT(*)
    FROM interceptions
    WHERE status = 'suppressed'
    """)
    suppressed = cursor.fetchone()[0]

    # Втрата відео
    cursor.execute("""
    SELECT COUNT(*)
    FROM interceptions
    WHERE status = 'video_loss'
    """)
    video_loss = cursor.fetchone()[0]

    # Ураження
    cursor.execute("""
    SELECT COUNT(*)
    FROM interceptions
    WHERE status = 'strike'
    """)
    hit = cursor.fetchone()[0]

    # Унікальні платформи
    cursor.execute("""
    SELECT COUNT(DISTINCT osd_name)
    FROM interceptions
    """)

    platforms = cursor.fetchone()[0]
   
    # Невідомий статус
    cursor.execute("""
    SELECT COUNT(*)
    FROM interceptions
    WHERE status = 'unknown'
    """)
    unknown = cursor.fetchone()[0]
    

# Останні 50 записів

    if search:

        cursor.execute("""
        SELECT
            datetime,
            osd_name,
            video_freq,
            control_freq,
            status
        FROM interceptions
        WHERE osd_name LIKE ?
        ORDER BY datetime DESC
        LIMIT 50
        """, (f"%{search}%",))

    else:

        cursor.execute("""
        SELECT
            datetime,
            osd_name,
            video_freq,
            control_freq,
            status
        FROM interceptions
        ORDER BY datetime DESC
        LIMIT 50
        """)

    rows = cursor.fetchall()

    table_rows = ""

    for row in rows:

        table_rows += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
            <td>{row[4]}</td>
        </tr>
        """

    conn.close()

    return f"""
        <html>

        <head>
            <title>FPV Analyzer</title>

            <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
            rel="stylesheet">
        </head>

        <body class="container mt-4">

            <h1>🚀 FPV Analyzer Dashboard</h1>

            <hr>

            <h2>📊 Statistics</h2>

            <div class="row mb-4">

            <div class="col">
            <div class="card text-center">
            <div class="card-body">
            <h3>{total}</h3>
            <p>Total</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-center">
            <div class="card-body">
            <h3>{suppressed}</h3>
            <p>Suppressed</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-center">
            <div class="card-body">
            <h3>{video_loss}</h3>
            <p>Video Loss</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-center">
            <div class="card-body">
            <h3>{hit}</h3>
            <p>Hit</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-center">
            <div class="card-body">
            <h3>{platforms}</h3>
            <p>Platforms</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-center">
            <div class="card-body">
            <h3>{unknown}</h3>
            <p>Unknown</p>
            </div>
            </div>
            </div>

            </div>

            <a
            href="/export"
            class="btn btn-success mb-3">

            📊 Download Excel

            </a>

            <table class="table table-striped table-hover">
            <tr>
                <th>Дата</th>
                <th>Платформа</th>
                <th>Відео</th>
                <th>Керування</th>
                <th>Статус</th>
            </tr>
            {table_rows}
            </table>
                <form method="get" class="mb-3">

                <input
                class="form-control"
                type="text"
                name="search"
                value="{search}"
                placeholder="Пошук платформи">

                </form>
        </body>

        </html>
        """