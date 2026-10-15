# 🎨 Text-to-Image Product Mockup Generator

### Turning natural-language ideas into visual product concepts with Generative AI

A multimodal AI project exploring how text-to-image diffusion models can transform product descriptions into visual mockups. The project uses a pretrained Stable Diffusion pipeline as a baseline, with plans to adapt the model for product-focused generation and evaluate results using CLIP similarity and human feedback.

> **Project status:** 🚧 In development — dataset preparation and baseline evaluation completed; product-focused adaptation is the next phase.

---

## ✨ Project Vision

Imagine describing a product in a sentence and getting a visual concept in seconds.

For example:

- 🎧 *"Minimal black wireless headphones on a clean studio background."*
- 🧴 *"A premium amber perfume bottle with elegant minimalist packaging."*
- 🥤 *"A reusable stainless-steel water bottle with a modern, matte finish."*

The goal is to explore a workflow that turns these descriptions into useful visual starting points for product ideation, concept exploration, and mockup creation.

**Note:** Generated images are AI-created concepts, not guaranteed production-ready product designs.

---

## 🎯 Project Objectives

- Build a working text-to-image generation pipeline using a pretrained diffusion model.
- Prepare and investigate a manageable subset of COCO Captions data.
- Explore product-focused data selection and model adaptation using LoRA.
- Evaluate generated images using human ratings and CLIP-based text-image similarity.
- Develop a full-stack demo with a React frontend and FastAPI backend.
- Document experiments, limitations, and reproducible setup steps.

---

## 🤖 Pretrained Model

### Stable Diffusion v1.5

**Model:** [`stable-diffusion-v1-5/stable-diffusion-v1-5`](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5)

We use the pretrained **Stable Diffusion v1.5** text-to-image model as the baseline for our product mockup generation experiments. The model uses latent diffusion to generate images conditioned on natural-language prompts. It is loaded using Hugging Face Diffusers and run on a GPU-enabled Google Colab runtime.

**Baseline configuration**

| Parameter | Configuration |
|---|---|
| Model | Stable Diffusion v1.5 |
| Framework | PyTorch and Hugging Face Diffusers |
| Runtime | Google Colab |
| GPU | NVIDIA Tesla T4 |
| Image resolution | 512 × 512 pixels |
| Inference steps | 25 |
| Guidance scale | 7.5 |
| Random seeds | 42 for the initial experiment; 100–104 for the five-image gallery |
| Evaluation | Human ratings and OpenCLIP image-text cosine similarity |

The pretrained model is used for baseline inference. Product-focused LoRA fine-tuning is planned as a subsequent experiment.

