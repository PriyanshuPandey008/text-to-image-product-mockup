
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "product_candidates" / "candidate_images.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed"
    / "product_candidates" / "candidate_review.csv"
)

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"{OUTPUT_FILE} already exists. "
            "Rename it before creating a new review file."
        )

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as source:
        reader = csv.DictReader(source)
        rows = list(reader)
        original_fields = reader.fieldnames or []

    if not rows:
        raise ValueError("Candidate CSV contains no records.")

    fields = original_fields + [
        "decision",
        "review_notes",
    ]

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8-sig"
    ) as destination:
        writer = csv.DictWriter(destination, fieldnames=fields)
        writer.writeheader()

        for row in rows:
            row["decision"] = ""
            row["review_notes"] = ""
            writer.writerow(row)

    print(f"Candidates prepared for review: {len(rows)}")
    print(f"Review file: {OUTPUT_FILE}")
    print("Use decision values: keep, reject, or review.")

if __name__ == "__main__":
    main()
