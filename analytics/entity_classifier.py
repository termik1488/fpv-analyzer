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


def get_entity_type(name):

    if not name:

        return "unknown"

    if name in KNOWN_PLATFORMS:

        return "platform"

    return "crew"