**Research paper:** [High-Resolution Image Synthesis with Latent Diffusion Models — CVPR 2022](https://arxiv.org/abs/2112.10752)

**Model license:** Review the model's [license and usage conditions](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5) before using or redistributing generated outputs.

---

## 🧠 How It Works

```text
Natural-Language Prompt
          │
          ▼
Prompt Encoding
          │
          ▼
Stable Diffusion v1.5
          │
          ▼
AI-Generated Image
          │
          ▼
Evaluation
(CLIP Similarity + Human Ratings)
          │
          ▼
Future: Product-Focused Adaptation
and Interactive Web Application
```

The initial experiments establish a baseline before product-focused fine-tuning. This provides a reference point for comparing future improvements.

---

## 🛠️ Technology Stack

| Area | Technologies |
|---|---|
| Generative AI | Stable Diffusion 1.5, Latent Diffusion Models |
| Deep Learning | PyTorch, Hugging Face Diffusers |
| Evaluation | OpenCLIP, CLIP similarity, human evaluation |
| Data Processing | Python, Pillow, COCO Captions |
| Training Direction | LoRA fine-tuning |
| Planned Backend | FastAPI |
| Planned Frontend | React |
| Development | VS Code, Google Colab, Git, GitHub |

---

## 📊 Current Progress

### 1. Dataset Preparation

- Inspected the COCO Captions dataset.
- Created a reproducible subset containing 1,000 training images and 100 validation images.
- Verified image availability and generated dataset quality reports.
- Developed scripts to identify potential product-related image candidates.
- Generated visual review galleries and candidate metadata.

**Dataset limitation:** COCO Captions contains general everyday scenes, not a dedicated product-mockup dataset. Automatically selected candidates may include irrelevant images and require further filtering.

### 2. Stable Diffusion Baseline

- Loaded pretrained Stable Diffusion v1.5 in Google Colab using a Tesla T4 GPU.
- Generated an initial product-style image.
- Created a five-prompt experiment gallery covering headphones, perfume, watches, sports shoes, and water bottles.
- Recorded generation settings and experiment metadata.

### 3. Preliminary Evaluation

Five generated images were rated on a 1–5 human evaluation rubric.

| Evaluation dimension | Average rating |
|---|---:|
| Object recognizability | 4.6/5 |
| Prompt adherence | 2.8/5 |
| Composition | 3.6/5 |
| Visual quality | 3.8/5 |

The initial OpenCLIP evaluation produced a mean image-text cosine similarity of **0.3023** across the same five prompts and generated images.

These are preliminary exploratory results from a small sample, not statistically conclusive evidence. The similarity score is specific to the evaluation implementation and should primarily be used for comparisons under the same setup.

---

## 🖼️ Dataset Review Galleries

Visual inspection helps us understand the quality and limitations of our data before model adaptation.

- **COCO subset review gallery:** [`data/processed/coco_subset/review_gallery.jpg`](data/processed/coco_subset/review_gallery.jpg)
- **Product candidate review gallery:** [`data/processed/product_candidates/candidate_review_gallery.jpg`](data/processed/product_candidates/candidate_review_gallery.jpg)

The galleries provide visual previews of the selected images. Product candidates are automatically identified and are not all manually verified product images.

---

## 🔬 Next Steps

- [x] Inspect the COCO Captions dataset.
- [x] Prepare a manageable training and validation subset.
- [x] Build product-candidate discovery and gallery scripts.
- [x] Establish a pretrained Stable Diffusion baseline.
- [x] Run preliminary human and CLIP-based evaluations.
- [ ] Refine the product-focused dataset.
- [ ] Experiment with LoRA-based model adaptation.
- [ ] Compare baseline and adapted-model results.
- [ ] Develop the FastAPI inference backend.
- [ ] Build the React demo interface.
- [ ] Add automated tests and deployment documentation.

---

## 📁 Repository Structure

```text
text-to-image-product-mockup/
├── backend/                     # Backend application
├── data/
│   └── processed/
│       ├── coco_subset/         # Dataset metadata and reports
│       └── product_candidates/  # Candidate metadata and galleries
├── docs/
│   └── data_preparation.md
├── frontend/                    # Frontend application
├── models/                      # Model-related code and configuration
├── scripts/                     # Project utility scripts
├── tests/                       # Project-level tests
├── training/
│   ├── artifacts/               # Training artifacts
│   ├── configs/                 # Experiment configurations
│   ├── experiments/             # Experiment records
│   ├── notebooks/               # Research notebooks
│   └── src/
│       ├── data/                # Dataset preparation scripts
│       ├── evaluation/           # Evaluation code
│       ├── models/               # Model code
│       └── training/             # Training code
├── .gitignore
└── README.md
```

Some directories may remain empty while their components are under development. Large datasets, model checkpoints, virtual environments, and temporary artifacts are intentionally excluded from Git.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PriyanshuPandey008/text-to-image-product-mockup.git
cd text-to-image-product-mockup
```

### 2. Create a Python environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies required by the specific script or notebook you intend to run. A consolidated project requirements file and complete setup instructions will be added as the application develops.

### 4. Run baseline experiments

The initial baseline was executed in Google Colab with GPU acceleration. A compatible GPU runtime is recommended for image generation and model adaptation. CPU-only systems may be substantially slower.

For the pretrained model and its configuration, refer to the [Stable Diffusion v1.5 model card](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5).

---

## 📈 Evaluation Strategy

Future experiments will compare the baseline and adapted pipeline using:

- **Human evaluation:** Recognizability, prompt adherence, composition, and visual quality.
- **CLIP similarity:** Image-text alignment using a consistent evaluation implementation.
- **Qualitative comparisons:** Side-by-side image galleries generated with documented prompts and settings.

Comparisons should use consistent prompts, settings, and evaluation procedures wherever possible.

---

## ⚠️ Limitations

- COCO Captions is a general-purpose dataset and is not specifically designed for product mockups.
- Candidate discovery is keyword-based and can produce false positives.
- Baseline evaluation currently covers only five generated images.
- CLIP similarity does not fully measure aesthetics, realism, or practical design usefulness.
- Product-focused adaptation, the web application, and deployment remain future work.

---

## 📚 References

1. Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752), CVPR 2022.
2. [Stable Diffusion v1.5 — Hugging Face Model Card](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5).
3. [COCO Dataset](https://cocodataset.org/).
4. [Hugging Face Diffusers Documentation](https://huggingface.co/docs/diffusers/index).
5. [OpenCLIP](https://github.com/mlfoundations/open_clip).

---

## 👨‍💻 Author

**Priyanshu Pandey**

B.Tech Computer Science & Engineering (AI/ML)

GitHub: [@PriyanshuPandey008](https://github.com/PriyanshuPandey008)

---

*Built as an exploration of generative AI, diffusion models, and product-focused image generation.*