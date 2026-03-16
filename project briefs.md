<a id="team-1"></a>
## Team 1 이사장님

| 항목 | 내용 |
|------|------|
| 프로젝트명 | Test-Time Prompt Tuning 기반 Cross-Sensor 도메인 적응을 통한 Vision-Language Model의 열대 저기압 분류 연구 |
| 서비스명(브랜드) | CyCLIP |
| 트랙 | 연구 |
| 팀명 | 이사장님 |
| 팀구성 | 설영은, 신지민, 윤희서 |
| 팀지도교수 | 황의원 교수님 |
| 무엇을 만들고자 하는가 | Test-Time Prompt Tuning(TPT)을 활용한 Cross-Sensor 도메인 적응 기반 Vision-Language Model(VLM) 열대 저기압 분류 모델을 개발한다. 위성 영상과 텍스트 정보를 함께 활용하는 멀티모달 모델을 기반으로 서로 다른 위성 센서(Himawari, GOES 등)에서 수집된 열대 저기압 데이터를 학습하고, 센서 환경이 달라져도 안정적인 분류 성능을 유지할 수 있는 기상 분석 AI 모델을 구축하는 것을 목표로 한다. 이를 통해 실제 다양한 위성 환경에서도 적용 가능한 일반화된 기상 영상 분석 모델을 개발한다. |
| 고객 (누구를 위해) | 본 연구는 기상 데이터 기반 AI 모델을 연구하는 연구자와 기상 서비스 및 기상 분석 시스템 개발자를 주요 대상으로 한다. 궁극적으로는 정확한 열대 저기압 정보를 필요로 하는 기상 기관, 재난 대응 시스템, 기상 데이터 분석 산업 등에서 활용될 수 있는 기술 기반을 제공하는 것을 목표로 한다. |
| Pain Point (해결할 문제) | 기상 및 기후 데이터는 위성 센서 종류, 해상도, 관측 방식 등의 차이로 인해 데이터 분포가 달라지는 domain gap 문제가 발생한다. 이로 인해 특정 센서 데이터로 학습된 모델은 새로운 센서 환경에서 domain shift가 발생하여 열대 저기압 분류와 같은 실제 응용 환경에서 성능 저하 문제가 발생한다. 특히 위성 영상과 텍스트 정보를 활용하는 멀티모달 모델의 경우 센서 차이, 데이터 수집 환경 차이, 지역별 관측 조건 차이 등으로 인해 모델의 일반화 성능이 제한되는 문제가 존재한다. 따라서 본 연구에서는 이러한 Cross-Sensor 환경에서 발생하는 문제를 해결하는 것을 핵심 목표로 한다. |
| 사용 기술 | 본 연구에서는 다음과 같은 기술을 활용한다. <br><br>- Vision-Language Model (CLIP 기반): 위성 이미지와 텍스트 정보를 함께 학습하는 멀티모달 모델<br>- Test-Time Prompt Tuning (TPT): 테스트 단계에서 프롬프트를 조정하여 새로운 도메인 환경에서도 성능을 향상시키는 기법<br>- Domain Adaptation / Cross-Sensor Learning: 서로 다른 위성 센서 데이터 간의 domain gap을 줄이는 기술<br>- Deep Learning Framework (PyTorch): 모델 학습 및 실험 환경 구축<br>- 기상 위성 데이터셋 활용: Himawari-8/9 TC Archive, TC PRIMED, IBTrACS 등<br><br>또한 CLIP zero-shot 모델을 베이스라인으로 설정하고, TPT 적용 모델과의 성능을 비교하여 Cross-Sensor 환경에서의 성능 개선 여부를 분석한다. |
| 기대 효과 | 본 연구를 통해 센서 환경 변화에도 강건한 기상 영상 분석 모델 개발, 열대 저기압 탐지 및 분류 정확도 향상, 새로운 위성 센서 환경에서도 추가 재학습 없이 활용 가능한 모델 제안과 같은 효과를 기대할 수 있다. 또한 본 연구에서 제안하는 멀티모달 도메인 적응 방법은 구름 분류, 강수 패턴 분석, 기상 현상 탐지 등 다양한 기상 및 기후 데이터 분석 문제로 확장될 수 있으며, 환경 데이터 분석 분야에서 멀티모달 AI 연구의 활용 가능성을 확대할 것으로 기대된다. |
| GitHub Repo | [https://github.com/chairwomans/chairwomans-capstone](https://github.com/chairwomans/chairwomans-capstone) |
| Team Ground Rule | [Team Ground Rule](https://github.com/chairwomans/chairwomans-capstone/blob/main/Team_Ground_Rule.md) |
| 최종수정일 | 2026-03-13 |
