# COCO Dataset Preparation Report

## Project

Text-to-Image Product Mockup Tool

## Objective

Inspect and prepare a reproducible subset of the COCO Captions dataset for initial experiments in text-to-image generation.

## Dataset Audit

- Training images: 118,287
- Validation images: 5,000
- Training caption annotations: 591,753
- Validation caption annotations: 25,014
- Missing image files detected: 0

## Prepared Subset

- Training images: 1,000
- Validation images: 100
- Training caption annotations: 5,006
- Validation caption annotations: 502
- Random sampling seed: 42

## Validation Checks

- Verified image-file matches against annotation records.
- Inspected image dimensions and caption lengths.
- Generated a quality report and a visual review gallery.
- Saved a manifest and dataset reports under `data/processed/coco_subset/`.

## Current Limitations

The initial subset was randomly sampled. It contains diverse scenes and is not yet a curated product-mockup dataset. Keyword matches are preliminary candidates, not proof that an image is suitable for product mockup generation.

## Next Steps

1. Identify product-relevant images using caption-based filtering.
2. Visually review candidate images and document selection criteria.
3. Establish a baseline text-to-image generation experiment.
4. Evaluate outputs using CLIP Score and a human-rating rubric.
5. Confirm the adaptation or fine-tuning approach with the project mentor.
