# Experiments

> 이 문서는 현재까지 완료된 실험과 향후 수행할 정량 평가를 구분하여 정리합니다.  
> 현재 공개 저장소의 핵심 실험 결과는 **PACS 기반 domain estimation에서 MTA 적용 전 94.64% → 적용 후 97.91%로 +3.27%p 향상**입니다.

---

## 1. Experiment Overview

| ID | 실험 | 목적 | 현재 상태 |
|---|---|---|---|
| E1 | Domain Prompt Design | 도메인별 텍스트 프롬프트가 도메인 추정에 충분한지 검증 | 완료 |
| E2 | Data Augmentation Exploration | RandomCrop과 Stable Diffusion 후보 방식 비교 | 부분 완료 |
| E3 | MTA Mode Validation | robust mode `m*`가 원본 의미를 유지하는지 검증 | 완료 |
| E4 | PACS Domain Estimation | MTA 적용 여부에 따른 도메인 추정 정확도 비교 | 완료 |
| E5 | Final Zero-Shot Classification | TPT, DiffTPT, MaPLe 대비 최종 분류 성능 비교 | Future Work |

---

## 2. E1 - Domain Prompt Design

### Goal

CLIP text encoder와 수작업 domain prompt bank만으로 이미지의 도메인을 추정할 수 있는지 확인합니다.

### Process

1. PACS 4개 도메인(`photo`, `art_painting`, `cartoon`, `sketch`)에서 시작
2. 각 도메인의 시각적 속성을 자연어로 기술
3. CLIP 공식 템플릿 스타일을 참고해 표현 확장
4. PACS 도메인 추정 결과가 낮은 prompt를 반복 수정
5. 최종적으로 17개 도메인, 총 75개 prompt로 확장

### Key Finding

초기 sketch prompt는 다음처럼 단순했습니다.

```python
"sketch": [
    "a black and white pencil sketch",
    "a grayscale line drawing",
    "a monochrome sketch",
]
```

하지만 이 표현만으로는 `art_painting`과의 구분이 충분하지 않았습니다. 이후 sketch의 핵심 속성인 윤곽선, 흰 배경, 검은 선, 음영 없는 line art를 명시하여 총 20개 prompt로 확장했습니다.

---

## 3. E2 - Data Augmentation Exploration

### Goal

테스트 이미지 한 장에서 다양한 view를 만들어 CLIP image embedding의 안정성을 높입니다.

### RandomCrop

현재 구현에 직접 사용된 방식입니다.

| Setting | Description |
|---|---|
| Transform | `torchvision.transforms.RandomResizedCrop(224)` |
| Current demo | original 1 + random crop 127 = 128 views |
| Strength | 빠르고 단순하며 실시간 데모에 적합 |
| Risk | 객체가 잘리거나 배경만 포함된 outlier crop 발생 가능 |

### Stable Diffusion Candidates

Stable Diffusion은 연구 노트북에서 후보 방식으로 비교되었습니다.

| Method | 특징 | 관찰 결과 | 현재 판단 |
|---|---|---|---|
| Image Variation | 원본 스타일 변형 | 원본 구조 보존 미흡 | 미채택 |
| img2img | 원본 구조 유지하며 변형 | `strength=0.3`에서 구조 보존 우수 | 후보 채택 |
| ControlNet(Canny) | edge 기반 구조 보존 | 과도한 윤곽선 artifact 발생 | 미채택 |

### Current Implementation Note

현재 공개 웹 데모에는 RandomCrop 기반 augmentation만 연결되어 있습니다. Stable Diffusion 기반 view 생성은 추후 pipeline 확장 범위입니다.

---

## 4. E3 - MTA Mode Validation

### Goal

MeanShift 기반 MTA로 계산한 mode `m*`가 원본 이미지의 의미를 잘 보존하는지 확인합니다.

### Evaluation Items

| 평가 항목 | 의미 |
|---|---|
| Original view ↔ mode cosine similarity | `m*`가 원본 의미를 유지하는지 확인 |
| All views ↔ mode mean similarity | augmentation view들이 같은 의미를 유지하는지 확인 |
| All views ↔ mode std | view 간 변동성이 얼마나 큰지 확인 |
| Mode ↔ simple average feature similarity | MTA mode와 단순 평균의 방향 차이 확인 |
| Inlierness score distribution | view별 신뢰도 가중치가 적절히 분포하는지 확인 |

### Reported Result

프로젝트 보고서 기준 MTA 수렴 검증 결과는 다음과 같습니다.

