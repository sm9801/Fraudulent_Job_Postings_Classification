# 사기성 채용 공고 탐지 파이프라인 (Fraudulent Job Postings Classification Pipeline)

For English version, please click here: [Overview in English](https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/README%20(EN).md)

본 프로젝트는 사기성 채용 공고를 효과적으로 식별하기 위해 다양한 머신러닝 모델을 비교 및 평가하는 것을 목표로 합니다. Snowflake를 data streaming 및 data warehousing 플랫폼으로, Dataiku를 분석 플랫폼으로 활용하여 여러 모델을 실험하고 사기성 채용 공고를 식별하는 데 중요한 특성(feature)을 분석합니다.  
또한, 분류 성능에 영향을 미치는 모델 파라미터에 대한 이해를 심화하는 것을 목표로 합니다.

⚠️ 본 프로젝트는 2024년에 수행한 기존 프로젝트를 복구 및 개선한 버전입니다. 초기 개발 과정에서 Dataiku와 Snowflake 간의 플랫폼 레벨 이슈로 인해 학습된 모델 아티팩트, 주요 프로젝트 설정 값, 그리고 두 시스템 간의 streaming 연결 정보가 손실되는 문제가 발생했습니다.  
프로젝트를 중단하는 대신 이를 프로덕션 데이터 플랫폼과 시스템 안정성에 대한 이해를 강화하는 기회로 삼았습니다.

