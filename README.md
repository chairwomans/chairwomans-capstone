# 이사장님

## Team
| Name | Github |
|-----|-----|
| 설영은 | [@0euun](https://github.com/0euun) |
| 신지민 | [@zziminally](https://github.com/zziminally) |
| 윤희서 | [@HSYoon124](https://github.com/HSYoon124) |

## Summary

> 테스트 이미지의 도메인을 자동으로 파악해 텍스트와 이미지 임베딩을 동적으로 재조합함으로써 도메인 변화에도 정확한 CLIP 기반 Zero-Shot 이미지 분류 연구

AI가 이미지를 보는 순간 **"이건 스케치네", "이건 회화네"** 를 스스로 파악하고, 그 도메인에 맞게 판단 기준을 자동으로 바꿔 **domain shift 환경에서도 정확하게 분류**한다.

<br>

---

<br>

## 1. Problem Statement

CLIP(Contrastive Language–Image Pre-training)은 이미지와 텍스트를 함께 이해하는 멀티모달 Vision-Language Model(VLM)이다.
별도의 학습 없이 텍스트 설명만으로 이미지를 분류하는 **Zero-Shot 분류** 능력이 강점이다.

그런데 한 가지 치명적인 한계가 있다.

- **고정된 클래스 대표 벡터**: 기존 CLIP은 "고양이 사진", "고양이 스케치" 등 여러 텍스트 프롬프트를 평균 내어 클래스 대표 벡터를 미리 만들어 고정해둔다.
- **Domain Shift에 취약**: 스케치 도메인의 이미지가 들어와도, 회화 도메인의 이미지가 들어와도 항상 똑같은 평균 벡터로만 비교한다. 도메인이 달라지는 순간 이미지-텍스트 정렬이 어긋나 분류 성능이 크게 떨어진다.
- **기존 Domain Adaptation의 한계**: 기존 방식은 새로운 도메인마다 추가 데이터를 모아 fine-tuning해야 해서 비효율적이고, 성능 향상도 제한적이다.

## 2. Proposed Idea

본 연구는 **추가 학습 없이, 테스트 시점에서만** 도메인을 스스로 파악하고 적응하는 **Test-Time Domain Adaptation** 방식을 제안한다.

테스트 이미지가 들어오면 다음 세 가지를 순서대로 수행한다.

1. **Augmentation**: 원본 이미지 1장으로부터 Stable Diffusion V2(63장)와 RandomCrop(64장)을 통해 총 128장의 augmented view를 생성하고, MeanShift 기반 MTA로 outlier를 제거해 robust한 이미지 임베딩 m*를 획득한다.
2. **도메인 자동 추정**: m*와 도메인 프롬프트 임베딩 간 코사인 유사도를 계산해 "이 이미지가 어떤 도메인인지"를 확률적으로 추정한다.
3. **동적 임베딩 재조합**: 추정된 도메인 가중치를 텍스트 임베딩과 이미지 임베딩 **양쪽에 동시에** 적용해, 해당 도메인에 최적화된 비교 기준을 실시간으로 생성한다.


## 3. Pipeline

전체 파이프라인은 **사전 단계**와 **테스트 단계**로 구성된다.

### 사전 단계 (Pre-processing)

```
도메인별 텍스트 프롬프트 구성
   ↓
CLIP 기본 템플릿 확인 (26개 데이터셋 기반)
   ↓
도메인 관련 템플릿 추가 및 수정
   ↓
최종 프롬프트 확정 → 도메인 프롬프트 임베딩 사전 계산
```

### 테스트 단계 (Test-Time)

```
테스트 이미지 1장 입력
↓
Augmentation — Stable Diffusion V2 (63장) + RandomCrop (64장) + 원본 (1장) = 총 128장
↓
CLIP Visual Encoder — 128장 각각 임베딩 벡터 추출
↓
MTA (MeanShift-based TTA) — outlier view 자동 제거 → robust한 이미지 임베딩 m* 획득
↓
도메인 추정 — m*와 도메인 프롬프트 임베딩 간 코사인 유사도 → Softmax (τ=0.07) → 도메인 가중치
↓ (동일한 도메인 가중치 적용)
↓                                    ↓
이미지 임베딩                       텍스트 임베딩
Linear Projection (768d → 512d)     클래스별 템플릿 가중 평균 재조합 → 클래스 대표 벡터
↓                                    ↓
↓──────── 코사인 유사도 계산 ─────────↓
↓
최종 클래스 분류
```

## 4. Key Idea

- **Test-Time Domain Adaptation**: fine-tuning 없이 테스트 시점에서만 도메인에 적응한다. 새로운 도메인이 와도 추가 학습이 필요 없다.
- **멀티모달 동시 적응**: 텍스트 임베딩만 바꾸는 게 아니라, 이미지 임베딩과 텍스트 임베딩 **양쪽을 동시에** 도메인에 맞게 조정해 정렬 품질을 높인다.
- **MTA (MeanShift-based TTA)**: 단순 평균 대신 MeanShift 알고리즘으로 outlier를 자동 제거해 노이즈에 강한 이미지 임베딩을 획득한다.


## 5. Related Research Area

본 연구는 다음 연구 분야의 교차 영역에 해당한다.

- **Vision-Language Model (VLM)**: CLIP 등 이미지-텍스트 멀티모달 모델 연구
- **Domain Adaptation / Domain Generalization**: domain shift 환경에서의 모델 강건성 연구
- **Test-Time Adaptation (TTA)**: 추가 학습 없이 테스트 시점에서만 모델을 적응시키는 연구
- **Prompt Engineering**: Zero-Shot 성능을 높이기 위한 텍스트 프롬프트 설계 연구

## 6. Experiments

### 데이터셋

| 구분 | 데이터셋 | 설명 |
|------|----------|------|
| Domain Shift 측정 (5종) | ImageNet | 일반 실사 이미지 (기준) |
| | ImageNet-A | 자연 adversarial 이미지 |
| | ImageNet-V2 | ImageNet 재수집 버전 |
| | ImageNet-R | 회화·만화·스케치 등 렌더링 이미지 |
| | ImageNet-Sketch | 순수 스케치 도메인 이미지 |
| 특정 도메인 분류 (10종) | Aircraft, EuroSAT, StanfordCars, Food101 | 항공기·위성·자동차·음식 |
| | OxfordPets, Flower102, Caltech101, DTD, UCF101, SUN397 | 반려동물·꽃·객체·질감·행동·장면 |

### 비교 대상 (Baseline)
| 모델 | 방식 | 비교 목적 |
|------|------|-----------|
| **CLIP Zero-Shot** | 고정 평균 프롬프트 앙상블, 아무 적응 없이 분류 | 순수 베이스라인 — 우리 방법이 얼마나 개선되는지 측정 |
| **TPT** | 테스트 시점에 프롬프트를 동적으로 튜닝 | 동일한 Test-Time Adaptation 설정에서의 직접 비교 |
| **MTA (단독)** | 도메인 추정 없이 MeanShift TTA만 적용 | 도메인 가중 재조합의 실질적 기여도 측정 |
| **MaPLe** | 멀티모달 프롬프트를 학습 데이터로 사전 학습 | 학습 기반 방법 대비 성능 상한선 참고용 |

## 7. 실행 환경

본 연구는 **Google Colab** 환경에서 실행한다.

```
- 런타임: GPU (A100 권장)
- Python: 추후 업데이트 예정
- 주요 라이브러리: 추후 업데이트 예정
```

## 8. 참고 자료

| 자료 | 링크 |
|------|------|
| CLIP 공식 코드 | https://github.com/openai/CLIP |
| DiffTPT | https://github.com/chunmeifeng/DiffTPT |
| MaPLe | https://github.com/muzairkhattak/multimodal-prompt-learning |
| MTA | https://github.com/MaxZanella/MTA |

- Radford et al., *Learning Transferable Visual Models From Natural Language Supervision* (CLIP), ICML 2021
- Khattak et al., *MaPLe: Multi-Modal Prompt Learning*, CVPR 2023
- Zanella et al., *On the Test-Time Zero-Shot Generalization of Vision-Language Models: Do We Really Need Prompt Learning?*, CVPR 2024
- 추후 업데이트 예정
