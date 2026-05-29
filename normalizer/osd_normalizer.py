import re


def normalize_osd_name(name):

    if not name:
        return None

    name = name.upper()

    # прибираємо сміття

    name = re.sub(
        r"[^A-ZА-ЯІЇЄ0-9 ]",
        " ",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    # FPV

    name = name.replace(
        "FPV ",
        ""
    )

    # MOLNIA

    if (
        "МОЛНІЯ" in name
        or
        "MOLNIA" in name
    ):

        return "МОЛНІЯ"

    # SUDNY DEN

    if (
        "SUDNY" in name
        or
        "UDNY" in name
    ):

        return "SUDNY DEN"

    # VT40

    if (
        "VT40" in name
        or
        "UT40" in name
    ):

        return "VT40"

    return name