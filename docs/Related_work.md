## Related Works
- Shu et al., *Test-Time Prompt Tuning for Zero-Shot Generalization in Vision-Language Models*, NeurIPS 2022
- Khattak et al., *MaPLe: Multi-Modal Prompt Learning*, CVPR 2023
- Zanella et al., *On the Test-Time Zero-Shot Generalization of Vision-Language Models: Do We Really Need Prompt Learning?*, CVPR 2024

### Test-Time Prompt Tuning for Zero-Shot Generalization in Vision-Language Models
TPT는 단일 테스트 샘플만으로 추가 학습 데이터 없이 프롬프트를 적응적으로 튜닝하는 방법이다. 테스트 이미지의 다양한 augmented view를 생성한 뒤, 예측의 주변 엔트로피(marginal entropy)를 최소화하는 방향으로 프롬프트를 최적화한다. 이때 신뢰도가 낮은 augmented view는 confidence selection으로 필터링한다. ImageNet-A/V2/R/Sketch 등 자연 분포 변화 벤치마크에서 CLIP 대비 평균 3.6% 향상을 달성하며, 별도 훈련 데이터가 필요한 CoOp/CoCoOp과 동등한 수준의 성능을 보인다.
<br>
본 연구는 TPT와 마찬가지로 training-free test-time adaptation 방식을 취하지만, 프롬프트 파라미터를 직접 최적화하는 대신 테스트 이미지의 도메인을 추정하여 기존 CLIP 템플릿의 가중치를 동적으로 재조합하는 방식으로 작동한다. 따라서 역전파 없이도 도메인 shift에 대응할 수 있다는 점에서 차별화된다.

### MaPLe: Multi-Modal Prompt Learning
MaPLe는 텍스트 인코더에만 프롬프트를 적용하던 기존 방식(CoOp, CoCoOp)과 달리, 텍스트와 이미지 인코더 양쪽에 계층적 프롬프트를 학습하는 멀티모달 프롬프트 학습 방법이다. 핵심은 시각 프롬프트를 언어 프롬프트에 명시적으로 조건화하는 결합 함수(coupling function)로, 두 브랜치 간 상호 시너지를 유도한다. CoCoOp 대비 새로운 클래스 일반화에서 평균 3.45%, 조화 평균 기준 2.72% 향상을 달성하며, 학습 기반 방법 중 강력한 상한선(upper bound) 역할을 한다.
<br>
본 연구에서 MaPLe는 직접적인 비교 대상이 아닌 학습 기반 방법의 참조 성능(reference baseline) 으로 활용된다. 본 연구는 어떠한 파라미터 학습도 수행하지 않는 training-free 방식으로, 도메인 가중치를 동적으로 추정해 텍스트·이미지 임베딩을 재조합함으로써 MaPLe에 준하는 도메인 일반화 성능을 목표로 한다.

### On the Test-Time Zero-Shot Generalization of Vision-Language Models: Do We Really Need Prompt Learning?
MTA(MeanShift Test-time Augmentation)는 테스트 시 생성된 다수의 augmented view를 활용하여 이미지 임베딩의 분포에서 밀도 중심(mode)을 추정함으로써, outlier에 강건한 representation을 생성하는 방법이다. 기존의 단순 평균 기반 aggregation이나 prompt tuning 방식과 달리, 각 view에 대해 inlierness score를 도입하여 신뢰도 기반 가중치를 부여하고, 이를 MeanShift 최적화 과정에 통합함으로써 별도의 학습이나 임계값 설정 없이도 안정적인 성능 향상을 달성한다. 또한 텍스트 기반 예측 결과를 활용한 affinity를 통해 멀티모달 정보를 반영하며, 모델 내부 접근이나 gradient 계산이 필요 없는 training-free 구조이므로 black-box 환경에서도 적용 가능하다.
<br>
이러한 특징은 테스트 이미지의 도메인 정보를 반영하여 텍스트 임베딩을 동적으로 조정하는 본 연구와 상호 보완적으로 작용하며, 이미지 표현과 텍스트 표현을 동시에 개선하는 방향으로 결합될 수 있다.

<br><br>

## Distinctiveness
첫째, 도메인 추정을 하나의 독립적인 단계로 분리했다는 점에서 기존 접근과 구별된다. 기존의 prompt tuning 계열 방법들(CoOp, CoCoOp, TPT 등)은 모델이 학습 과정에서 자연스럽게 도메인에 적응하도록 유도할 뿐, 특정 입력이 어떤 도메인에 속하는지 모델이 명시적으로 판단하지 않는다. 반면 우리 연구에서는 이미지와 도메인 프롬프트 간 코사인 유사도를 계산하고, softmax를 통해 각 도메인에 대한 비율을 직접 산출한다. 이렇게 얻은 도메인 가중치는 이후 모든 단계에 영향을 미치는 기준으로 사용된다. 이 방식은 단순히 성능 향상을 넘어서, 모델이 어떤 근거로 판단했는지를 확인하고 조정할 수 있게 해주며, 문제를 “프롬프트를 잘 만드는 것”이 아니라 “상황에 맞게 선택하고 조합하는 것”으로 다시 정의한다는 점에서 의미가 있다.
<br><br>
둘째, 도메인 정보를 텍스트뿐 아니라 이미지 처리에도 함께 반영한다는 점에서 차별성이 있다. 대부분의 기존 연구(CoOp, CoCoOp, TPT, MTA 등)에서는 텍스트 표현만 조정하고 이미지 임베딩은 그대로 사용하는 경우가 일반적이다. 우리는 이 한계점에 주목하여 이미지 인코딩 과정 초반에 도메인 힌트를 반영하여, 특징 추출 자체가 특정 도메인 맥락을 고려하도록 만드는 방향을 떠올렸다. 텍스트와 이미지가 서로 다른 조건에서 생성된 표현이 아니라, 같은 맥락을 공유하는 상태에서 비교되는 것이다. 또한 서로 다른 차원의 임베딩을 선형 투영(linear projection)으로 정렬하여 이 구조를 유지한다는 점에서, 단순한 기법의 결합이 아니라 전체 파이프라인의 일관성을 우선하여 설계했다.
<br><br>
셋째, MTA를 단순히 성능을 높이기 위한 보조 기법(TPT의 confidence selection 등)으로 사용하는 것이 아니라, 전체 흐름의 출발점으로 활용한다. 다양한 augmentation으로부터 얻은 임베딩들 중에서 outlier를 제거하고 안정적인 표현을 먼저 확보한 뒤, 이를 바탕으로 도메인을 추정하고 이후 처리를 진행한다. 이렇게 하면 도메인 판단 자체가 더 신뢰할 수 있는 정보에 기반하게 되고, 그 결과 전체 과정의 안정성이 자연스럽게 확보된다. 중요한 점은 각 단계가 따로 작동하는 것이 아니라, 앞 단계의 결과가 뒤 단계의 품질을 직접적으로 좌우하는 구조를 가진다는 것이다.
<br><br>
결과적으로 우리 연구는 모델이 MTA 과정을 통해 확보한 안정적인 표현을 바탕으로 도메인을 명확히 인식하도록 하고, 그 정보를 이미지와 텍스트 양쪽에 동시에 반영하는 것을 목표로 한다. 처음부터 끝까지 일관된 흐름으로 연결되는 파이프라인을 만들 수 있다면, 기존 방법들이 학습에 기대서 얻던 성능을 구조적 설계만으로 따라잡을 수 있다고 생각한다.
