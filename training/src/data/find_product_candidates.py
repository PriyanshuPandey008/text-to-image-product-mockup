
import csv
import json
from pathlib import Path

# Project root: Text_to_Image_ProductMockup/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

SUBSET_DIR = PROJECT_ROOT / "data" / "processed" / "coco_subset"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "product_candidates"
OUTPUT_FILE = OUTPUT_DIR / "candidate_images.csv"

PRODUCT_KEYWORDS = {
    "packaging": [
        "bottle", "package", "packaging", "box", "container",
        "carton", "can", "jar", "plastic bag", "wrapper",
    ],
    "electronics": [
        "phone", "cellphone", "laptop", "computer", "keyboard",
        "mouse", "camera", "television", "remote", "headphones",
        "electronic", "monitor",
    ],
    "fashion": [
        "shoe", "shoes", "handbag", "backpack", "suitcase",
        "hat", "sunglasses", "watch", "shirt", "dress", "jacket",
        "clothing", "purse",
    ],
    "home_and_kitchen": [
        "chair", "table", "lamp", "clock", "cup", "mug",
        "plate", "bowl", "fork", "spoon", "knife", "pan",
        "pot", "toaster", "microwave", "refrigerator", "blender",
        "kettle", "vase",
    ],
    "sports_and_toys": [
        "toy", "teddy bear", "racket", "skateboard",
        "sports ball", "frisbee", "baseball bat",
    ],
    "vehicles_and_other": [
        "bicycle", "motorcycle", "motorbike", "car", "truck",
        "helmet", "umbrella", "book",
    ],
    "food_and_drink": [
        "food", "snack", "cereal", "drink", "beverage",
        "coffee", "bread", "cake", "fruit", "vegetable",
    ],
}


def find_candidates(json_path, split):
    with json_path.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    captions_by_image = {}
    filenames = {
        image["id"]: image["file_name"]
        for image in dataset["images"]
    }

    for annotation in dataset["annotations"]:
        image_id = annotation["image_id"]
        caption = annotation["caption"].strip()
        captions_by_image.setdefault(image_id, []).append(caption)

    candidates = []

    for image_id, captions in captions_by_image.items():
        text = " ".join(captions).lower()
        categories = {}

        for category, keywords in PRODUCT_KEYWORDS.items():
            matches = [
                keyword for keyword in keywords
                if keyword in text
            ]
            if matches:
                categories[category] = matches

        if categories:
            candidates.append({
                "split": split,
                "image_id": image_id,
                "file_name": filenames.get(image_id, ""),
                "categories": "; ".join(categories.keys()),
                "matched_keywords": "; ".join(
                    keyword
                    for matches in categories.values()
                    for keyword in matches
                ),
                "captions": " | ".join(captions),
            })

    return candidates


def main():
    train_json = SUBSET_DIR / "captions_train2017.json"
    val_json = SUBSET_DIR / "captions_val2017.json"

    for path in (train_json, val_json):
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")

    output_path = OUTPUT_FILE

    # Avoid overwriting an existing report.
    if output_path.exists():
        raise FileExistsError(
            f"{output_path} already exists. Review or rename it first."
        )

    rows = []
    rows.extend(find_candidates(train_json, "train"))
    rows.extend(find_candidates(val_json, "val"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fields = [
        "split", "image_id", "file_name",
        "categories", "matched_keywords", "captions",
    ]

    with output_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    train_count = sum(row["split"] == "train" for row in rows)
    val_count = sum(row["split"] == "val" for row in rows)

    print(f"Training candidates: {train_count}")
    print(f"Validation candidates: {val_count}")
    print(f"Total candidates: {len(rows)}")
    print(f"Saved report: {output_path}")
    print("These are keyword candidates, not yet visually approved.")


if __name__ == "__main__":
    main()
