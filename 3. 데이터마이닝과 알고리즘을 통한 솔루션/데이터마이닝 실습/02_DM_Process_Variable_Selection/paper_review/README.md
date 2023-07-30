## Related Paper

Zhang, Yaojie, et al. “Forecasting Oil Price Volatility: Forecast Combination Versus Shrinkage Method.” *Energy Economics*, vol. 80, 2019, pp. 423–33, https://doi.org/10.1016/j.eneco.2019.01.010.

([https://www.sciencedirect.com/science/article/pii/S0140988319300258](https://www.sciencedirect.com/science/article/pii/S0140988319300258))

- Citations in Scopus : 94 (98th percentile)

- FWCI : 6.77

- Journal : Energy Economics

### 1. **논문 선정 이유**

가격 예측은 AI 기술이 발전함에 따라 계속해서 연구되는 분야이다. 본 논문에서는 원유 가격을 예측하는 모델들의 예측 성능을 비교한다. 그중에는 이번 주차에 배운 축소 추정 기법을 활용한 모델들도 있으며, 그 모델들의 성능이 우수하다는 결론을 내렸다. 

또한, 이 논문은 기존 가격 예측에서 활용된 프레임워크 아래에서 두 다른 방식을 사용했다. 이 때 가능한 후보군을 아주 다양하게 설정한 후정량적으로 평가하고, 견고성 검사 등을 추가로 수행했다는 점이 인상깊었다.

위 사항들을 고려하여, 이 논문을 통해 이번 주차의 내용을 더 깊게 공부해 보고자 했다.

### 2. **논문의 배경 및 주제**

- **Data**
    
    이 연구에서는 뉴욕상업거래소에서 거래되는 WTI 원유 선물의 근월물 계약에 대해 고주파 데이터를 사용한다. 당사의 고주파 원유 선물 가격 데이터는 Thomson Reuters Tick History Database([https://fsc.stevens.edu/tag/databases/](https://fsc.stevens.edu/tag/databases/))에서 확인할 수 있다.
    
    전체 샘플 기간은 2007년 1월 2일부터 2016년 7월 15일까지이다. 7거래 세션이 짧거나 거래가 너무 적은 날을 제거한 후 2,357개의 관찰을 얻었다. 샘플 외 예측을 생성하기 위해 전체 샘플 기간을 처음 1,457개의 관측치로 구성된 샘플 내 추정 기간과 나머지 900개의 관측치로 구성된 샘플 외 평가 기간으로 나눴다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259141-b1396801-d259-4541-830a-a7f0e8742999.png)
    

원유는 세계 경제에 결정적인 영향을 미치는 중요한 상품 중 하나이다. 또한 유가 변동성은 자산 가격 책정, 자산 배분 및 위험 관리의 핵심이다. 따라서 유가 변동성을 예측하는 작업에 주목하는 작업이 늘어나고 있다.

이 논문에서는 유가 변동성 예측을 위해 널리 사용되고 있는 HAR-RV 프레임워크에 대해 설명하고, 예측 조합과 축소 추정 기법을 사용하여 유가 변동성 예측을 시도한다. 이를 위해 다음 방법들을 사용하여 예측을 수행하고 그 결과를 비교한다. 

- **HAR-RV-type models**

- **Forecast combination**

- **Shrinkage methods (Elastic Net, Lasso)**

### 3. **논문의 Research Gap**

석유 선물 시장의 변동성을 예측하기 위해, “실현 변동성을 위한 이질적 자기회귀 모형(Heterogeneous AutoRegressive model for Realized Variance : HAR-RV)”을 사용한 기존 연구가 있다. 또한, Lasso와 HAR-RV의 프레임워크을 활용하여 석유 시장의 변동성을 예측한 기존의 연구가 존재한다. 하지만, 이 연구는 몇 가지 차이점을 통해 이 분야에 새로이 기여했다.

첫째, 기존 연구는 여러 개별 주식에 대한 실증 분석을 수행하는 반면, 이 논문은 원유 선물 시장에 초점을 맞추어 석유 선물 시장의 변동성을 예측에 있어 shrinkage method가 효과적임을 확인했다.

둘째, 기존 연구는 간단한 HAR-RV 모델에 의해 부과된 지연 구조가 Lasso에 의해 복구될 수 있는지 여부를 탐색한다. 그러나 이 논문은 원본 HAR-RV 모델뿐만 아니라 다양한 확장에서 모든 예측 변수를 수집하고 이러한 모든 예측 변수가 Lasso뿐만 아니라 Elastic Net에서도 효율적으로 사용될 수 있는지 조사했다.

세 번째로, HAR-RV 프레임워크에서 유가 변동성을 예측하는 데 어느 것이 더 신뢰할 수 있는지 forecast combination과 shrinkage method 간의 포괄적인 비교를 진행했다. 

마지막으로, 이 논문은 광범위한 견고성 검사와 DoC 테스트 등을 추가로 수행했다.먼저 모델 신뢰도(MCS) 테스트를 통해 Elastic Net과 Lasso의 축소 방법이 개별 HAR-RV 유형 모델뿐만 아니라 결합 접근법보다 훨씬 더 정확한 유가 변동성 예측을 보여줬다. “결론”의 Table 2를 참고하길 바란다.둘째, 수축 인자를 추정하는 데 사용되는 다양한 표본 크기, 서로 다른 표본 외 기간 및 기타 조합 접근법을 포함하여 광범위한 검사에서 강력하다.

![image](https://user-images.githubusercontent.com/59306720/229259160-1acee404-e341-4216-98d4-6f031f2cf55f.png)

![image](https://user-images.githubusercontent.com/59306720/229259167-49aa08d6-c380-4f36-bb43-9a7b115f52d2.png)

셋째, 변화 방향(DoC) 테스트는 Elastic net과 Lasso가 더 높은 방향 정확도를 갖는다는 증거를 제공한다. “결론”의 Table 7을 참고하길 바란다.

따라서 이 논문은 유가 변동성 예측에 관한 기존 문헌에서 나아가 shrinkage method가 forecast combination보다 일관되게 우수하다는 새로운 통찰력을 제공한다.

### 4. **사용된 방법론**

- **HAR-RV-type models**
    
    해당 논문에서는, HAR-RV 모형(Heterogeneous AutoRegressive model with Realized Volatility)을 사용하여 원유 가격 변동성을 예측한다. 이 모형은 일정 기간 동안 과거의 실현 변동성(realized volatility)을 사용하여 다음 기간의 변동성을 예측하는 모형으로, 기존의 ARCH나 GARCH와 같은 변동성 모형보다 예측 성능이 더 뛰어나다는 것이 알려져 있다. HAR-RV 모형은 또한 고빈도(high-frequency) 데이터에 적합하다는 장점이 있다.
    
    RV 모형은 일일 수익률의 제곱의 합의로 정의할 수 있다. 이때 샘플링의 빈도에 따라 일일, 주간, 월간 RV 등을 구할 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259181-2dda2da9-6ef0-4784-9b88-e7ae0aeab4a3.png)
    
    HAR-RV는 위의 일간, 주간, 월간 RV를 예측 변수로 활용하는 모델이며 다음과 같이 표현할 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259194-0b461ac7-eb1b-4a11-8122-4d006c6535b4.png)
    
    선행 연구에서 HAR-RV를 기반으로 하는 여러 확장 모델이 제시되었으며 본 논문에서는 그중에서 원형 HAR-RV를 포함한 총 8개의 모델을 사용, 비교 분석하였다.
    

- **Forecast combination**
    
    8가지의 HAR-RV 모델을 통해 8개의 개별적인 변동성 예측을 얻을 수 있다. 그러나 모형의 불확실성 때문에 개별 모형의 예측 성능이 불안정하다는 것이 잘 알려져 있기에 개별 모델이 생성한 예측에 의존하는 것은 너무 위험하다. 이를 감안하여, 선행 연구에서는 이 문제를 각종 조합 접근 방식을 사용하여 해결하였으며 그중 5가지 방법을 논문에서 채택하였다.
    
    통계적으로 조합 변동성 예측은 다음과 같이 계산할 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259199-da609971-188c-4d7c-a04b-7bf09ac6bfa1.png)
    
    RV는 유가 변동성의 조합 예측값을 나타내고, ω는 k번째 개별 예측의 결합 가중치를 나타낸다. 
    
    가중치를 구하는 방법을 달리하여 총 5가지의 조합 접근 방식을 사용하였다.
    
    - Mean combination : N개의 개별 예측의 등중 평균
    - Median combination : N개의 개별 예측의 중앙값을 사용
    - Trimmed mean combination : 최댓값, 최솟값을 제외한 나머지 개별 예측의 평균
    - Discount mean square prediction error (DMSPE) combining method : RV와 예측 RV 간의 오차 제곱합을 discount 요인 θ을 이용해 가중 계산한 것이다. θ의 경우에는 0.9와 1이라는 2가지 방식을 사용했다.
- **Shrinkage methods**
    
    이 논문에서는 Elastic Net과 Lasso와 같은 가장 인기 있는 축소 방법을 사용한다. 통계적으로, Lasso 방법을 사용하여 석유 가격 변동성 예측은 강의에서 다룬 바와 동일하게, 다음과 같이 추정된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259209-8f2d088b-c5f3-4544-8270-2b3ed53fbf7f.png)
    
    ![image](https://user-images.githubusercontent.com/59306720/229259214-d06f5a22-c383-45e6-acdd-6b14a5150e66.png)
    
    Elastic Net 방법을 사용하여 석유 가격 RV를 예측할 때에도 강의와 동일하게 다음과 같이 추정된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259221-a75fdec8-d6f8-4b35-8e8c-7113c81ce8b5.png)
    

- **Forecast evaluation**
    
    본 연구에서는 예측 모델들의 예측 능력을 양적으로 비교하고, 모델들 간의 통계적 성능 비교를 수행하는 두 단계를 거쳤다.
    
    이 논문에서 사용된 예측 모델들의 예측 능력을 양적으로 비교하기 위해, QLIKE, MSE 및 MAE의 세 가지 손실 함수를 사용한다. 특히 QLIKE와 MSE는 기존 연구에서 변동성 대리 변수의 노이즈 존재에 대해 강건함을 보였다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259230-e74a67b4-5018-4913-a94c-c041f01df8e5.png)
    
    ![image](https://user-images.githubusercontent.com/59306720/229259233-e092d865-c1c9-44aa-b1c8-6addd776aef6.png)
    
    ![image](https://user-images.githubusercontent.com/59306720/229259235-2a1bb867-a4b2-4b30-b85f-9364e6c9e50e.png)
    
    본 논문은 예측 모델들 간의 통계적인 성능 비교를 위해 모델 신뢰 구간 (MCS) 방법론을 사용한다. MCS는 일정한 신뢰 수준에서 최고의 모델을 포함하는 모델들의 하위 집합이다. MCS p-value의 해석은 고전적인 p-value의 해석과 유사하다.
    

### 5. **결론 (도출할 수 있는 의미)**

- **예측 결합 방법과 축소 방법 비교**
    
    기존 연구에서는 조합 예측이 일반적으로 개별 예측을 능가한다고 주장한다. table 2의 panel B 부분을 보면 실제로 조합 접근법이 일반적으로 더 높은 MCS p-value 값을 보여준다. 
    
    table 2의 pabal C에서는 조합 예측과 shrinkage method를 비교한 결과를 보여준다. Elastic Net이 항상 가장 큰 mcs p-value 값을 보여주며 일반적으로 Lasso가 Elastic Net 다음으로 큰 MCS-p value를 보여준다. 즉, 일반적으로 shrinkage method가 combination approaches보다 더 좋은 성능을 보여준다. 
    
    ![image](https://user-images.githubusercontent.com/59306720/229259239-1302192a-5aaa-4c41-8f50-b42d03b621c6.png)
    
    수축 방법이 조합 접근법보다 좋은 성능을 보여주는 이유는 bias-variance trade-off로 설명할 수 있다. Elastic Net 기법과 Lasso 기법은 약간의 편향이 발생하는 대신 예측 오차 분산을 줄여준다. 
    
    HAR-RV 모델과 Elastic Net, Lasso 모델을 모두 결합했을 때의 성능과 기존 모델들의 성능을 비교한 결과 새로운 모델이 기존의 조합 접근 방식보다는 뛰어난 성능을 보여주었지만, 여전히 Elastic Net / Lasso 모델의 성능에는 미치지 못하였다.
    
- **경제적 중요성**
    
    유가의 변동성 예측을 기반으로, 석유 시장의 투자자들이 리스크 관리와 포트폴리오 최적화 등의 작업을 할 수 있다. 이때 각 모델에 따른 포트폴리오 수익의 기댓값을 계산할 수 있다.
    
    단순한 HAR-RV 모델이 각종 확장 모델보다 일반적으로 더 좋은 기댓값을 도출한다는 특이점이 존재하지만, Elastic Net과 Lasso에는 미치지 못한다. 즉, 위의 결과와 마찬가지로 shrinkage method가 combination approaches보다 투자자들에게 더 높은 기대수익을 제공할 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/229259246-7828115e-ccbd-4261-a77c-ed78c309370e.png)
    

### 6. **논문을 개선시킬 수 있는 점 / 아쉬운 점**

원유 가격의 변동성을 설명하는 추가적인 변수를 이용하여 예측 성능을 더 향상시킬 수 있으리라 생각된다. 

이 논문에서 사용한 변수들은 “논문의 배경 및 주제” Table 1에서 확인할 수 있다. 그런데, 원유 가격을 예측하는 다른 논문*에서는 Table 1의 변수 이외의 다양한 변수를 제시하고 있다.

Zhang, Yaojie et al. “Forecasting crude oil prices with a large set of predictors: Can LASSO select powerful predictors?” *Journal of Empirical Finance* 54 (2019): 97-117.

원유 가격의 변동성 요인 : 국채 금리, 장기 수익률, 경제정책 불확실성, Kilian 지수, 원유 생산량 증가율, 원유 재고/수입 증가율 등

이러한 변수들은 석유 가격 예측에 중요한 영향을 미치는 것으로 알려져 있으며, 이를 이용하여 더 나은 예측을 수행할 수 있다.

이러한 변수들을 추가로 고려한 뒤, 데이터마이닝 교과목에서 배운 고전적인 변수 선택 방법과 Ridge, Lasso, Elastic Net 등의 축소 추정 기법을 활용하여 변수 선택을 진행하면 더 좋은 성능을 기대할 수 있겠다.
