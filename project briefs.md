## Team 1 이사장님

| 항목 | 내용 |
|------|------|
| 프로젝트명 | 테스트 이미지의 도메인을 자동으로 파악해 텍스트와 이미지 임베딩을 동적으로 재조합함으로써 도메인 변화에도 정확한 CLIP 기반 Zero-Shot 이미지 분류 연구 |
| 서비스명(브랜드) | DoFit |
| 트랙 | 연구 |
| 팀명 | 이사장님 |
| 팀구성 | 설영은, 신지민, 윤희서 |
| 팀지도교수 | 황의원 교수님 |
| 무엇을 만들고자 하는가 | CLIP(Contrastive Language–Image Pre-training)은 이미지와 텍스트를 함께 이해하는 멀티모달 AI 모델인데, 기존 방식은 스케치든 실사(이를 domain shift라고 봄) 사진이든 똑같은 클래스 대표 벡터로 판단해서 domain shift 상황에서 성능이 떨어지는 경우가 많다. 따라서 테스트 이미지가 들어오는 순간 "아 이건 ~~한 도메인이네"를 자동으로 파악하고, 그 도메인에 맞게 텍스트·이미지 임베딩을 동적으로 재조합하는 test-time domain adaptation 시스템을 만들고자 한다. |
| 고객 (누구를 위해) | 스케치, 회화, 위성사진, 의료 이미지처럼 학습 데이터와 도메인이 다른(domain shift가 발생하는) 이미지를 분류해야 하는데, 매번 새로 fine-tuning하기엔 데이터도 없고 비용도 부담스러운 연구자 및 ML 엔지니어 |
| Pain Point (해결할 문제) | 멀티모달 데이터는 도메인 차이(domain shift)가 발생하면 테스트 성능이 크게 저하된다. 특히 CLIP과 같은 Vision-Language Model(VLM)은 Zero-Shot downstream task 환경에서 학습 도메인과 테스트 도메인이 달라지는 순간 이미지-텍스트 간 정렬이 어긋나 분류 성능이 떨어진다. 기존의 멀티모달 도메인 적응(domain adaptation) 방식은 추가 학습 데이터나 fine-tuning이 필요해 비효율적이고 성능 향상도 제한적이다. 이를 해결하기 위해 별도의 재학습 없이 테스트 시점에서만 도메인을 자동으로 감지하고 적응하는 Test-Time Domain Adaptation 방식이 필요하다. |
| 사용 기술 | 본 연구에서는 다음과 같은 기술을 활용한다. <br><br>- Vision-Language Model (CLIP 기반): 이미지와 텍스트 정보를 함께 이해하는 멀티모달 모델<br>- MeanShift 기반 MTA (MeanShift for Test-Time Augmentation): 테스트 단계에서 augmented view들의 outlier를 자동 제거하고 robust한 이미지 임베딩을 획득하는 기법<br>- Test-Time Domain Adaptation: 테스트 단계에서 이미지의 도메인을 자동 추정하여 텍스트·이미지 임베딩을 동적으로 재조합하는 기법<br>- Stable Diffusion V2: 테스트 이미지로부터 다양한 augmented view를 생성하는 이미지 증강 모델<br>- Deep Learning Framework (PyTorch): 모델 학습 및 실험 환경 구축<br><br>또한 기존 CLIP의 고정 평균 프롬프트 앙상블을 베이스라인으로 설정하고, 도메인 가중 동적 임베딩 재조합 방식과의 성능을 비교하여 domain shift 환경에서의 성능 개선 여부를 분석한다. |
| 개발환경 | 1. Client 디바이스: PC(Windows, Mac) 및 GPU 서버 기반 연구 환경<br>2. 딥러닝 프레임워크: Python/PyTorch/CUDA 기반 GPU 환경<br>3. 데이터셋: ImageNet 계열 5종(ImageNet, ImageNet-A, ImageNet-V2, ImageNet-R, ImageNet-Sketch) + 특정 도메인 10종(SUN397, Aircraft, EuroSAT, StanfordCars, Food101, OxfordPets, Flower102, Caltech101, DTD, UCF101)<br>4. 활용 모델: CLIP 기반 Vision-Language Model<br>5. 사전학습 모델: CLIP pretrained model (ViT 기반)<br>6. 라이브러리: NumPy, Pandas, Matplotlib, TensorBoard 등<br>7. 이미지 증강: Stable Diffusion V2, RandomCrop |
| 사용하는 소프트웨어 URL | 1. CLIP 공식 코드베이스: https://github.com/openai/CLIP<br>2. DiffTPT 코드베이스: https://github.com/chunmeifeng/DiffTPT<br>3. MTA 코드베이스: https://github.com/MaxZanella/MTA<br>4. ImageNet 데이터셋: [https://www.image-net.org](https://www.image-net.org/)<br>5. HuggingFace (사전학습 모델 허브): [https://huggingface.co](https://huggingface.co/) |
| 기대 효과 | 본 연구를 통해 domain shift 환경에서도 강건한 이미지 분류 모델 개발, Zero-Shot 분류 정확도 향상, 새로운 도메인 환경에서도 추가 fine-tuning 없이 활용 가능한 모델 제안과 같은 효과를 기대할 수 있다. 또한 본 연구에서 제안하는 test-time domain adaptation 방법론은 멀티모달 모델의 domain shift 문제를 다루는 다양한 downstream task로 확장될 수 있으며, 데이터 확보가 어려운 특수 도메인 분야에서 멀티모달 AI 연구의 활용 가능성을 확대할 것으로 기대된다. |
| GitHub Repo | [https://github.com/chairwomans/chairwomans-capstone](https://github.com/chairwomans/chairwomans-capstone) |
| Team Ground Rule | [Team Ground Rule](https://github.com/chairwomans/chairwomans-capstone/blob/main/Team_Ground_Rule.md) |
| 최종수정일 | 2026-04-14 |
