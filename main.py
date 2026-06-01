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

from export.export_csv import (
    export_csv
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
            print(
                parsed["datetime"],
                parsed["osd_name"],
                parsed["video_freq"],
                parsed["control_freq"]
)
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

    export_csv()

    print("\n1. Daily Report")
    print("2. Full Database Report")

    choice = input("\nChoose option: ")

    if choice == "1":

        report_date = input(
            "Enter date (YYYY-MM-DD): "
        )

        export_to_excel(
            report_date=report_date
        )

    elif choice == "2":

        export_to_excel()

    else:

        print("Invalid option")


if __name__ == "__main__":

    main()