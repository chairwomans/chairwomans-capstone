# 🔍 Multimodal domain adaptation

## 1. 연구 배경 및 필요성

- **문제 인식**: 테스트 이미지의 도메인(스케치, 회화, 위성사진 등)이 학습 도메인과 달라지는 domain shift 상황에서 CLIP과 같은 Vision-Language Model(VLM)의 이미지-텍스트 정렬이 어긋나 Zero-Shot 분류 성능이 저하되는 문제를 해결하고자 한다.
- **연구 목적**: 본 연구는 멀티모달 모델 기반 이미지 분류 시스템을 연구 및 개발하는 연구자와 ML 엔지니어를 주요 대상으로 하며, 궁극적으로는 별도의 fine-tuning 없이 다양한 도메인 환경에서도 정확하고 강건한 Zero-Shot 이미지 분류가 가능한 시스템 개발에 기여하는 것을 목표로 한다.

## 2. 연구 방법론

- **데이터/대상**
  - Domain Generalization 표준 벤치마크 (PACS)
  - ImageNet 계열 5종 (ImageNet, ImageNet-A, ImageNet-V2, ImageNet-R, ImageNet-Sketch)
  - 특정 도메인 10종 (SUN397, Aircraft, EuroSAT, StanfordCars, Food101, OxfordPets, Flower102, Caltech101, DTD, UCF101)
- **분석 방법**: MeanShift 기반 MTA (MeanShift for Test-Time Augmentation), Test-Time Domain Adaptation, 동적 텍스트·이미지 임베딩 재조합
- **핵심 가설**
  - 테스트 이미지의 도메인을 자동으로 추정하여 텍스트·이미지 임베딩을 동적으로 재조합하면 고정 평균 프롬프트 앙상블 방식보다 높은 Zero-Shot 분류 성능을 보일 것이다.
  - MeanShift 기반 MTA를 통해 outlier augmented view를 제거하면 보다 robust한 이미지 임베딩을 획득할 수 있을 것이다.
  - 도메인 가중치를 텍스트와 이미지 임베딩에 동시에 적용하면 멀티모달 정렬 품질이 향상되어 domain shift 환경에서의 분류 정확도가 개선될 것이다.

## 3. 기대 효과 및 활용 방안

- **학문적 기여**: 멀티모달 도메인 적응 문제를 test-time에서 해결하는 방법론을 제시함으로써 향후 다양한 domain shift 환경에서 활용 가능한 robust Vision-Language Model 개발에 기여할 수 있다.
