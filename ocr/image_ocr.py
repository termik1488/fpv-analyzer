import numbers
import os
import re

from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

import pytesseract


# TESSERACT PATH

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def preprocess_image(image):

    # Збільшуємо зображення

    image = image.resize(
        (
            image.width * 4,
            image.height * 4
        )
    )

    # Чорно-білий режим

    image = image.convert("L")

    # Контраст

    enhancer = ImageEnhance.Contrast(
        image
    )

    image = enhancer.enhance(5)

    # Threshold

    image = image.point(
        lambda p: 255 if p > 160 else 0
    )

    # Різкість

    image = image.filter(
        ImageFilter.SHARPEN
    )

    return image


def extract_distance_from_image(image_path):

    if not os.path.exists(image_path):

        print(
            f"OCR ERROR: file not found -> {image_path}"
        )

        return None

    image = Image.open(image_path)

    width, height = image.size

    # Широкий центральний crop

    image = image.crop((
        int(width * 0.30),
        int(height * 0.25),
        int(width * 0.75),
        int(height * 0.55)
    ))

    image = preprocess_image(image)

    # Для відладки

    image.save(
        "debug_processed.png"
    )

    custom_config = (
        r'--oem 3 --psm 6 '
        r'-c tessedit_char_whitelist='
        r'0123456789.KMkm'
    )

    text = pytesseract.image_to_string(
        image,
        lang="eng",
        config=custom_config
    )

    print("\n=== OCR TEXT ===\n")

    print(text)

    print(
        "RAW OCR:",
        repr(text)
    )

    # Шукаємо всі десяткові числа

    matches = re.findall(
        r"\d+(?:\.\d+)?",
        text
    )

    if not matches:

        return None

    numbers = []

    for match in matches:

        try:

            match = match.replace(",", ".")

            value = float(match)

            if value < 2:
                continue

            if value > 35:
                continue

            numbers.append(
                value
            )

        except:

            pass


    if not numbers:

        return None

    decimal_numbers = [
        n for n in numbers
        if not n.is_integer()
    ]

    if decimal_numbers:
        distance = max(decimal_numbers)
    else:
        distance = max(numbers)

    print(
        "FOUND:",
        numbers
    )

    return round(
        distance,
        2
    )
if __name__ == "__main__":

    images_dir = r"C:\Users\Admin\fpv_analyzer\data\raw"

    success = 0
    failed = 0

    for filename in os.listdir(images_dir):

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        image_path = os.path.join(
            images_dir,
            filename
        )

        distance = extract_distance_from_image(
            image_path
        )

        if distance is None:

            failed += 1

            print(
                "FAILED FILE:",
                filename
          )

        else:

            success += 1

        print(
            f"{filename} -> {distance}"
        )

    print("\n================")
    print("SUCCESS:", success)
    print("FAILED :", failed)
    print("TOTAL  :", success + failed)