| 평가 항목 | 값 |
|---|---:|
| 원본 view ↔ mode 코사인 유사도 | 0.9465 |
| 전체 view ↔ mode 평균 유사도 | 0.9341 |
| 전체 view ↔ mode 표준편차 | 0.0343 |
| mode ↔ 단순 평균 feature 코사인 유사도 | 0.9918 |

### Interpretation

- `0.9465`의 original-mode similarity는 MTA mode가 원본 이미지의 의미적 방향을 상당히 잘 보존함을 의미합니다.
- `0.0343`의 낮은 표준편차는 다수의 crop view가 전반적으로 일관된 의미를 유지했음을 시사합니다.
- `0.9918`의 mode-average similarity는 전체 방향은 유지되지만, MTA의 실제 이점은 단순 방향 변화보다 outlier view의 영향 완화에서 확인해야 함을 의미합니다.

---

## 5. E4 - PACS Domain Estimation

### Goal

MTA 적용 여부가 domain estimation accuracy에 미치는 영향을 PACS 데이터셋에서 측정합니다.

### Experimental Setup

| 항목 | 설정 |
|---|---|
| Dataset | PACS |
| Domains | photo, art_painting, cartoon, sketch |
| Backbone | CLIP ViT-B/32 |
| Baseline | MTA 미적용: 원본 이미지 1장 |
| Ours | MTA 적용: 원본 1장 + RandomCrop 127장 |
| Metric | Domain Estimation Accuracy |
| Temperature | CLIP pretrained `logit_scale.exp()` |

### Main Result

| 조건 | 전체 도메인 추정 정확도 |
|---|---:|
| MTA 미적용 | 94.64% (9454 / 9991) |
| MTA 적용 | 97.91% (9782 / 9991) |
| 개선 폭 | **+3.27%p** |

### Domain-wise Result

| Domain | MTA 미적용 | MTA 적용 | 변화 |
|---|---:|---:|---:|
| photo | 92.63% | 98.20% | +5.57%p |
| art_painting | 93.85% | 95.95% | +2.10%p |
| cartoon | 95.22% | 95.95% | +0.73%p |
| sketch | 96.01% | 99.97% | +3.96%p |

### Interpretation

- MTA 적용 후 전체 domain estimation accuracy가 3.27%p 향상되었습니다.
- `photo`와 `sketch`에서 개선 폭이 크게 나타났습니다.
- 이는 시각적 특성이 비교적 명확한 도메인에서 MeanShift 기반 outlier 제거가 도메인 신호를 더 선명하게 만들 수 있음을 시사합니다.
- `art_painting`과 `cartoon`은 도메인 경계가 상대적으로 모호하여 개선 폭이 제한적이었습니다.

---

## 6. Current Result Summary

| Component | Evidence | Status |
|---|---|---|
| Domain prompt bank | 17 domains, 75 prompts | 완료 |
| RandomCrop view generation | 128 views generation | 완료 |
| Stable Diffusion 후보 비교 | img2img strength=0.3이 구조 보존 우수 | 후보 선정 |
| MTA mode validation | original-mode similarity 0.9465 | 완료 |
| PACS domain estimation | 94.64% → 97.91% | 완료 |
| Final class prediction | TPT/DiffTPT 비교 필요 | Future Work |

---

## 7. Planned Evaluation

최종 연구 단계에서는 domain estimation을 넘어 Zero-Shot class classification 정확도를 측정합니다.

### Baselines

| Method | 비교 목적 |
|---|---|
| CLIP Zero-Shot | 고정 평균 prompt ensemble baseline |
| TPT | test-time prompt tuning baseline |
| DiffTPT | Stable Diffusion 기반 TTA baseline |
| MTA-only | domain weighting 없이 image-side MTA만 적용한 경우 |
| MaPLe | learning-based multimodal prompt upper bound |

### Datasets

- PACS
- ImageNet
- ImageNet-A
- ImageNet-V2
- ImageNet-R
- ImageNet-Sketch
- SUN397
- Aircraft
- EuroSAT
- StanfordCars
- Food101
- OxfordPets
- Flower102
- Caltech101
- DTD
- UCF101


---

## 8. Reproducibility Notes

현재 공개 저장소에는 full PACS batch evaluation script가 별도 CLI로 제공되어 있지 않습니다. 따라서 실험 재현은 다음 순서를 권장합니다.

1. `Demo.ipynb` 또는 `research/DomainpromptPACS.ipynb` 확인
2. PACS 데이터셋 로컬 준비
3. `domain_prompts.py`의 prompt bank 로드
4. `clip_pipeline.py`의 domain feature 생성 로직 재사용
5. `mta.py`의 `make_views()`와 `solve_mta()`로 MTA 적용
6. domain label과 predicted top-1 domain 비교
