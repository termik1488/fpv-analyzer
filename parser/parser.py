import re

from analyzer.analyzer import (
    calculate_launch_distance
)

from ocr.image_ocr import (
    extract_distance_from_image
)

from normalizer.osd_normalizer import (
    normalize_osd_name
)


def parse_message(text):

    data = {

        "datetime": None,

        "osd_name": None,

        "flight_distance_km": None,

        "video_freq": None,

        "control_freq": None,

        "control_bandwidth": None,

        "protocol": None,

        "lora_rate": None,

        "spreading_factor": None,

        "battery_start": None,

        "battery_end": None,

        "status": None,

        "estimated_launch_distance_m": None
    }

    # -------------------------
    # DATETIME
    # -------------------------

    datetime_match = re.search(
        r"Дата:\s*(\d{2}/\d{2}/\d{4})\s*(\d{2}:\d{2})",
        text
    )

    if datetime_match:

        date = datetime_match.group(1)

        time = datetime_match.group(2)

        data["datetime"] = (
            f"{date} {time}"
        )

# Якщо поля "Дата:" немає —
# беремо дату з WhatsApp

    if data["datetime"] is None:

        whatsapp_match = re.search(
            r"(\d{2})\.(\d{2})\.(\d{2}),\s*(\d{2}:\d{2})",
            text
        )

        if whatsapp_match:

            day = whatsapp_match.group(1)
            month = whatsapp_match.group(2)
            year = whatsapp_match.group(3)
            time = whatsapp_match.group(4)

            data["datetime"] = (
                f"{day}/{month}/20{year} {time}"
            )

    # -------------------------
    # OSD NAME
    # -------------------------

    name_match = re.search(
        r"Назва:\s*(.+)",
        text
    )

    if name_match:

        data["osd_name"] = (
            normalize_osd_name(
                name_match.group(1).strip()
            )
        )
    

    # -------------------------
    # VIDEO FREQ
    # -------------------------

    video_match = re.search(
        r"відео:\s*(\d+)",
        text,
        re.IGNORECASE
    )

    if video_match:

        data["video_freq"] = int(
            video_match.group(1)
        )

    # -------------------------
    # CONTROL
    # -------------------------

    control_match = re.search(
        r"Управа:\s*(\d+)[\\/](\d+)",
        text
    )

    if control_match:

        data["control_freq"] = int(
            control_match.group(1)
        )

        data["control_bandwidth"] = int(
            control_match.group(2)
        )

    # -------------------------
    # LORA
    # -------------------------

    lora_match = re.search(
        r"lora[_ ]?(\d+)",
        text,
        re.IGNORECASE
    )

    if lora_match:

        data["protocol"] = "LoRa"

        data["lora_rate"] = int(
            lora_match.group(1)
        )

    # -------------------------
    # SF
    # -------------------------

    sf_match = re.search(
        r"sf[_ ]?(\d+)",
        text,
        re.IGNORECASE
    )

    if sf_match:

        data["spreading_factor"] = int(
            sf_match.group(1)
        )

    # -------------------------
    # BATTERY
    # -------------------------

    battery_match = re.search(
        r"батка:\s*(\d+).*?(\d+)",
        text,
        re.IGNORECASE
    )

    if battery_match:

        data["battery_start"] = int(
            battery_match.group(1)
        )

        data["battery_end"] = int(
            battery_match.group(2)
        )

    # -------------------------
    # STATUS
    # -------------------------

    lower_text = text.lower()

    if (
        "подавлено" in lower_text
        or "подавився" in lower_text
    ):
        data["status"] = "suppressed"

    elif (
        "ураження" in lower_text
        or "зайшов на ураження" in lower_text
    ):
        data["status"] = "strike"

    elif (
        "втрата відео" in lower_text
        or "відео втрачено" in lower_text
    ):
        data["status"] = "video_loss"

    # -------------------------
    # IMAGE OCR
    # -------------------------

    image_match = re.search(
        r"(IMG-\d+-WA\d+\.(jpg|png))",
        text,
        re.IGNORECASE
    )

    if image_match:

        image_file = image_match.group(1)

        image_path = (
            f"data/raw/{image_file}"
        )

        try:

            ocr_distance = (
                extract_distance_from_image(
                    image_path
                )
            )

            if ocr_distance:

                data[
                    "flight_distance_km"
                ] = ocr_distance

                print(
                    f"OCR DISTANCE: "
                    f"{ocr_distance} km"
                )

        except Exception as e:

            print(
                f"OCR ERROR: {e}"
            )

    # -------------------------
    # LAUNCH ESTIMATION
    # -------------------------

    if (
        data["battery_start"]
        and
        data["battery_end"]
        and
        data["flight_distance_km"]
    ):

        data[
            "estimated_launch_distance_m"
        ] = (
            calculate_launch_distance(
                data["battery_start"],
                data["battery_end"],
                data["flight_distance_km"]
            )
        )

    if data["status"] is None:
        data["status"] = "unknown"

    return data