복구 과정에서 Snowflake 인프라를 수동으로 분리(disconnect)한 뒤, 데이터베이스, 웨어하우스, 역할(Role) 구조, 사용자 권한을 처음부터 다시 구성했습니다. 이후 해당 설정을 Dataiku에 재연결하고 모든 연결 파라미터를 보안 설정과 함께 재구성 및 검증했습니다.  
이 과정에서 Snowflake와 Dataiku 양측의 기술 전문가들과 협업하여 보안, 접근 제어, 시스템 안정성 측면에서의 모범 사례를 적용했습니다.  
플랫폼 복구 이후에는 프로젝트를 End-to-End로 재구축하며, 개선된 피처 엔지니어링, 평가 전략, 모델 비교 방식을 반영했습니다.

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [데이터셋](#데이터셋)
- [접근 방식](#접근-방식)
- [평가](#평가)
- [결과](#결과)
- [향후 개선 방향](#향후-개선-방향)

## 프로젝트 개요

본 데이터 처리 파이프라인은 채용 공고 데이터를 분석하여 사기 가능성을 예측하도록 설계되었습니다. 데이터셋에는 직무명, 지역, 기업 프로필 등 다양한 채용 공고 관련 정보가 포함되어 있습니다.  
먼저 지역 정보를 국가, 주(State), 도시 단위로 분리하여 지리적 분석의 정확도를 높였습니다. 또한 기업 소개, 직무 설명, 요구 사항, 복지 항목과 같은 텍스트 필드의 길이를 계산하여 채용 공고의 품질이나 신뢰도를 나타낼 수 있는 지표로 활용했습니다.

텍스트 데이터에는 정규화 및 단순화 과정을 적용하여 불필요한 변동성을 제거하고, 이후 모델링 단계에서의 성능 향상을 도모했습니다.

핵심 단계에서는 과거 데이터를 활용해 사기성 채용 공고를 예측하는 분류 모델을 학습하고, 테스트 데이터셋에 대해 평가 및 스코어링을 수행합니다.  
`test_scored`, `test_scored_2`, `test_scored_3`와 같은 결과 데이터셋에는 원본 채용 공고 정보와 함께 사기 확률 및 예측 결과가 추가로 포함됩니다.

이러한 결과는 기업 및 채용 플랫폼이 사기성 채용 공고를 사전에 탐지하고 대응하는 데 중요한 역할을 합니다. 확률 점수와 예측 결과를 제공함으로써 의사결정자가 선제적으로 조치를 취할 수 있으며, 이는 구직자를 보호하고 플랫폼의 신뢰도를 높이는 데 기여합니다.

## 데이터셋

본 프로젝트에서는 여러 온라인 소스로부터 수집된 샘플 데이터를 Snowflake 웨어하우스로 스트리밍하여 사용합니다.

**DISCLAIMER**  
본 프로젝트에 사용된 모든 데이터는 기밀성 보호를 위해 실제 데이터를 모방한 합성 데이터(synthetic data)입니다. 기업명, 급여 범위, 직무 설명 등 주요 속성은 수정 또는 비식별화 처리되었으며, 어떠한 기업의 독점적이거나 민감한 정보도 포함되어 있지 않습니다.

최종 데이터셋은 총 17,879건의 채용 공고와 19개의 원본 컬럼으로 구성되어 있으며 지역 정보, 기업 프로필, 급여 범위 등 다양한 속성을 포함합니다.  
피처 엔지니어링을 통해 다음과 같은 추가 지표를 생성했습니다.

- 중위 급여(median salary), 지역 세분화  
- 직무 설명 / 요구 사항 / 복지 / 기업 프로필 텍스트 길이  
- 최소 급여(minimum salary)

타깃 변수로는 `Fraudulent` 컬럼을 추가했으며, 총 27개 컬럼 중 26개 피처를 사용해 모델을 학습했습니다.  
각 채용 공고에 대해 사기 확률을 산출하고 이를 이진 값으로 변환하여 사기성 채용 공고를 식별하는 것이 목표입니다.

## 접근 방식

먼저 Snowflake 웨어하우스를 구축하고, S3에서 채용 공고 및 소득 데이터를 적재한 뒤 데이터셋을 조인하여 피처를 확장했습니다. 이후 Dataiku와의 연동을 위해 역할, 권한, 스테이지를 설정하여 보안이 적용된 분석 환경을 구성했습니다.  
이를 통해 Snowflake와 Dataiku 간의 원활한 연계를 기반으로 피처 엔지니어링, 모델 학습 및 평가를 수행할 수 있도록 했습니다.

<img width="668" height="89" alt="image" src="https://github.com/user-attachments/assets/172ba1dc-be3c-45e8-b451-4fe751a7d0f9" />

이후 데이터셋에 추가적인 예측 신호를 부여하기 위해 피처 엔지니어링을 수행하고, Dataiku의 내장 모델링 프레임워크를 활용해 다양한 분류 알고리즘을 평가했습니다.

총 9개의 모델을 학습 및 비교했으며 이는 의도적인 전략입니다. 사기성 채용 공고는 전체 데이터에서 소수 클래스이기 때문에 단순 정확도(accuracy)는 신뢰할 수 있는 지표가 아닙니다.  
따라서 정밀도(Precision), 재현율(Recall), F1-score 등 다양한 지표를 활용해 모델 간 trade-off를 분석했습니다.

연산 자원 제약으로 인해 초기 모델 학습은 80:20의 학습–테스트 분할을 사용했으며 성능이 우수한 모델을 선택하여 교차 검증을 통해 재학습할 것입니다.

![](https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Data%20Flow.png)

## 평가

- 학습 평가

<img title="Train Evaluation" width="2000" height="2000" alt="image" src="https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Train%20Summary.png" />

예상대로 모든 모델은 높은 정확도를 보였습니다. 이에 따라 본 프로젝트에서는 정밀도, 재현율, F1-score를 중심으로 평가를 진행했습니다.
재현율 기준으로는 Decision Tree 모델이 가장 높은 성능을 보였으나, 정밀도와 F1-score 간의 trade-off가 심각하여 최종 모델 선정에서는 제외하였습니다.
정밀도에 따라 LightGBM, XGBoost, SVM 모델이 가장 우수한 성능을 보였습니다.

- 검증 평가

<img title="Train Evaluation" width="3000" height="3000" alt="image" src="https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Test%20Summary.png" />

| 평가 기준 | XGBoost | LightGBM | SVM | 
|---|---|---|---|
| ROC AUC | 0.974 | 0.976 | 0.962 | 
| Accuracy | 0.951 | 0.959 | 0.951 |
| Precision | 0.929 | 0.971 | 0.938 |
| Recall | 0.534 | 0.589 | 0.525 | 
| F1-score | 0.678 | 0.733 | 0.673 |
| Cost Matrix Gain | 0.050 | 0.056 | 0.049 | 
| Lift | 2.478 | 2.456 | 2.427 | 
| Average Precision | 0.859 | 0.891 | 0.847 |
| Log Loss | 0.141 | 0.102 | 0.134 | 
| Calibration Loss | 0.052 | 0.015 | 0.030 |

모든 평가 지표에서 LightGBM은 XGBoost와 SVM 대비 전반적으로 더 우수한 성능을 보였습니다. 
이는 LightGBM이 지도 학습, 특히 이진 분류 문제에서 높은 성능을 발휘하는 알고리즘이라는 점에 기인합니다. 
이에 따라 LightGBM을 최종 모델로 선정하여 추가 분석을 진행했습니다.

## 결과

- 피처 중요도

![](https://github.com/sm9801/Fraudulent_Job_Postings_Classification/blob/master/Model%20Metrics/Feature%20Importance/CV%20LightGBM%20feature%20importance.png)

피처 중요도 분석 결과 기업 프로필, 회사 로고 유무, 국가, 산업군이 사기성 채용 공고 판단에 가장 중요한 요소로 나타났으며, 전체 중요도의 60% 이상을 차지했습니다.

## 향후 개선 방향

향후에는 스트레스 테스트, 하이퍼파라미터 최적화, 비용 민감 학습(cost-sensitive learning)을 통해 모델의 강건성을 강화할 계획입니다.  
장기적으로는 실시간 데이터 수집 및 모델 모니터링을 통합하여 프로덕션 환경에서의 지속적인 성능 평가를 가능하게 하고, Transformer 또는 LLM 기반 모델을 적용해 텍스트 이해 성능을 고도화할 예정입니다.
