# Self-Demo 가이드

> **이 문서의 목적**
> 
> 
> 처음 보는 사람이 노트북을 직접 실행해보고, 막히는 순간 참고할 수 있도록 작성되었습니다.
> 
> 전체 실행 시간: 약 5~10분
> 

### 테스트 이미지 추천

데모 효과를 잘 확인하려면 아래처럼 명확한 스타일의 이미지를 사용하는 것이 좋습니다 (예시) :

| 사용할 이미지 유형 | 예상 예측 도메인 |
| --- | --- |
| 연필로 그린 선화 | `sketch` |
| 일반 사진 | `photo` |
| 만화 캐릭터 이미지 | `cartoon` |
| 3D 렌더링 이미지 | `rendering` |
| 자수 작품 사진 | `embroidery` |

### 한 줄 요약

이미지 한 장을 업로드하면, CLIP 모델이 그 이미지의 도메인(스타일)을 자동으로 추정합니다.

예: 스케치인가, 사진인가, 만화인가, 3D 렌더링인가 등.

### 데모 영상 시청

막히는 부분이 있을 때 영상을 참고하세요. 영상은 **자막(또는 나레이션)** 포함하고 있습니다.
https://www.youtube.com/watch?v=FWY20-wg71c

---

# 🌐 웹사이트

링크: https://chairwomans-start-demo.hf.space/

Demo 페이지(테스트 전, 테스트 후)를 제외한 나머지 페이지들은 연구 이해도를 위한 참고용입니다. 
| Team | Project | Method | Demo(테스트 전) | Demo(테스트 후) | 향후 계획 |
|------|---------|-----------|-----------|-----------|---------|
| <img width="424" height="928" alt="image" src="https://github.com/user-attachments/assets/228dd76a-8d41-4eb1-a76d-ac4c7cf4c6ce" /> | <img width="424" height="928" alt="image" src="https://github.com/user-attachments/assets/b25ae2f5-9b66-456d-a79c-bcdb381c3b54" /> | <img width="424" height="928" alt="image" src="https://github.com/user-attachments/assets/7654b3ed-6b5c-44bc-a32a-404b7189f4bb" /> | <img width="424" height="928" alt="image" src="https://github.com/user-attachments/assets/61e106b2-037d-4daa-81dd-7ee6e33d0b01" /> | <img width="424" height="928" alt="image" src="https://github.com/user-attachments/assets/995ef6e5-f5d2-4bd6-aa11-2d988fef22f4" /> | <img width="424" height="928" alt="image" src="https://github.com/user-attachments/assets/550cb9ad-7dc3-407e-89c6-d9eb49570246" /> |

### [Team]

- 팀 이름, 팀원 정보, 팀원 역할, 연구 구성 확인 가능

### [Project]

- 연구 주제, 기존 방식의 한계, 핵심 아이디어, 데이터셋 확인 가능

### [Method]

- 연구 전체 파이프라인
- 전처리 단계: 도메인 프롬프트 확장
- 테스트 단계 (현재 4번까지 진행 완료)
    1. Image Input & Augmentation
    2. Visual Encoder
    3. MTA - MeanShift
    4. Domain Assumption
    5. Domain-Weighted Embedding
    6. Final Classification

### [Demo]

- 실행 방법
    1. 원하는 이미지 업로드
       
       <img width="92" height="201" alt="image" src="https://github.com/user-attachments/assets/c9c03522-888f-4a3c-9ea4-f40bb6ca9c2f" />

    2. RandomCrop 결과 출력
 
       <img width="92" height="201" alt="image" src="https://github.com/user-attachments/assets/4c9225c9-a1cb-4e10-a288-b46250eb679a" />

    4. 'Domain Estimation 실행' 버튼 클릭
 
       <img width="92" height="201" alt="image" src="https://github.com/user-attachments/assets/10397a11-cf5c-4e9c-b9f7-f40aa56e6e56" />

    6. 몇 초 후 도메인 추정 결과 출력
        - MTA 실행 결과 (outlier 제거 수 확인)
      
          <img width="92" height="201" alt="image" src="https://github.com/user-attachments/assets/6f76e8dd-7d82-4dc9-9d04-049daa06556a" />

        - 추정된 도메인 결과 (추정된 상위 5개 도메인 확인 가능)
      
          <img width="92" height="201" alt="image" src="https://github.com/user-attachments/assets/3b9e74fb-949f-4afb-862b-4b3774f633da" />


### [Next]

- 완료된 실험과 진행 예정 계획, 최종 목표 확인 가능

---

# 👨🏼‍💻 코랩 실행

