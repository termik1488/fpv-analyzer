from PIL import Image

image = Image.open(
    r"data/raw/IMG-20260528-WA0053.jpg"
)

width, height = image.size

print(
    f"Width={width} Height={height}"
)

# 9 секторів

parts = [

    ("top_left",
     (0, 0,
      width//3,
      height//3)),

    ("top_center",
     (width//3, 0,
      2*width//3,
      height//3)),

    ("top_right",
     (2*width//3, 0,
      width,
      height//3)),

    ("mid_left",
     (0,
      height//3,
      width//3,
      2*height//3)),

    ("mid_center",
     (width//3,
      height//3,
      2*width//3,
      2*height//3)),

    ("mid_right",
     (2*width//3,
      height//3,
      width,
      2*height//3)),

    ("bottom_left",
     (0,
      2*height//3,
      width//3,
      height)),

    ("bottom_center",
     (width//3,
      2*height//3,
      2*width//3,
      height)),

    ("bottom_right",
     (2*width//3,
      2*height//3,
      width,
      height))
]

for name, box in parts:

    crop = image.crop(box)

    crop.save(
        f"debug_{name}.png"
    )

print("Done")