
from pathlib import Path
import json

# Replace this with the actual path to your extracted COCO folder.
DATASET_ROOT = Path(r"C:\Users\HP\Downloads\archive (3)\coco_data")


def main():
    print("COCO Captions Dataset Audit")
    print("=" * 45)

    if not DATASET_ROOT.exists():
        print(f"Dataset folder not found: {DATASET_ROOT}")
        print("Update DATASET_ROOT with your actual folder path.")
        return

    caption_files = sorted(DATASET_ROOT.rglob("captions_*.json"))

    if not caption_files:
        print("No caption JSON files found.")
        print("Please check the extracted folder structure.")
        return

    for caption_file in caption_files:
        print(f"\nFile: {caption_file}")

        with caption_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        images = data.get("images", [])
        annotations = data.get("annotations", [])

        print("Image records:", len(images))
        print("Caption annotations:", len(annotations))

        if annotations:
            print("Example caption:", annotations[0].get("caption"))

    print("\nAudit completed.")


if __name__ == "__main__":
    main()