깃허브 내 [chairwomans-capstone/Demo.ipynb](https://github.com/chairwomans/chairwomans-capstone/blob/main/Demo.ipynb) 파일 다운로드 (사이트에서 **An error occurred라고 나오는 것은 정상입니다.)**
<img width="768" height="386" alt="image" src="https://github.com/user-attachments/assets/43513f6d-0536-4351-b048-809a4d224800" />


### 전체 실행 흐름

```
[Google Colab 열기]
      ↓
라이브러리 설치 (CLIP 등)
      ↓
import 및 CLIP 모델 로드
      ↓
도메인 프롬프트 정의
      ↓
도메인 텍스트 임베딩 생성
      ↓
MTA 함수 정의 (make_views / solve_mta)
      ↓
estimate_domain() 함수 정의
      ↓
이미지 업로드 → 결과 출력
```

## Step-by-Step 실행 가이드

### 1. Colab에서 노트북 열기

1. Google Colab 접속
2. **파일 → 노트북 업로드** → `Demo.ipynb` 선택
3. 런타임 타입 확인: **런타임 → 런타임 유형 변경 → GPU** (T4 권장)
4. ‘모두 실행’ 버튼을 누르면 한번에 실행됩니다.

> GPU 없이 CPU로 실행해도 되지만, MTA 단계에서 속도가 느립니다 (128개 뷰 처리).
> 
<img width="916" height="455" alt="image" src="https://github.com/user-attachments/assets/09bb2b50-3796-4cb3-abe5-2c22a2516d6d" />

### → 모두 실행 버튼을 누르지 않은 경우 아래 단계 참고 (코드 블럭 좌측 상단의 실행 버튼 클릭)
<img width="604" height="39" alt="image" src="https://github.com/user-attachments/assets/0160d91e-aec9-4a96-aab9-a9724269fed1" />

### 2. 필요한 모듈 설치 및 import 셀 실행

```python
!pip install ftfy regex tqdm git+https://github.com/openai/CLIP.git
```

```python
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
    ...
```

### 3. CLIP 모델 로드 셀 실행

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()
```

- 처음 실행 시 CLIP 모델 가중치 다운로드 (약 350MB, 30초~1분 소요)

### 4. 도메인 프롬프트 정의 셀 실행

- `domain_prompts` 딕셔너리 정의
- 총 18개 도메인: `photo`, `sketch`, `cartoon`, `rendering`, `painting`, `sculpture`, `origami`, `tattoo`, `graffiti`, `deviantart`, `embroidery`, `graphic`, `sticker`, `toy`, `videogame`, `drawing`, `plastic`, `misc`
- 출력 없음 — 정상입니다

### 5. 도메인 프롬프트 임베딩 생성 셀 실행

```python
domain_features_dict = {}
for domain, prompts in domain_prompts.items():
    ...
```

- 각 도메인의 텍스트 프롬프트를 CLIP 텍스트 인코더로 벡터화
- 출력 없음 — 정상입니다
- 완료 후 `domain_features` 행렬 (18 × 512) 생성됨

### 6. MTA 함수 정의 셀 실행

```python
def make_views(image, n_views):
    ...
```

- `make_views()`, `gaussian_kernel()`, `solve_mta()` 함수 정의
- 출력 없음 — 정상입니다

### 7. estimate_domain() 함수 정의 셀 실행

```python
def estimate_domain(image_path, n_views=127, top_k=5, show_plot=True):
    ...
```

- 전체 파이프라인을 하나로 묶은 메인 함수 정의
- 출력 없음 — 정상입니다

### 8. 이미지 업로드 및 결과 확인 (핵심 단계)

```python
from google.colab import files

uploaded = files.upload()
IMAGE_PATH = list(uploaded.keys())[0]

result = estimate_domain(
    image_path=IMAGE_PATH,
    n_views=127,
    top_k=5,
    show_plot=True
)
```

**실행 순서:**

1. 셀 실행 → 파란 **파일 선택** 버튼 클릭
2. 로컬에서 이미지 파일 선택 (JPG, PNG 모두 가능)
3. 업로드 완료 후 자동으로 추정 시작

**예상 콘솔 출력:**

```
이미지 로드 완료: my_image.jpg  |  크기: (512, 512)
총 128개 뷰 생성 완료
MTA 완료 → robust mode 획득

========================================
도메인          가중치
----------------------------------------
sketch         0.6023 ◀ 예측
photo          0.1842
cartoon        0.0891
drawing        0.0412
graphic        0.0198
========================================

최종 예측 도메인: [SKETCH]
```

**예상 시각화 출력:**

<img width="707" height="214" alt="image" src="https://github.com/user-attachments/assets/eafa74dc-fa86-4815-93d2-d71a668a0040" />

업로드한 이미지에 따라 출력 결과는 다릅니다.
| 왼쪽 패널 | 오른쪽 패널 |
| --- | --- |
| 업로드한 원본 이미지 | 상위 5개 도메인 가중치 가로 바 차트 |
|  | 예측 도메인은 빨간색으로 강조 |

## 참고) 자주 발생하는 문제

| 증상 | 원인 | 해결 |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'clip'` | 설치 후 런타임 재시작 안 함 | 런타임 → 런타임 재시작 후 설치 셀 제외하고 위에서부터 재실행 |
| 파일 업로드 버튼이 안 보임 | `google.colab` 환경 아님 | Colab에서 실행 중인지 확인. 로컬 실행 시 `image_path`를 직접 문자열로 지정 |
| 추정 결과가 직관과 다름 | 이미지 스타일이 복합적이거나 모호한 경우 | `top_k=5`로 상위 5개 도메인 가중치를 함께 확인. 2위 도메인도 참고 |
| CUDA out of memory | GPU 메모리 부족 | `n_views=63`으로 줄여서 실행 |
| 실행이 느림 (CPU 환경) | GPU 미사용 | Colab 런타임 → GPU로 변경 후 처음부터 재실행 |

## 참고) 파라미터 조정 가이드

`estimate_domain()` 함수의 파라미터를 변경해 실험할 수 있습니다:

```python
result = estimate_domain(
    image_path=IMAGE_PATH,
    n_views=63,    # 뷰 수 줄이면 빠르지만 정확도 소폭 하락
    top_k=10,      # 상위 10개 도메인까지 표시
    show_plot=False  # 시각화 없이 콘솔 출력만
)
```

| 파라미터 | 기본값 | 범위 | 효과 |
| --- | --- | --- | --- |
| `n_views` | 127 | 15~255 | 높을수록 정확하지만 느림 |
| `top_k` | 5 | 1~18 | 출력 도메인 수 |
| `show_plot` | True | True/False | 시각화 on/off |
