from whatsapp.whatsapp_reader import (
    read_whatsapp_export
)

from parser.parser import (
    parse_message
)

from database.database import (
    init_db,
    insert_interception
)

from export.export_excel import (
    export_to_excel
)


def main():

    init_db()

    messages = read_whatsapp_export(
        "data/raw/chat.txt"
    )

    print(
        f"Found messages: "
        f"{len(messages)}"
    )

    inserted = 0

    for message in messages:

        parsed = parse_message(
            message
        )

        if parsed["osd_name"]:

            insert_interception(
                parsed
            )

            inserted += 1

            print(
                f"Inserted: "
                f"{parsed['osd_name']}"
            )

    print(
        f"Inserted total: "
        f"{inserted}"
    )

    export_to_excel()


if __name__ == "__main__":

    main()