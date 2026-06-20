# Reproducibility Guide

> 이 문서는 프로젝트를 로컬 또는 Colab에서 재현하기 위한 환경 설정, 실행 방법, 검증 포인트, 문제 해결 방법을 정리합니다.

---

## 1. Environment Summary

| Item | Recommended |
|---|---|
| Python | 3.10 이상 권장 |
| Backend | FastAPI + Uvicorn |
| Model | CLIP ViT-B/32 |
| Deep Learning Framework | PyTorch |
| Demo Runtime | GPU 권장, CPU도 가능하나 느림 |
| Colab | T4 GPU 권장 |

> Note: Dockerfile은 `python:3.10-slim`을 사용합니다. README의 Python 3.12 권장 문구와 Docker 환경을 맞추려면 3.10+로 통일해도 충분합니다.

---

## 2. Installation

### 2.1 Clone

```bash
git clone https://github.com/chairwomans/chairwomans-capstone.git
cd chairwomans-capstone
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
pip install git+https://github.com/openai/CLIP.git
```

### 2.3 Run Server

```bash
uvicorn server:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## 3. Quick Functional Test

After installation, run a minimal check in Python.

```python
from PIL import Image
from clip_pipeline import estimate_domain

image = Image.open("your_image.png").convert("RGB")
result = estimate_domain(image, n_views=8, top_k=5)
print(result)
```

For a faster smoke test, use `n_views=8` or `n_views=16`. For the full demo setting, use `n_views=127`.

---

## 4. Expected Output Format

`estimate_domain()` returns a dictionary of top-k domain weights.

```python
{
    "sketch": 0.7065,
    "cartoon": 0.2480,
    "drawing": 0.0278,
    "photo": 0.0177,
    "graphic": 0.0100,
}
```

The exact values are not deterministic because RandomCrop creates random views.

---

## 5. Randomness and Seeds

Current code uses random crop transformations without explicitly fixing a seed. This is appropriate for interactive demo use, but exact reproduction requires seed control.

For deterministic experiments, add:

```python
import torch
import random
import numpy as np

seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
```

Also consider controlling `torch.backends.cudnn.deterministic` and `torch.backends.cudnn.benchmark` depending on the experiment.

---

## 6. Reproducing Current Domain Estimation Result

현재 보고된 핵심 실험은 PACS 기반 domain estimation입니다.

| Condition | Accuracy |
|---|---:|
| MTA 미적용 | 94.64% |
| MTA 적용 | 97.91% |

현재 저장소에는 이 결과를 한 번에 재현하는 standalone CLI script가 포함되어 있지 않습니다. 재현을 위해서는 다음 로직을 구성해야 합니다.

```text
for each image in PACS:
    1. load image
    2. infer ground-truth domain from folder name
    3. estimate domain with original only or MTA
    4. compare predicted top-1 domain with ground-truth domain
    5. accumulate total and domain-wise accuracy
```

Recommended files to reuse:

| Step | File / Function |
|---|---|
| domain prompt bank | `domain_prompts.py` |
| CLIP domain features | `clip_pipeline._build_domain_features()` |
| crop view generation | `mta.make_views()` |
| robust mode | `mta.solve_mta()` |
| top-k domain estimation | `clip_pipeline.estimate_domain()` |

---

## 7. Performance Notes

| Setting | Speed | Notes |
|---|---|---|
| `n_views=8` | Fast | smoke test용 |
| `n_views=32` | Moderate | 개발 중 디버깅용 |
| `n_views=127` | Slow but stable | 현재 demo/report setting |
| CPU | Very slow | 가능하지만 권장하지 않음 |
| GPU | Recommended | CLIP image encoding 속도 개선 |

---

## 8. Troubleshooting

### 8.1 `ModuleNotFoundError: No module named 'clip'`

Install OpenAI CLIP:

```bash
pip install git+https://github.com/openai/CLIP.git
```

### 8.2 CLIP Tokenizer Vocab Error

If the local `clip/` folder is included and `clip/bpe_simple_vocab_16e6.txt.gz` is not a real gzip file, tokenizer loading can fail.

Check the file:

```bash
file clip/bpe_simple_vocab_16e6.txt.gz
```

If it shows a Git LFS pointer instead of gzip data, use one of these approaches.

#### Option A: Use Git LFS

```bash
git lfs install
git lfs pull
```

#### Option B: Remove vendored `clip/` folder

Remove the local `clip/` folder and rely on:

```bash
pip install git+https://github.com/openai/CLIP.git
```

This avoids Python importing the broken local package first.

### 8.3 CUDA Out of Memory

Reduce number of views.

```python
estimate_domain(image, n_views=16, top_k=5)
```

### 8.4 Server Starts but Page Does Not Load

Check port and static path.

```bash
uvicorn server:app --host 0.0.0.0 --port 7860
```

Then open:

```text
http://127.0.0.1:7860
```

### 8.5 Predictions Change Across Runs

This is expected because RandomCrop is stochastic. Fix seeds for controlled experiments.

---

## 9. Suggested Future Reproducibility Improvements

| Improvement | Benefit |
|---|---|
| Add `scripts/evaluate_pacs.py` | PACS result 재현 가능 |
| Add `configs/default.yaml` | view count, temperature, lambda 값 관리 |
| Add seed option | deterministic experiment 가능 |
| Add `examples/` images | visitor-friendly smoke test 가능 |
| Pin dependency versions | 장기 재현성 향상 |
| Add CI smoke test | import/runtime error 조기 발견 |

---

## 10. Minimal Requirements Suggestion

Current `requirements.txt` can be made more reproducible by version-bounding major dependencies.

Example:

```text
fastapi>=0.110
uvicorn[standard]>=0.29
python-multipart>=0.0.9
torch>=2.1
torchvision>=0.16
Pillow>=10.0
ftfy>=6.1
regex>=2023.0
tqdm>=4.66
packaging>=23.0
```

Exact versions should be confirmed in the environment where the final demo was tested.
