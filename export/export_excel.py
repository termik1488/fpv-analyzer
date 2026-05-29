import os
import sqlite3
from datetime import datetime
from collections import Counter

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import (
    PatternFill,
    Font,
    Border,
    Side,
    Alignment
)

DB_PATH = "db/fpv.db"


def export_to_excel():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
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
        FROM interceptions
    """)

    rows = cursor.fetchall()

    conn.close()

    wb = Workbook()

    # ==================================================
    # INTERCEPTIONS
    # ==================================================

    ws = wb.active

    ws.title = "Interceptions"

    headers = [
        "Дата/Час",
        "Назва OSD",
        "Дальність польоту (км)",
        "Частота відео",
        "Частота керування",
        "Ширина каналу",
        "Протокол",
        "LoRa Rate",
        "SF",
        "Батарея старт (%)",
        "Батарея кінець (%)",
        "Статус",
        "Дистанція виявлення (м)"
    ]

    ws.append(headers)

    header_fill = PatternFill(
        start_color="4472C4",
        end_color="4472C4",
        fill_type="solid"
    )

    for cell in ws[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = header_fill
        cell.alignment = Alignment(
            horizontal="center"
        )
        
    ws.freeze_panes = "A2"
    red_fill = PatternFill(
        start_color="FF9999",
        end_color="FF9999",
        fill_type="solid"
    )

    for row in rows:

        ws.append(row)

        launch_distance = row[12]

        current_row = ws.max_row

    if (
        launch_distance
         and
        launch_distance < 500
    ):

        for cell in ws[current_row]:

            cell.fill = red_fill

    ws.auto_filter.ref = ws.dimensions

    for sheet in wb.worksheets:

        for column_cells in sheet.columns:

            try:

                length = max(
                    len(str(cell.value))
                    if cell.value else 0
                    for cell in column_cells
                )

                sheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = min(
                    length + 3,
                    40
                )

            except:
                pass

    # ==================================================
    # TOP CREWS
    # ==================================================

    crews_sheet = wb.create_sheet(
        "Top Crews"
    )

    crews_sheet.append([
        "Name",
        "Count"
    ])

    crew_counter = Counter()

    for row in rows:

        name = row[1]

        if name:

            crew_counter[name] += 1

    for name, count in crew_counter.most_common():

        crews_sheet.append([
            name,
            count
        ])

    # ==================================================
    # VIDEO FREQUENCIES
    # ==================================================

    video_sheet = wb.create_sheet(
        "Video Frequencies"
    )

    video_sheet.append([
        "Frequency",
        "Count"
    ])

    video_counter = Counter()

    for row in rows:

        freq = row[3]

        if freq:

            video_counter[freq] += 1

    for freq, count in video_counter.most_common():

        video_sheet.append([
            freq,
            count
        ])

    # ==================================================
    # CONTROL RANGES
    # ==================================================

    control_sheet = wb.create_sheet(
        "Control Ranges"
    )

    control_sheet.append([
        "Range",
        "Count",
        "Percent",
        "Graph"
    ])

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

        freq = row[4]

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

    total = sum(
        ranges.values()
    )

    for name, count in ranges.items():

        if total > 0:

            percent = round(
                count * 100 / total,
                1
            )

        else:

            percent = 0

        bars = "█" * round(percent / 2)

        control_sheet.append([
            name,
            count,
            f"{percent}%",
            bars
        ])

    control_sheet.append([
        "TOTAL",
        total,
        "100%"
    ])

    # ==================================================
    # PLATFORM STATS
    # ==================================================

    platform_sheet = wb.create_sheet(
        "Platform Stats"
    )

    platform_sheet.append([
        "Platform",
        "Flights",
        "Avg Distance",
        "Max Distance"
    ])

    KNOWN_PLATFORMS = {
        "МОЛНІЯ",
        "SUDNY DEN",
        "VT40",
        "VT 40",
        "UT 40",
        "SIMARGL",
        "UT 40 SIMARGL",
        "MALOY VT 40"
    }

    platform_stats = {}

    for row in rows:

        name = row[1]
        distance = row[2]

        if name not in KNOWN_PLATFORMS:
            continue

        if distance is None:
            continue

        platform_stats.setdefault(
            name,
            []
        ).append(distance)

    for name, distances in sorted(
        platform_stats.items(),
        key=lambda x: len(x[1]),
        reverse=True
    ):

        platform_sheet.append([
            name,
            len(distances),
            round(
                sum(distances) / len(distances),
                2
            ),
            round(
                max(distances),
                2
            )
        ])

    # ==================================================
    # SAVE
    # ==================================================

    os.makedirs(
        "data/reports",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        f"data/reports/"
        f"interceptions_{timestamp}.xlsx"
    )

    wb.save(output_file)

    print(
        f"Excel exported: {output_file}"
    )