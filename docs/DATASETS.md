# Datasets

> 이 문서는 본 연구에서 고려한 데이터셋과 각 데이터셋의 역할을 정리합니다.  
> 데이터셋은 크게 **Domain Shift 측정용**과 **Domain-Specific Classification 측정용**으로 나뉩니다.

---

## 1. Dataset Selection Criteria

본 프로젝트의 데이터셋 선정 기준은 다음 두 가지입니다.

1. **Domain Shift를 명확히 측정할 수 있는가?**
   - 같은 class라도 photo, sketch, cartoon, rendering 등 시각적 도메인이 달라지는 상황을 다뤄야 합니다.
2. **기존 CLIP / TPT / DiffTPT / MTA 계열 연구와 비교 가능한가?**
   - 선행 연구에서 자주 쓰인 benchmark를 포함해야 향후 정량 비교가 가능합니다.

---

## 2. Domain Shift Evaluation Datasets

| Dataset | 역할 | 설명 |
|---|---|---|
| PACS | Domain estimation 검증 | Photo, Art painting, Cartoon, Sketch 4개 도메인과 7개 클래스 |
| ImageNet | 기준 분포 | 일반 실사 이미지 중심의 baseline dataset |
| ImageNet-A | 자연 adversarial shift | CLIP/vision model이 어려워하는 자연 adversarial 이미지 |
| ImageNet-V2 | 재수집 분포 변화 | ImageNet과 유사하지만 재수집으로 생긴 distribution shift 평가 |
| ImageNet-R | rendition shift | 회화, 만화, 스케치 등 렌더링 기반 변형 이미지 |
| ImageNet-Sketch | sketch domain shift | ImageNet class를 sketch 스타일로 표현한 데이터셋 |

---

## 3. Why PACS First?

현재 실험에서 PACS를 먼저 사용한 이유는 다음과 같습니다.

| 이유 | 설명 |
|---|---|
| 도메인 레이블이 명확함 | 폴더 구조에 `photo`, `art_painting`, `cartoon`, `sketch`가 직접 반영되어 있음 |
| Domain generalization 표준 벤치마크 | domain shift 연구에서 널리 쓰이는 데이터셋 |
| 도메인 추정 정확도 측정에 적합 | 모델의 predicted domain과 ground-truth domain을 직접 비교 가능 |
| Start 단계 검증에 적합 | class classification 이전의 domain estimation module을 검증하기 좋음 |

현재 보고된 핵심 수치인 **MTA 미적용 94.64% → MTA 적용 97.91%**는 PACS 기반 domain estimation accuracy입니다.

---

## 4. PACS Domain Structure

| Domain | 시각적 특징 | 본 연구에서의 활용 |
|---|---|---|
| Photo | 실사, 자연 사진, 실제 색감 | 실사 기반 domain prompt 검증 |
| Art painting | 회화적 질감, 붓터치, 색채 변형 | sketch/cartoon과의 경계 검증 |
| Cartoon | 단순화된 형태, 채도 높은 색상, comic style | stylized domain prompt 검증 |
| Sketch | 흑백, 윤곽선, line art, 배경 단순 | prompt refinement 효과 검증 |

---

## 5. Domain-Specific Classification Datasets

최종 Zero-Shot class classification 평가에서는 domain-specific dataset도 고려합니다.

| Dataset | Task | Classes / 특징 |
|---|---|---|
| SUN397 | Scene classification | 397개 장면 분류 |
| Aircraft | Fine-grained aircraft classification | 항공기 기종 분류 |
| EuroSAT | Satellite image classification | 위성 이미지 기반 토지 분류 |
| StanfordCars | Fine-grained car classification | 자동차 모델 분류 |
| Food101 | Food classification | 음식 분류 |
| OxfordPets | Pet classification | 반려동물 품종 분류 |
| Flower102 | Flower classification | 꽃 종류 분류 |
| Caltech101 | Object classification | 일반 객체 분류 |
| DTD | Texture classification | 질감/텍스처 분류 |
| UCF101 | Action classification | 인간 행동 분류 |

---

## 6. Evaluation Plan by Dataset Group

| Dataset Group | Current Use | Future Use |
|---|---|---|
| PACS | Domain estimation accuracy 측정 완료 | 최종 class classification 성능 비교 |
| ImageNet variants | 연구 배경 및 domain shift benchmark | CLIP/TPT/DiffTPT 대비 성능 비교 |
| Domain-specific 10 datasets | 평가 계획 수립 | final zero-shot generalization 측정 |

---

## 7. Dataset Preparation Notes

현재 공개 저장소는 데이터셋 파일을 포함하지 않습니다. 대부분의 benchmark dataset은 라이선스와 용량 문제로 별도 다운로드가 필요합니다.

권장 구조 예시는 다음과 같습니다.

```text
data/
├── PACS/
│   ├── photo/
│   ├── art_painting/
│   ├── cartoon/
│   └── sketch/
├── ImageNet-R/
├── ImageNet-Sketch/
└── ...
```

실험 스크립트를 확장할 경우, 데이터 경로는 환경 변수 또는 config 파일로 분리하는 것을 권장합니다.

---

## 8. Future Dataset Extensions

향후 연구에서는 다음 확장을 고려할 수 있습니다.

- 의료 이미지 도메인별 분류 데이터셋
- 야간/비/안개 등 자율주행 weather shift 데이터셋
- 카메라/조명 변경이 포함된 산업 결함 이미지 데이터셋
- mixed-domain 이미지에 대한 multi-domain weight 평가용 데이터셋

이 확장은 본 연구가 단순 art-style domain shift를 넘어 실제 산업 환경의 domain shift에도 적용 가능한지 확인하는 데 도움이 됩니다.
