
import json
import csv
import statistics
from collections import Counter
from pathlib import Path
from PIL import Image

SUBSET_ROOT = Path("data/processed/coco_subset")

PRODUCT_KEYWORDS = {
    "product": [
        "product", "packaging", "bottle", "box", "can",
        "phone", "laptop", "headphone", "watch", "camera",
        "shoe", "bag", "chair", "table", "furniture",
        "keyboard", "mouse", "speaker", "mug", "cup",
        "cosmetic", "perfume", "soap", "toy", "appliance"
    ],
    "vehicle": [
        "car", "motorcycle", "bicycle", "truck", "bus"
    ]
}


def analyze_split(split):
    image_dir = SUBSET_ROOT / "images" / split
    annotation_file = SUBSET_ROOT / f"captions_{split}.json"

    with annotation_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    annotations_by_image = {}
    for annotation in data["annotations"]:
        annotations_by_image.setdefault(
            annotation["image_id"], []
        ).append(annotation["caption"])

    widths, heights = [], []
    image_errors = []
    caption_lengths = []
    matched_images = 0
    relevant_images = 0
    category_counts = Counter()
    examples = []

    for image_record in data["images"]:
        image_id = image_record["id"]
        filename = image_record["file_name"]
        image_path = image_dir / filename
        captions = annotations_by_image.get(image_id, [])

        if not image_path.is_file():
            image_errors.append(filename)
            continue

        try:
            with Image.open(image_path) as img:
                width, height = img.size
                img.verify()

            widths.append(width)
            heights.append(height)
            matched_images += 1
        except Exception as exc:
            image_errors.append(f"{filename}: {exc}")
            continue

        combined_caption = " ".join(captions).lower()
        caption_lengths.extend(len(c.split()) for c in captions)

        matched_categories = []
        for category, keywords in PRODUCT_KEYWORDS.items():
            if any(keyword in combined_caption for keyword in keywords):
                category_counts[category] += 1
                matched_categories.append(category)

        if matched_categories:
            relevant_images += 1

        if len(examples) < 10:
            examples.append({
                "image_id": image_id,
                "file_name": filename,
                "captions": captions,
                "width": width,
                "height": height,
                "keyword_matches": matched_categories
            })

    return {
        "split": split,
        "image_records": len(data["images"]),
        "caption_annotations": len(data["annotations"]),
        "images_verified": matched_images,
        "image_errors": image_errors,
        "mean_width": round(statistics.mean(widths), 2) if widths else None,
        "mean_height": round(statistics.mean(heights), 2) if heights else None,
        "min_width": min(widths) if widths else None,
        "min_height": min(heights) if heights else None,
        "mean_caption_words": round(statistics.mean(caption_lengths), 2) if caption_lengths else None,
        "keyword_matched_images": relevant_images,
        "keyword_match_counts": dict(category_counts),
        "sample_examples": examples
    }


def main():
    reports = [
        analyze_split("train2017"),
        analyze_split("val2017")
    ]

    output_path = SUBSET_ROOT / "quality_report.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)

    for report in reports:
        print(f"\n--- {report['split']} ---")
        print("Images verified:", report["images_verified"])
        print("Caption annotations:", report["caption_annotations"])
        print("Mean image width:", report["mean_width"])
        print("Mean image height:", report["mean_height"])
        print("Mean caption length (words):", report["mean_caption_words"])
        print("Images with product/vehicle keyword matches:",
              report["keyword_matched_images"])
        print("Keyword match counts:", report["keyword_match_counts"])
        print("Image errors:", len(report["image_errors"]))

        print("\nSample captions:")
        for example in report["sample_examples"][:3]:
            print(example["file_name"], "->", example["captions"][:2])

    print("\nSaved quality report to:", output_path)


if __name__ == "__main__":
    main()
