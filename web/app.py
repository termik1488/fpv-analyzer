from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, FileResponse
import sqlite3
from normalizer.osd_normalizer import normalize_osd_name

app = FastAPI()

@app.get("/export")
def export_report(
    date_from: str = "",
    date_to: str = ""
):

    from export.export_excel import export_to_excel

    file_path = export_to_excel(
        date_from=date_from,
        date_to=date_to
    )

    import os

    return FileResponse(
        file_path,
        filename=os.path.basename(file_path)
    )

@app.get("/", response_class=HTMLResponse)
def dashboard(
    search: str = "",
    date_from: str = "",
    date_to: str = ""
):

    conn = sqlite3.connect("db/fpv.db")
    cursor = conn.cursor()

    # Фільтри

    where_conditions = []
    params = []

    if date_from:

        where_conditions.append("""
        date(
            substr(datetime, 7, 4) || '-' ||
            substr(datetime, 4, 2) || '-' ||
            substr(datetime, 1, 2)
        ) >= date(?)
        """)

        params.append(date_from)

    if date_to:

        where_conditions.append("""
        date(
            substr(datetime, 7, 4) || '-' ||
            substr(datetime, 4, 2) || '-' ||
            substr(datetime, 1, 2)
        ) <= date(?)
        """)

        params.append(date_to)

    if search:

        where_conditions.append(
            "osd_name LIKE ?"
        )

        params.append(
            f"%{search}%"
        )

    where_sql = ""

    if where_conditions:

        where_sql = (
            "WHERE "
            + " AND ".join(where_conditions)
        )

      # Загальна кількість

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM interceptions
        {where_sql}
        """,
        params
    )

    total = cursor.fetchone()[0]

    # Подавлено

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        status = 'suppressed'
        """,
        params
    )

    suppressed = cursor.fetchone()[0]

    # Втрата відео

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        status = 'video_loss'
        """,
        params
    )

    video_loss = cursor.fetchone()[0]

    # Ураження

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        status = 'strike'
        """,
        params
    )

    hit = cursor.fetchone()[0]

    # Унікальні платформи

    cursor.execute(
        f"""
        SELECT COUNT(DISTINCT osd_name)
        FROM interceptions
        {where_sql}
        """,
        params
    )

    platforms = cursor.fetchone()[0]

    # Невідомий статус

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        status = 'unknown'
        """,
        params
    )

    unknown = cursor.fetchone()[0]


        # TOP Platforms

    cursor.execute(
        f"""
        SELECT
            osd_name,
            COUNT(*) as cnt
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        osd_name IS NOT NULL
        GROUP BY osd_name
        ORDER BY cnt DESC
        LIMIT 10
        """,
        params
    )

    top_platforms = cursor.fetchall()

    platform_rows = ""

    for name, count in top_platforms:

        platform_rows += f"""
        <tr>
            <td>{name}</td>
            <td>{count}</td>
        </tr>
        """
    

               # Video Bands

    band_counter = {
        "1.2 GHz": 0,
        "3.3 GHz": 0,
        "5.8 GHz": 0,
        "6-7.2 GHz": 0
    }

    cursor.execute(
        f"""
        SELECT video_freq
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        video_freq IS NOT NULL
        """,
        params
    )

    for (freq,) in cursor.fetchall():

        if 900 <= freq < 2000:
            band_counter["1.2 GHz"] += 1

        elif 2900 <= freq < 4200:
            band_counter["3.3 GHz"] += 1

        elif 4200 <= freq < 6000:
            band_counter["5.8 GHz"] += 1

        elif 6000 <= freq <= 7200:
            band_counter["6-7.2 GHz"] += 1

    video_12 = band_counter["1.2 GHz"]
    video_33 = band_counter["3.3 GHz"]
    video_58 = band_counter["5.8 GHz"]
    video_72 = band_counter["6-7.2 GHz"]

    total_video = (
        video_12 +
        video_33 +
        video_58 +
        video_72
    )

    if total_video > 0:

        p12 = round(video_12 * 100 / total_video, 1)
        p33 = round(video_33 * 100 / total_video, 1)
        p58 = round(video_58 * 100 / total_video, 1)
        p72 = round(video_72 * 100 / total_video, 1)

    else:

        p12 = 0
        p33 = 0
        p58 = 0
        p72 = 0

    # Control Bands

    control_bands = {
        "300-500": 0,
        "500-700": 0,
        "700-1000": 0,
        "1000-1500": 0,
        "1500-2000": 0,
        "2000-2400": 0,
        "2400-2700": 0
    }

    cursor.execute(
        f"""
        SELECT control_freq
        FROM interceptions
        {where_sql}
        {"AND" if where_sql else "WHERE"}
        control_freq IS NOT NULL
        """,
        params
    )

    for (freq,) in cursor.fetchall():

        if freq is None:
            continue

        if 300 <= freq < 500:
            control_bands["300-500"] += 1

        elif 500 <= freq < 700:
            control_bands["500-700"] += 1

        elif 700 <= freq < 1000:
            control_bands["700-1000"] += 1

        elif 1000 <= freq < 1500:
            control_bands["1000-1500"] += 1

        elif 1500 <= freq < 2000:
            control_bands["1500-2000"] += 1

        elif 2000 <= freq < 2400:
            control_bands["2000-2400"] += 1

        elif 2400 <= freq <= 2700:
            control_bands["2400-2700"] += 1

    control_300_500 = control_bands["300-500"]
    control_500_700 = control_bands["500-700"]
    control_700_1000 = control_bands["700-1000"]
    control_1000_1500 = control_bands["1000-1500"]
    control_1500_2000 = control_bands["1500-2000"]
    control_2000_2400 = control_bands["2000-2400"]
    control_2400_2700 = control_bands["2400-2700"]

# Останні 50 записів

    cursor.execute(
        f"""
        SELECT
            datetime,
            osd_name,
            video_freq,
            control_freq,
            status
        FROM interceptions
        {where_sql}
        ORDER BY datetime DESC
        LIMIT 50
        """,
        params
    )

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
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>
            <meta http-equiv="refresh" content="60">
        </head>

        <body class="container mt-4">

            <h1>🚀 FPV Analyzer Dashboard</h1>

            <hr>

            <h2>📊 Statistics</h2>

            <div class="row mb-4">

            <div class="col">
            <div class="card text-bg-primary text-center">
            <div class="card-body">
            <h3>{total}</h3>
            <p>Total</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-bg-success text-center">
            <div class="card-body">
            <h3>{suppressed}</h3>
            <p>Suppressed</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-bg-warning text-center">
            <div class="card-body">
            <h3>{video_loss}</h3>
            <p>Video Loss</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-bg-danger text-center">
            <div class="card-body">
            <h3>{hit}</h3>
            <p>Hit</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-bg-info text-center">
            <div class="card-body">
            <h3>{platforms}</h3>
            <p>Platforms</p>
            </div>
            </div>
            </div>

            <div class="col">
            <div class="card text-bg-secondary text-center">
            <div class="card-body">
            <h3>{unknown}</h3>
            <p>Unknown</p>
            </div>
            </div>
            </div>

            </div>

            <div class="row">

            <div class="col-md-6">

            <h2>📈 Status Distribution</h2>

            <div style="height:350px;">
                <canvas id="statusChart"></canvas>
            </div>

            <hr>

            <h2>🏆 Top Platforms</h2>

            <table class="table table-striped table-hover">
            <tr>
            <th>Platform</th>
            <th>Count</th>
            </tr>

            {platform_rows}

            </table>

            </div>

            <div class="col-md-6">

            <h2>📡 Video Bands</h2>

            <canvas id="videoChart"></canvas>

            <hr>

            <h3>🎮 Control Bands</h3>

            <canvas id="controlChart"></canvas>
            </div>

            </div>

            <a
            href="/export?date_from={date_from}&date_to={date_to}"
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

                    <div class="row">

                        <div class="col">
                            <input
                                class="form-control"
                                type="date"
                                name="date_from"
                                value="{date_from}">
                        </div>

                        <div class="col">
                            <input
                                class="form-control"
                                type="date"
                                name="date_to"
                                value="{date_to}">
                        </div>

                        <div class="col">
                            <input
                                class="form-control"
                                type="text"
                                name="search"
                                value="{search}"
                                placeholder="Пошук платформи">
                        </div>

                        <div class="col-auto">
                            <button
                                class="btn btn-primary"
                                type="submit">
                                Показати
                            </button>
                        </div>

                    </div>

                </form>

            <script>
            Chart.register(ChartDataLabels);
            new Chart(
                document.getElementById('statusChart'),
                {{
                    type: 'doughnut',

                    data: {{
                        labels: [
                            'Suppressed',
                            'Video Loss',
                            'Hit',
                            'Unknown'
                        ],

                        datasets: [{{
                            data: [
                                {suppressed},
                                {video_loss},
                                {hit},
                                {unknown}
                            ]
                        }}]
                    }},

                    options: {{
                        plugins: {{
                            datalabels: {{
                                color: 'white',
                                font: {{
                                    weight: 'bold',
                                    size: 14
                                }},
                                formatter: function(value) {{
                                    return value;
                                }}
                            }}
                        }}
                    }}
                }}
            );

            new Chart(
                document.getElementById('videoChart'),
                {{
                    type: 'pie',

                    data: {{
                        labels: [
                            '1.2 GHz ({p12}%)',
                            '3.3 GHz ({p33}%)',
                            '5.8 GHz ({p58}%)',
                            '6-7.2 GHz ({p72}%)'
                        ],

                        datasets: [{{
                            data: [
                                {video_12},
                                {video_33},
                                {video_58},
                                {video_72}
                            ]
                        }}]
                    }},

                    options: {{
                        plugins: {{
                            datalabels: {{
                                color: 'white',
                                font: {{
                                    weight: 'bold',
                                    size: 14
                                }},
                                formatter: function(value, ctx) {{

                                    let total =
                                        ctx.chart.data.datasets[0].data
                                        .reduce((a, b) => a + b, 0);

                                    let percent =
                                        Math.round(value * 100 / total);

                                    return percent + '%';
                                }}
                            }}
                        }}
                    }}
                }}
            );


            new Chart(
                document.getElementById('controlChart'),
                {{
                    type: 'bar',

                    data: {{
                        labels: [
                            '300-500',
                            '500-700',
                            '700-1000',
                            '1000-1500',
                            '1500-2000',
                            '2000-2400',
                            '2400-2700'
                        ],

                        datasets: [{{
                            label: 'Control Links',

                            data: [
                                {control_300_500},
                                {control_500_700},
                                {control_700_1000},
                                {control_1000_1500},
                                {control_1500_2000},
                                {control_2000_2400},
                                {control_2400_2700}
                            ]
                        }}]
                    }},

                    options: {{
                        indexAxis: 'y'
                    }}
                }}
            );                       
            
            </script>

        </body>

        </html>
        """