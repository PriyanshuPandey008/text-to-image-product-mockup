
import json
import random
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ROOT = Path("data/processed/coco_subset")
OUTPUT = ROOT / "review_gallery.jpg"
SAMPLE_SIZE = 24
SEED = 42


def main():
    rng = random.Random(SEED)
    examples = []

    for split in ("train2017", "val2017"):
        annotation_file = ROOT / f"captions_{split}.json"
        image_dir = ROOT / "images" / split

        with annotation_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        captions_by_id = {}
        for ann in data["annotations"]:
            captions_by_id.setdefault(ann["image_id"], []).append(
                ann["caption"]
            )

        for record in data["images"]:
            image_path = image_dir / record["file_name"]
            captions = captions_by_id.get(record["id"], [])

            if image_path.is_file() and captions:
                examples.append({
                    "path": image_path,
                    "filename": record["file_name"],
                    "captions": captions,
                    "split": split,
                })

    if not examples:
        raise RuntimeError("No valid image-caption examples found.")

    selected = rng.sample(examples, min(SAMPLE_SIZE, len(examples)))

    cell_w, cell_h = 300, 250
    columns = 4
    rows = (len(selected) + columns - 1) // columns

    gallery = Image.new(
        "RGB", (columns * cell_w, rows * cell_h), "white"
    )
    draw = ImageDraw.Draw(gallery)

    for i, item in enumerate(selected):
        with Image.open(item["path"]) as source:
            image = ImageOps.contain(source.convert("RGB"), (280, 165))

        x = (i % columns) * cell_w
        y = (i // columns) * cell_h

        gallery.paste(image, (x + (cell_w - image.width) // 2, y + 5))

        caption = item["captions"][0]
        if len(caption) > 65:
            caption = caption[:62] + "..."

        draw.text((x + 8, y + 175), item["filename"], fill="black")
        draw.text((x + 8, y + 193), caption, fill="black")
        draw.text((x + 8, y + 225), item["split"], fill="gray")

    gallery.save(OUTPUT, quality=90)
    print(f"Saved gallery to: {OUTPUT.resolve()}")
    print("Review the images and captions manually.")


if __name__ == "__main__":
    main()
