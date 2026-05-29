import os

from ocr.image_ocr import (
    extract_distance_from_image
)


RAW_FOLDER = "data/raw"


def main():

    found = 0

    total = 0

    results = []

    for file_name in os.listdir(
        RAW_FOLDER
    ):

        if not (
            file_name.lower().endswith(".jpg")
            or
            file_name.lower().endswith(".png")
        ):

            continue

        total += 1

        image_path = os.path.join(
            RAW_FOLDER,
            file_name
        )

        print(
            f"\nProcessing: {file_name}"
        )

        try:

            distance = (
                extract_distance_from_image(
                    image_path
                )
            )

            print(
                f"Distance: {distance}"
            )

            if distance:

                found += 1

            results.append(
                (
                    file_name,
                    distance
                )
            )

        except Exception as e:

            print(
                f"ERROR: {e}"
            )

    print("\n=== OCR SUMMARY ===\n")

    print(f"Total images: {total}")

    print(f"Detected distances: {found}")

    if total > 0:

        success_rate = (
            found / total
        ) * 100

        print(
            f"Success rate: "
            f"{success_rate:.1f}%"
        )

    print("\n=== RESULTS ===\n")

    for file_name, distance in results:

        print(
            f"{file_name} -> {distance}"
        )


if __name__ == "__main__":

    main()