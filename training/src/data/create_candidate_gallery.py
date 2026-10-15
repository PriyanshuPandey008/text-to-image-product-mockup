
import csv
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[3]

CANDIDATE_CSV = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "product_candidates"
    / "candidate_images.csv"
)

COCO_ROOT = Path(
    r"C:\Users\HP\Downloads\archive (3)\coco_data"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "product_candidates"
    / "candidate_review_gallery.jpg"
)

SAMPLE_SIZE = 80
SEED = 42
COLUMNS = 4
CELL_WIDTH = 300
CELL_HEIGHT = 260
IMAGE_WIDTH = 280
IMAGE_HEIGHT = 180


def main():
    if not CANDIDATE_CSV.exists():
        raise FileNotFoundError(
            f"Candidate CSV not found: {CANDIDATE_CSV}"
        )

    if OUTPUT_PATH.exists():
        raise FileExistsError(
            f"{OUTPUT_PATH} already exists. "
            "Rename it before creating a new gallery."
        )

    with CANDIDATE_CSV.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        candidates = list(csv.DictReader(file))

    if not candidates:
        raise ValueError("No candidate records found.")

    random.seed(SEED)
    selected = random.sample(
        candidates, min(SAMPLE_SIZE, len(candidates))
    )

    rows = (len(selected) + COLUMNS - 1) // COLUMNS

    gallery = Image.new(
        "RGB",
        (COLUMNS * CELL_WIDTH, rows * CELL_HEIGHT),
        "white",
    )
    draw = ImageDraw.Draw(gallery)

    try:
        font = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()

    for index, item in enumerate(selected):
        split = item["split"]
        filename = item["file_name"]

        image_path = (
            COCO_ROOT
            / "images"
            / f"{split}2017"
            / filename
        )

        x = (index % COLUMNS) * CELL_WIDTH
        y = (index // COLUMNS) * CELL_HEIGHT

        if not image_path.exists():
            draw.text(
                (x + 10, y + 10),
                f"MISSING: {filename}",
                fill="red",
                font=font,
            )
            continue

        with Image.open(image_path) as source:
            image = source.convert("RGB")
            image.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))

        image_x = x + (CELL_WIDTH - image.width) // 2
        gallery.paste(image, (image_x, y + 5))

        keywords = item["matched_keywords"].replace("; ", ", ")
        caption_lines = [
            filename,
            f"Split: {split}",
            f"Keywords: {keywords[:90]}",
        ]

        for line_index, line in enumerate(caption_lines):
            draw.text(
                (x + 8, y + IMAGE_HEIGHT + 15 + line_index * 18),
                line,
                fill="black",
                font=font,
            )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    gallery.save(OUTPUT_PATH, quality=90)

    print(f"Candidates available: {len(candidates)}")
    print(f"Images in gallery: {len(selected)}")
    print(f"Gallery saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
