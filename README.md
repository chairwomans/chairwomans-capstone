# 이사장님
서비스명: DoFit

## 팀원 소개

| Name | GitHub | Role |
| --- | --- | --- |
| 설영은 | [@0euun](https://github.com/0euun) | 총괄 · 실험 설계 · 알고리즘 리드 |
| 신지민 | [@zziminally](https://github.com/zziminally) | 모델 구현 · 인프라 · 알고리즘 구현 |
| 윤희서 | [@HSYoon124](https://github.com/HSYoon124) | 데이터 · 평가 · 프롬프트 설계 |

지도교수: 황의원 교수님 | 이화여자대학교

## 한 줄 요약

> 테스트 이미지의 도메인을 자동으로 파악해 텍스트와 이미지 임베딩을 동적으로 재조합함으로써 도메인 변화에도 정확한 CLIP 기반 Zero-Shot 이미지 분류 연구
> 

이미지가 들어오는 순간 **"이건 스케치네", "이건 회화네"** 를 스스로 파악하고, 그 도메인에 맞게 판단 기준을 자동으로 바꿔 domain shift 환경에서도 정확하게 분류한다.

---

## 1. 문제 제기

CLIP(Contrastive Language–Image Pre-training)은 이미지와 텍스트를 함께 이해하는 멀티모달 Vision-Language Model(VLM)이다.
별도의 학습 없이 텍스트 설명만으로 이미지를 분류하는 **Zero-Shot 분류** 능력이 강점이다.

그런데 치명적인 한계가 존재한다. 

| 문제 | 설명 |
| --- | --- |
| **고정된 클래스 대표 벡터** | 기존 CLIP은 "고양이 사진", "고양이 스케치" 등 여러 텍스트 프롬프트를 평균 내어 클래스 대표 벡터를 미리 만들어 고정 |
| **Domain Shift에 취약** | 스케치·회화·위성사진 등 도메인이 달라져도 항상 똑같은 평균 벡터로 비교하기 때문에 도메인이 달라지는 순간 이미지-텍스트 정렬이 어긋나 분류 성능 급락 |
| **기존 DA의 한계** | 기존 방식은 새로운 도메인마다 추가 데이터를 모아 fine-tuning해야 해서 비효율적이고, 성능 향상도 제한적 |

## 2. 제안 방법

**추가 학습 없이, 테스트 시점에서만** 도메인을 스스로 파악하고 적응하는 **Test-Time Domain Adaptation** 방식을 제안한다.

테스트 이미지가 들어오면 다음 세 가지를 순서대로 수행한다.

1. **Augmentation**: 원본 이미지 1장으로부터 Stable Diffusion V2(63장)와 RandomCrop(64장)을 통해 총 128장의 augmented view를 생성하고, MeanShift 기반 MTA로 outlier를 제거해 robust한 이미지 임베딩 m*를 획득한다.
2. **도메인 자동 추정**: m*와 도메인 프롬프트 임베딩 간 코사인 유사도를 계산해 "이 이미지가 어떤 도메인인지"를 확률적으로 추정한다.
3. **동적 임베딩 재조합**: 추정된 도메인 가중치를 텍스트 임베딩과 이미지 임베딩 **양쪽에 동시에** 적용해, 해당 도메인에 최적화된 비교 기준을 실시간으로 생성한다.

## 3. 전체 파이프라인

전체 파이프라인은 **사전 단계**와 **테스트 단계**로 구성된다.

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

**지원 도메인 (18종)**

`photo` `sketch` `cartoon` `rendering` `painting` `sculpture` `origami` `tattoo` `graffiti` `deviantart` `embroidery` `graphic` `sticker` `toy` `videogame` `drawing` `plastic` `misc`

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

## 4. 차별성

| 구분 | 기존 CLIP | TPT (NeurIPS 2022)  | DiffTPT (ICCV 2023)  | 본 연구 (Ours) |
| --- | --- | --- | --- | --- |
| 텍스트 임베딩 | 고정 평균 | 학습된 프롬프트 | 학습된 프롬프트 | **도메인 가중 평균 (동적)**  |
| 이미지 임베 | 단순 평균 | 단순 평균 | 단순 평균 | **MeanShift 기반 outlier 제거** |
| Data Augmentation | - | RandomCrop | RandomCrop + Stable Diffusion | **RandomCrop + Stable Diffusion** |
| 도메인 인식 | - | - | - | **명시적 추정 후 가중치 반영** |
| 추가 학습 | 불필요 | 필요 (역전파) | 필요 (역전파) | **불필요** **(training-free)** |

## 5. 실험

### 데이터셋

아래 데이터셋을 가지고 추후 Zero-Shot 이미지 분류 실험 예정 (정확도 검증용)

| 구분 | 데이터셋 | 설명 |
| --- | --- | --- |
| Domain Generalization 표준 벤치마크 | PACS | Photo·Art painting·Cartoon·Sketch 4개 도메인 |
| Domain Shift 측정 (5종) | ImageNet | 일반 실사 이미지 (기준) |
|  | ImageNet-A | 자연 adversarial 이미지 |
|  | ImageNet-V2 | ImageNet 재수집 버전 |
|  | ImageNet-R | 회화·만화·스케치 등 렌더링 |
|  | ImageNet-Sketch | 순수 스케치 도메인 |
| 특정 도메인 분류 (10종) | Aircraft, EuroSAT, StanfordCars, Food101 | 항공기·위성·자동차·음식 |
|  | OxfordPets, Flower102, Caltech101, DTD, UCF101, SUN397 | 반려동물·꽃·객체·질감·행동·장면 |

### 비교 대상 (Baseline)

아래 비교 대상을 가지고 추후 비교 실험 예정 (기존 연구들과의 차별성 검증용)

| 모델 | 방식 | 비교 목적 |
| --- | --- | --- |
| CLIP Zero-Shot | 고정 평균 프롬프트 앙상블 | 순수 베이스라인 |
| TPT | 테스트 시점 프롬프트 동적 튜닝 | 동일 TTA 설정 직접 비교 |
| MTA (단독) | 도메인 추정 없이 MeanShift TTA만 적용 | 도메인 재조합의 실질 기여 측정 |
| MaPLe | 멀티모달 프롬프트 사전 학습 | 학습 기반 방법 성능 상한 참고 |

### 현재까지 완료된 실험

**① Data Augmentation 탐색**

ImageNet-R (200클래스, 30,000장) 기준으로 원본 1장 + RandomResizedCrop 127장 = 총 128장 생성 정상 동작 확인. Stable Diffusion 방향으로 Image Variation / img2img / ControlNet 세 가지 파이프라인을 각각 실험했으며, img2img (`strength=0.3`)가 원본 구조를 가장 잘 유지하는 것을 확인. 최종적으로 **SD V2 63장 + RandomCrop 64장 = 128장** 조합을 목표로 설정한 상태.

**② MTA 구현 및 수렴 검증**

ImageNet-R 이미지 기준으로 `solve_mta()` 실행 결과, MTA가 계산한 mode가 단순 평균 대비 원본에 더 가까우면서도 outlier 영향을 줄인 robust한 표현임을 수치로 확인.

| 항목 | 값 |
| --- | --- |
| 원본 view ↔ mode 코사인 유사도 | 0.9684 |
| 전체 view ↔ mode 평균 유사도 | 0.9244 |
| 전체 view ↔ mode 유사도 표준편차 | 0.0439 |
| mode ↔ 단순 평균 feature 유사도 | 0.9839 |
| mode norm | 1.0000 (정규화 정상) |

**③ 도메인 프롬프트 설계 및 PACS 검증**

CLIP 공식 ImageNet 템플릿을 참고해 PACS 4개 도메인(`photo`, `art_painting`, `cartoon`, `sketch`) 맞춤 프롬프트 직접 설계 후 실제 이미지로 추정 정확도 1차 검증 완료.

```
PACS 검증 예시 (정답: sketch)
→ 예측: sketch
  sketch: 0.7065 / cartoon: 0.2480 / art_painting: 0.0278 / photo: 0.0177
```

이후 도메인을 18개로 확장. 확장된 도메인은 domain_prompts.py 참고.

---

## 6. 빠른 시작

[self_demo.md](https://github.com/chairwomans/chairwomans-capstone/blob/main/self_demo.md)에서 자세한 내용 확인 가능

[데모 시연 참고 영상](https://www.youtube.com/watch?v=FWY20-wg71c)

### 방법 1. 웹 데모 (권장, 설치 불필요)

👉 **https://chairwomans-start-demo.hf.space/**

1. Demo 페이지로 이동
2. 이미지 업로드
3. "Domain Estimation 실행" 버튼 클릭
4. 상위 5개 도메인 가중치 및 최종 예측 확인

### 방법 2. Google Colab

```
1. Demo.ipynb 다운로드 (GitHub에서 raw 다운로드)
2. Google Colab 업로드 → 런타임: GPU (T4 권장)
3. "모두 실행" 클릭
4. 이미지 업로드 → 결과 확인
```

> **전체 실행 시간**: 약 5~10분 (첫 실행 시 CLIP 모델 다운로드 ~350MB 포함)
> 

### 방법 3. 로컬 실행

```bash
git clone https://github.com/chairwomans/chairwomans-capstone.git
cd chairwomans-capstone
pip install -r requirements.txt
pip install git+https://github.com/openai/CLIP.git
uvicorn server:app --reload   # 서버 실행
```

> ‘방법 1. 웹 데모’를 로컬에서 실행하는 방법입니다. 로컬에서 실행하기 위하여 Python 버전을 3.12.4로 맞추시는 것을 추천드립니다.
> 

## 7. 레포지토리 구조

```
chairwomans-capstone/
├── .github/                         # 깃허브 문서용(pr, issue) 폴더
│   ├── ISSUE_TEMPLATE/              #   이슈 폴더
│   │   └── todo_request.md          #     이슈 등록 템플릿 (할 일 요청 양식)
│   └── PULL_REQUEST_TEMPLATE.md     #   PR 등록 템플릿 (코드 리뷰 요청 양식)
├── clip/                            # OpenAI CLIP 모델 코드 (로컬 포함본)
│   ├── __init__.py                  #   현재 디렉토리를 파이썬 패키지로 인식
│   ├── bpe_simple_vocab_16e6.txt.gz #   토크나이저(Tokenizer) 사전 데이터
│   ├── clip.py                      #   load(), tokenize() 등 공개 API
│   ├── model.py                     #   ViT 기반 Visual/Text Transformer 구조 정의
│   └── simple_tokenizer.py          #   BPE 토크나이저 (bpe_simple_vocab_16e6.txt.gz 사용)
├── research/                        # 연구 전용 실험 폴더
│   │                                #   ※ 이 폴더는 오로지 연구·탐색 목적의 파일만 모아둡니다.
│   │                                #     실제 서비스 파이프라인과 직접 연결되지 않습니다.
│   ├── DataAugmentation.ipynb       #   RandomCrop / Stable Diffusion V2 augmentation 탐색
│   ├── DomainpromptPACS.ipynb       #   PACS 데이터셋 기반 도메인 프롬프트 초기 검증
│   ├── MTA_mode.ipynb               #   MTA solve_mta() 수렴 과정 및 mode 시각화 실험
│   └── research.md                  #   어느 파일 있는지 요약
├── docs/                            # 프로젝트 문서 폴더
│   ├── Ideation.md                  #   연구 배경, 아이디어 도출 과정, 핵심 가설
│   ├── Related_work.md              #   TPT·MaPLe·MTA 논문 분석 및 본 연구와의 차별점 정리
│   ├── Team_Ground_Rule.md          #   팀 협업 규칙 (소통·회의·PR 규약)
│   ├── elevator_speech.md           #   프로젝트 소개문
│   └── project briefs.md            #   프로젝트 요약
├── web-demo/                        # 웹 데모 프론트엔드
│   ├── css/                         #   css 폴더
│   │   └── style.css                #     스타일시트
│   └── js/                          #   js 폴더
│       └── main.js                  #     /predict 엔드포인트 fetch 및 도메인 가중치 렌더링
│   └── demo.html                    #   이미지 업로드 UI, 결과 시각화 페이지
├── .gitattributes                   # 파일, 경로 속성 정의
├── .gitignore                       # 특정 파일, 폴더 추적 무시
├── Demo.ipynb                       # 메인 데모 노트북 (Google Colab에서 실행 가능)
├── Dockerfile                       # HuggingFace Spaces 컨테이너 배포용
├── README.md                        # 프로젝트 소개 README.md
├── clip_pipeline.py                 # 전체 추론 파이프라인 진입점
├── domain_prompts.py                # 18개 도메인별 텍스트 프롬프트 딕셔너리
├── mta.py                           # MeanShift 기반 MTA (Test-Time Augmentation) 구현
├── requirements.txt                 # 의존성 목록 (필요한 라이브러리 명시)
├── self_demo.md                     # Self-Demo 실행 가이드
└── server.py                        # FastAPI 기반 웹 데모 백엔드
```

## 8. 참고 자료

| 자료 | 링크 |
| --- | --- |
| CLIP | [OpenAI/CLIP](https://github.com/openai/CLIP) |
| MTA | [MaxZanella/MTA](https://github.com/MaxZanella/MTA) |
| DiffTPT | [chunmeifeng/DiffTPT](https://github.com/chunmeifeng/DiffTPT) |
| MaPLe | [muzairkhattak/multimodal-prompt-learning](https://github.com/muzairkhattak/multimodal-prompt-learning) |
| ImageNet | [ImageNet](https://www.image-net.org) |
| PACS | [PACS](https://huggingface.co/datasets/flwrlabs/pacs) |
| HuggingFace | [HuggingFace](https://huggingface.co/) |
- Radford et al., *Learning Transferable Visual Models From Natural Language Supervision*, ICML 2021
- Shu et al., *Test-Time Prompt Tuning for Zero-Shot Generalization in Vision-Language Models*, NeurIPS 2022
- Khattak et al., *MaPLe: Multi-Modal Prompt Learning*, CVPR 2023
- Feng et al., *Diverse Data Augmentation with Diffusions for Effective Test-time Prompt Tuning*, ICCV 2023
- Zanella et al., *On the Test-Time Zero-Shot Generalization of Vision-Language Models: Do We Really Need Prompt Learning?*, CVPR 2024
- 추후 실험 진행하면서 추가 예정
