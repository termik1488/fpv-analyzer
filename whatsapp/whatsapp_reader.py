import re


def read_whatsapp_export(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    messages = []

    current_message = ""

    for line in lines:

        line = line.strip()

        # NEW MESSAGE

        if re.match(
            r"^\d{2}\.\d{2}\.\d{2},",
            line
        ):

            if current_message:

                messages.append(
                    current_message
                )

            current_message = line

        else:

            current_message += (
                "\n" + line
            )

    # LAST MESSAGE

    if current_message:

        messages.append(
            current_message
        )

    return messages