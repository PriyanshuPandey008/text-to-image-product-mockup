
import json
from pathlib import Path

DATASET_ROOT = Path(
    r"C:\Users\HP\Downloads\archive (3)\coco_data"
)

SPLITS = ["train2017", "val2017"]


def main():
    total_images = 0
    total_matched = 0
    total_missing = 0

    for split in SPLITS:
        annotation_file = (
            DATASET_ROOT / "annotations" / f"captions_{split}.json"
        )
        image_dir = DATASET_ROOT / "images" / split

        print(f"\nChecking {split}...")

        if not annotation_file.exists():
            print(f"Missing annotation file: {annotation_file}")
            continue

        if not image_dir.exists():
            print(f"Missing image directory: {image_dir}")
            continue

        with annotation_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        image_records = data.get("images", [])
        matched = 0
        missing = []

        for record in image_records:
            filename = record.get("file_name")

            if filename and (image_dir / filename).is_file():
                matched += 1
            else:
                missing.append(filename or "<missing filename>")

        total_images += len(image_records)
        total_matched += matched
        total_missing += len(missing)

        print("Image records:", len(image_records))
        print("Files found:", matched)
        print("Files missing:", len(missing))

        if missing:
            print("First missing examples:", missing[:5])

    print("\n" + "=" * 40)
    print("IMAGE MATCHING SUMMARY")
    print("=" * 40)
    print("Total image records:", total_images)
    print("Matched:", total_matched)
    print("Missing:", total_missing)

    if total_images and total_missing == 0:
        print("SUCCESS: All checked image records have files.")
    elif total_missing:
        print("WARNING: Investigate missing files before subset creation.")


if __name__ == "__main__":
    main()
