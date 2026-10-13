
import json
import random
import shutil
import csv
from pathlib import Path
from collections import Counter

# Original COCO dataset
DATASET_ROOT = Path(
    r"C:\Users\HP\Downloads\archive (3)\coco_data"
)

# Output subset inside your project
OUTPUT_ROOT = Path("data/processed/coco_subset")

TRAIN_COUNT = 1000
VAL_COUNT = 100
RANDOM_SEED = 42


def load_annotations(split):
    annotation_path = (
        DATASET_ROOT / "annotations" / f"captions_{split}.json"
    )

    with annotation_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    images = data["images"]
    annotations = data["annotations"]

    captions_by_image = {}
    for annotation in annotations:
        image_id = annotation["image_id"]
        caption = annotation.get("caption", "").strip()

        if caption:
            captions_by_image.setdefault(image_id, []).append(caption)

    return images, captions_by_image


def prepare_split(split, requested_count, rng):
    images, captions_by_image = load_annotations(split)

    # Keep only image records with at least one caption and an existing file.
    image_dir = DATASET_ROOT / "images" / split
    eligible = [
        image for image in images
        if captions_by_image.get(image["id"])
        and (image_dir / image["file_name"]).is_file()
    ]

    if requested_count > len(eligible):
        raise ValueError(
            f"Requested {requested_count}, but only "
            f"{len(eligible)} eligible images exist in {split}."
        )

    selected = rng.sample(eligible, requested_count)

    output_images = OUTPUT_ROOT / "images" / split
    output_images.mkdir(parents=True, exist_ok=True)

    selected_image_records = []
    selected_annotations = []
    manifest_rows = []

    for image in selected:
        image_id = image["id"]
        filename = image["file_name"]
        captions = captions_by_image[image_id]

        source = image_dir / filename
        destination = output_images / filename

        shutil.copy2(source, destination)

        selected_image_records.append(image)

        for caption in captions:
            selected_annotations.append({
                "image_id": image_id,
                "caption": caption
            })

        manifest_rows.append({
            "split": split,
            "image_id": image_id,
            "file_name": filename,
            "caption_count": len(captions),
            "captions": captions
        })

    return {
        "images": selected_image_records,
        "annotations": selected_annotations
    }, manifest_rows


def main():
    if not DATASET_ROOT.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_ROOT}"
        )

    if OUTPUT_ROOT.exists() and any(OUTPUT_ROOT.iterdir()):
        raise FileExistsError(
            f"{OUTPUT_ROOT} is not empty. "
            "Choose a new output folder or inspect the existing subset "
            "before running again."
        )

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    rng = random.Random(RANDOM_SEED)

    all_manifest_rows = []
    split_summary = {}

    for split, count in [
        ("train2017", TRAIN_COUNT),
        ("val2017", VAL_COUNT)
    ]:
        print(f"\nPreparing {split}: {count} images")

        coco_data, rows = prepare_split(split, count, rng)
        all_manifest_rows.extend(rows)

        output_json = OUTPUT_ROOT / f"captions_{split}.json"
        with output_json.open("w", encoding="utf-8") as f:
            json.dump(coco_data, f, ensure_ascii=False, indent=2)

        split_summary[split] = {
            "images": len(coco_data["images"]),
            "caption_annotations": len(coco_data["annotations"])
        }

        print("Images copied:", len(coco_data["images"]))
        print("Caption annotations:", len(coco_data["annotations"]))

    manifest_path = OUTPUT_ROOT / "manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "split", "image_id", "file_name",
                "caption_count", "captions"
            ]
        )
        writer.writeheader()

        for row in all_manifest_rows:
            writer.writerow({
                **row,
                "captions": json.dumps(row["captions"], ensure_ascii=False)
            })

    report = {
        "dataset": "COCO Captions",
        "random_seed": RANDOM_SEED,
        "requested_subset": {
            "train_images": TRAIN_COUNT,
            "validation_images": VAL_COUNT
        },
        "splits": split_summary,
        "total_images": sum(
            item["images"] for item in split_summary.values()
        ),
        "total_caption_annotations": sum(
            item["caption_annotations"]
            for item in split_summary.values()
        ),
        "note": (
            "Initial random subset. Product relevance and image quality "
            "must be assessed before fine-tuning."
        )
    }

    report_path = OUTPUT_ROOT / "data_report.json"
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\nSubset preparation complete.")
    print(json.dumps(report, indent=2))
    print("Output folder:", OUTPUT_ROOT.resolve())


if __name__ == "__main__":
    main()
