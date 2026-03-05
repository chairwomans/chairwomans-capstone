# ☁️ Multimodal domain adaptation

## 1. 연구 배경 및 필요성
- **문제 인식**: 지역, 센서, 데이터 수집 환경이 달라질 때 발생하는 기상 데이터 분포 차이로 인해 모델 성능이 떨어지는 문제를 해결하고자 함
- **연구 목적**: 본 연구는 기상 데이터 기반 예측 모델을 연구 및 개발하는 연구자와 기상 서비스 개발자를 주요 대상으로 하며, 궁극적으로는 정확하고 신뢰성 높은 날씨 예측 정보를 필요로 하는 일반 사용자 및 산업 분야에 기여하는 것을 목표로 한다.: 

## 2. 연구 방법론
- **데이터/대상**
  - Satellite imagery
  - Weather radar data
  - Numerical Weather Prediction (NWP) variables
  - Surface station observations
- **분석 방법**: Multimodal Feature Encoder, Feature Fusion, Domain Adaptation
- **핵심 가설**
  - Multimodal representation learning은 단일 modality 모델보다 높은 일반화 성능을 보일 것이다.
  - Domain adaptation을 적용한 모델은 새로운 지역 또는 센서 환경에서도 성능 저하가 적을 것이다.
  - Feature-level alignment를 통해 domain-invariant representation을 학습할 수 있다.

## 3. 기대 효과 및 활용 방안
- **학문적 기여**: 기상 데이터의 도메인 간 분포 차이 문제를 해결하는 방법론을 제시함으로써 향후 다양한 환경에서 활용 가능한 robust weather prediction models 개발에 기여할 수 있다.
