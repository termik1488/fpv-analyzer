from ocr.image_ocr import (
    extract_distance_from_image
)


distance = extract_distance_from_image(
    "data/raw/IMG-20260507-WA0349.jpg"
)

print(
    f"\nDistance: {distance}"
)