# 이사장님

## 팀 소개
| Name | Github |
|-----|-----|
| 설영은 | [@0euun](https://github.com/0euun) |
| 신지민 | [@zziminally](https://github.com/zziminally) |
| 윤희서 | [@HSYoon124](https://github.com/HSYoon124) |

## 연구 주제

> 테스트 이미지의 도메인을 자동으로 파악해 텍스트와 이미지 임베딩을 동적으로 재조합함으로써 도메인 변화에도 정확한 CLIP 기반 Zero-Shot 이미지 분류 연구

AI가 이미지를 보는 순간 **"이건 스케치네", "이건 회화네"** 를 스스로 파악하고, 그 도메인에 맞게 판단 기준을 자동으로 바꿔 **domain shift 환경에서도 정확하게 분류**한다.

<br>

---

<br>

## 1. 문제 제기

CLIP(Contrastive Language–Image Pre-training)은 이미지와 텍스트를 함께 이해하는 멀티모달 Vision-Language Model(VLM)이다.
별도의 학습 없이 텍스트 설명만으로 이미지를 분류하는 **Zero-Shot 분류** 능력이 강점이다.

그런데 한 가지 치명적인 한계가 있다.

- **고정된 클래스 대표 벡터**: 기존 CLIP은 "고양이 사진", "고양이 스케치" 등 여러 텍스트 프롬프트를 평균 내어 클래스 대표 벡터를 미리 만들어 고정해둔다.
- **Domain Shift에 취약**: 스케치 도메인의 이미지가 들어와도, 회화 도메인의 이미지가 들어와도 항상 똑같은 평균 벡터로만 비교한다. 도메인이 달라지는 순간 이미지-텍스트 정렬이 어긋나 분류 성능이 크게 떨어진다.
- **기존 Domain Adaptation의 한계**: 기존 방식은 새로운 도메인마다 추가 데이터를 모아 fine-tuning해야 해서 비효율적이고, 성능 향상도 제한적이다.

<br>

## 2. 해결 아이디어

본 연구는 **추가 학습 없이, 테스트 시점에서만** 도메인을 스스로 파악하고 적응하는 **Test-Time Domain Adaptation** 방식을 제안한다.

테스트 이미지가 들어오면 다음 세 가지를 순서대로 수행한다.

1. **Augmentation**: 원본 이미지 1장으로부터 Stable Diffusion V2(63장)와 RandomCrop(64장)을 통해 총 128장의 augmented view를 생성하고, MeanShift 기반 MTA로 outlier를 제거해 robust한 이미지 임베딩 m*를 획득한다.
2. **도메인 자동 추정**: m*와 도메인 프롬프트 임베딩 간 코사인 유사도를 계산해 "이 이미지가 어떤 도메인인지"를 확률적으로 추정한다.
3. **동적 임베딩 재조합**: 추정된 도메인 가중치를 텍스트 임베딩과 이미지 임베딩 **양쪽에 동시에** 적용해, 해당 도메인에 최적화된 비교 기준을 실시간으로 생성한다.

<br>

## 3. 기술 / 구현

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

## 4. MVP / 배포

- MTA를 통한 도메인 추정을 사용자가 직접 경험할 수 있는 웹 데모 시연
- 중간 실험 결과 및 향후 확장 방향 제시 - 텍스트와 이미지 임베딩을 동적으로 재조합하여 최종 클래스 분류

<br>

## 5. 차별성
- **단순 prompt tuning이 아닌 동적 조정 구조**
    - 입력 상황에 따라 프롬프트와 이미지 표현이 함께 조정됨
- **MTA를 전체 파이프라인의 출발점으로 활용**
    - outlier를 제거한 안정적인 이미지 표현을 기반으로 도메인 추정
- **도메인 정보를 텍스트와 이미지 양쪽에 반영**
    - 텍스트 프롬프트뿐 아니라 이미지 인코딩 과정에도 도메인 힌트 적용
- **도메인 추정을 독립적인 단계로 분리**
    - 입력 이미지가 어떤 도메인에 가까운지 명시적으로 계산

<br>

## 6. 참고 문헌

| 자료 | 링크 |
|------|------|
| CLIP | https://github.com/openai/CLIP |
| DiffTPT | https://github.com/chunmeifeng/DiffTPT |
| MaPLe | https://github.com/muzairkhattak/multimodal-prompt-learning |
| MTA | https://github.com/MaxZanella/MTA |

- Radford et al., *Learning Transferable Visual Models From Natural Language Supervision* (CLIP), ICML 2021
- Khattak et al., *MaPLe: Multi-Modal Prompt Learning*, CVPR 2023
- Zanella et al., *On the Test-Time Zero-Shot Generalization of Vision-Language Models: Do We Really Need Prompt Learning?*, CVPR 2024
- 추후 업데이트 예정
