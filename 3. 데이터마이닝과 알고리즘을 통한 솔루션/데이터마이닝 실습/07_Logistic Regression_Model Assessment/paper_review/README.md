## Related Paper

Moon, Seung-Hyun, and Yong-Hyuk Kim. "An improved forecast of precipitation type using correlation-based feature selection and multinomial logistic regression." Atmospheric Research, vol. 240, 2020, 104928, https://doi.org/10.1016/j.atmosres.2020.104928
([https://www.sciencedirect.com/science/article/pii/S0169809519313092](https://www.sciencedirect.com/science/article/pii/S0169809519313092))

- Citations in Scopus : 28 (91th percentile)

- FWCI : 2.55

- Journal : Atmospheric Research 240(S1):104928

### 1. **논문 선정 이유**

정확한 강수 유형 예측은 기상 예보와 관련된 다양한 응용 분야에서 중요한 역할을 수행한다. 예를 들어, 농업, 수자원 관리, 도로 관리 면에서 작물의 수확 시기 조절, 수질 관리, 노면 관리 등 강수 유형에 따른 대응 전략을 수립하는 데 도움을 줄 수 있다. 

그런데, Practice HW를 진행하며 찾아본 기상 데이터에서 알게 된 점은 강수량 유형은 대부분의 기상 관측소에서 모니터링되지 않으며, 비와 눈 정도로만 분류되었다는 것이다. 심지어 이러한 데이터는 종종 사용할 수 없었다.

이 연구에서는 다항 로지스틱 회귀분석을 포함한 몇 가지 모델로 강수 유형을 비, 눈, 진눈깨비 3가지로 확장하여 더욱 정확한 강수 유형 예측을 시도했으며, 특히나 우리나라의 기상 데이터를 활용했기에 공유하고자 선정했다.

### 2. **논문의 배경 및 주제**

강수는 땅에 떨어지는 모든 형태의 응축된 대기 수중기를 말한다. 겨울에는 비, 눈, 진눈깨비같이 여러 형태로 떨어진다. 우리나라는 겨울이 아닌 계절에 강수량이 주로 비의 형태로 발생하기 때문에 강수량 예측의 정확도를 높이는 것은 어렵지 않다. 그러나 겨울에는 다양한 종류의 강우가 발생할 수 있어 정확한 예측이 어렵다. 

강수 유형에 따라 여러 사고가 발생할 수 있기 때문에 정확한 예측이 필요하다. 하지만 대부분의 기상 관측소에서 강수 유형 예측보다 강수 발생 시 정확한 강수량 분류에 더 많은 관심이 집중하고 있다. 

본 논문에서는 ECMWF(European Centre for Medium-Range Weather Forecasts)와 RDAPS(Regional Data Assimilation and Prediction System)에서 사용하는 단기 일기예보에 포함된 강수 유형을 예측에 사용하는 기상 변수를 활용했다. 이를 바탕으로 상관관계 기반 특징 선택을 사용하여 단기 일기 예보에서 사용할 수 있는 많은 날씨 변수의 효과적인 하위 집합을 조합하고, 다항 로지스틱 회귀분석을 통해 강수 유형 예측을 진행했다.

- **Data**
    
    이 연구에서는 ECMWF와 RDAPS에서 예측에 사용하는 기상 변수와 동일한 변수 세트를 사용한다. ECMWF 및 RDAPS 단기 일기 예보는 하루에 2번 발표되며, 최대 72시간 이후의 날씨를 3시간 간격으로 예측한다. 다음 표에 나열된 93개의 날씨 변수에는 온도, 풍속 및 상대 습도뿐만 아니라 우리가 개선하고자 하는 강수 유형의 예보(No.69)도 포함된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671517-2751ee9b-518f-48bb-a127-d3b3da7ccd67.png)
    
    ![image](https://user-images.githubusercontent.com/59306720/232671541-834a3da6-1d34-4ecd-b8ec-27d8d1684c2b.png)
    
    한국에서는 강수 유형을 780개의 관측소 중 그림에 표시된 22개의 지역에서만 기록한다. 연구에서는 2013년부터 2015년까지 한국의 해당 22개 지역에 대한 ECMWF 및 RDAPS의 단기 일기예보 데이터를 사용했다. [https://www.ecmwf.int/](https://www.ecmwf.int/)
    
    ![image](https://user-images.githubusercontent.com/59306720/232671555-bf1304fc-124d-49f1-86ac-41af1af28e09.png)
    
    기상청 데이터를 활용하여 각 위치의 위도, 경도, 고도, 월간 평균 기온의 범위, 각 유형별 발생 수를 연구에 사용하였다.
    
    - 'Non-winter'는 3월에서 11월을 의미하고 'Winter'는 12월에서 2월을 의미한다.
    - 유형별 발생 수는 2013년부터 2015년까지 3시간 간격으로 각 유형의 발생 여부를 관측하여 이를 종합한 값이다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671576-2b11f4af-e1fd-438a-8eb3-65ecacd48485.png)
    

### 3. **논문의 Research Gap**

기존에 로지스틱 회귀분석을 활용한 연구에서는 기온이나 습구 온도를 강수 유형 예측에 활용했으며, 강수를 비 또는 눈 2가지로만 예측했다.

본 연구에서는 강수 유형에 영향을 주는 기상량으로 상대습도, 풍속, 압력층의 두께 등을 추가하고, 강수 유형을 비, 눈, 진눈깨비 3가지로 확장하여 더욱 정확한 강수 유형 예측을 시도했다. 겨울에는 다양한 종류의 강우가 발생할 수 있어 기존 연구의 결과가 포함하지 못하는 부분이 있었기 때문이다.

이를 위해 상관 분석과 다항 로지스틱 회귀분석을 활용하였고, 기존 방법들과의 예측 결과 비교를 통해 성능을 검증하였다.

### 4. **사용된 방법론**

Correlation-based 변수 선택을 통한 기계 학습, 특히 다항 로지스틱 회귀를 사용하여 강수량 유형을 예측한다. 이후 정확도, Heidke score, Peirce score을 통해 모델을 평가한다.

- **Correlation-based feature select(CFS)**
    
    CFS는 좋은 기능 하위 집합에 클래스 레이블과 높은 상관관계가 있고 서로 거의 상관관계가 없는 기능이 포함되어 있다는 가설을 기반으로 한다. 주어진 기능의 하위 집합 S ⊆{ $X_1$, $X_2$, … , $X_m$}, 해당 하위 집합의 가치는 다음과 같이 표현된다. 
    
    ![image](https://user-images.githubusercontent.com/59306720/232671592-9a04712b-1390-4d8f-83e8-c9b9a80581a7.png)
    
    분자는 클래스 레이블을 예측하는 *S*의 능력을 측정하고, 분모는 선택한 기능 간에 중복되는 정보의 양을 측정한다. 가장 큰 장점을 가진 기능 하위 집합을 찾기 위해 CFS는 최고 우선 검색 알고리즘을 사용한다.
    
    참고로, U(A , B)는 다음과 같이 정의되는 두 확률 변수 A와 B의 대칭 불확실성이다. 대칭 불확실성은 상호 정보를 0과 1사이에 있도록 정규화한다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671614-1a297712-3293-459a-bb3e-dfaea7834a38.png)
    
- **Multinomial logistic regression**
    
    Y의 범주가 K개(K>2)일 때,  각각의 확률은 다음과 같이 나타낼 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671636-9be1dd2f-4568-423c-b298-c429d64c5e37.png)
    
    회귀 계수 $**b_k**$는 일반적으로 최대우도추정법으로 추정된다. 
    
    날씨 데이터의 관측값 x가 주어지면 다음과 같이 클래스 y가 계산된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671654-da451fe8-a7e9-4962-9aff-251a12663984.png)
    
- **Performance criteria**
    
    어떤 사건에 대한 예측 결과를 다음 표와 같이 나타낼 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671726-f5e2ac34-7380-4399-82a0-a679ee7fed5a.png)
    
    표를 기반으로, Heidke skill score (HSS)라는 평가 지표를 다음과 같이 정의한다. HSS는 예측이 우연히 맞을 확률을 고려하여 보정한 평가 지표로, 예측이 정확할수록 1에 가까워진다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671738-00122a7d-4133-486d-8307-acb3ba2a8ccb.png)
    
    여기서의 PC(proportion correct)와 E는 다음과 같이 정의된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671760-bf51655a-d39d-40d1-856c-439af0d84f94.png)
    
    ![image](https://user-images.githubusercontent.com/59306720/232671770-80fc67a9-d2d3-4bbc-9233-339dd74a9701.png)
    
    보조 평가지표로는 Peirce skill score(PSS)를 사용한다. 마찬가지로 예측이 정확할수록 1에 가까워지는 지표이며 다음과 같이 적중률(HR, 민감도)에서 오경보율(FAR, false positive rate)을 뺀 값으로 정의된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232671784-78cc22bf-85ad-457e-a055-c622d7dc0161.png)
    

### 5. **결론 (도출할 수 있는 의미)**

- **Experiment setup**
    
    2013년부터 2015년까지 한국 내 22개의 주요 위치에서 ECMWF와 RDAPS의 단기 일기예보 데이터를 사용하여 각종 강수 유형 예측 방법을 평가했다. ECMWF와 RDAPS 데이터에 대해 각각 별도로 3-fold 교차 검증 방법을 사용한 평가를 수행했다.
    
    성능 측정 지표로는 ECMWF와 RDAPS의 강수 유형을 사용했으며, 선행연구의 결과와 비교했다. 선행연구에서 사용된 Matsuo 스키마는 대한민국의 겨울 강수 유형을 기온, 상대습도 등의 기상 변수를 이용하여 예측하는 알고리즘이다.
    
    예측 모델로는 전처리 없이 진행한 다항 로지스틱 회귀분석과 PCA(주성분 분석) 전처리를 사용한 다항 로지스틱 회귀분석, 그리고 정보이론에서의 엔트로피 개념을 이용한 C 4.5 의사결정 나무 알고리즘을 사용했다. 
    
- **Analysis of feature selection**
    
    CFS를 활용해서 변수를 선택한 결과, Variables 64 (snow) 와 92 (the thickness of the 1000-700 hPa layer)는 모든 모델에서 선택되었고, 습도, 기온, 바람과 같은 변수들은 주로 선택되었다. 지역과 관련된 변수에서는 위도가 비교적 많이 선택되었다.
    
    RDAPS 데이터 세트에서는 강수량이 주로 선택되었으나, ECMWF에서는 잘 선택되지 않았다.
    
- **Comparative analysis**
    
    2013년부터 2015년까지 ECMWF와 RDAPS의 단거리 예보에 포함된 강수 유형 예측의 정확도는 비겨울에는 97% 이상, 겨울에는 약 70% 정도이다[.](https://www.sciencedirect.com/science/article/pii/S0169809519313092#t0030) 
    
    다항 로지스틱 회귀를 활용한 ECMWF 데이터를 사용한 겨울철 강수 유형 예측의 비교는 다음과 같다 
    
    (a) 정확도, (b) 비에 대한 HSS, (c) 눈에 대한 HSS, (d) 진눈깨비에 대한 HSS
    
    ![image](https://user-images.githubusercontent.com/59306720/232671827-4818ced8-216c-4b19-b59e-34337b21985e.png)
    

RDAPS 데이터를 이용한 다양한 다항 로지스틱 회귀 결과 비교는 다음과 같다.

![image](https://user-images.githubusercontent.com/59306720/232671851-21c15706-0402-40c5-b6d4-b6d7702533b7.png)

제안한 방법의 성능을 ECMWF 및 RDAPS 데이터와 비교한 결과는 아래 표와 같다.  Wilcoxon 부호 순위 테스트가 데이터 세트가 성능에 차이가 없다는 귀무 가설과 함께 모든 결과 쌍에 대해 수행되었다. 

![image](https://user-images.githubusercontent.com/59306720/232671868-1b193e87-3bcb-4f0b-ae83-07320f3f1d14.png)

따라서, 이 논문의 결론을 요약하면 아래와 같다.

▶ 진눈깨비는 ECMWF 데이터보다 RDAPS 데이터에서 더 잘 예측되었다. 또한 진눈깨비에 대한 HSS의 평균값이 다른 것들보다 훨씬 낮은 것을 확인할 수 있다.

▶ 강수량 예측 결과는 ECMWF 예측보다 15% 더 정확하고 RDAPS 예측보다 13% 더 나은 것으로 나타났다. 또한 한국 강수량 예보에 특화된 개선된 기존의 Matsuo 방식보다도 성능이 뛰어났다.

### 6. **논문을 개선시킬 수 있는 점 / 아쉬운 점**

이 논문에서는 날씨 예측에서 유용한 기상 변수를 선택하고, 다항 로지스틱 회귀분석을 이용하여 강수 유형을 예측하는 방법을 제안하였다. 그러나 각 유형에 대한 예측 성능 평가를 진행했을 때, 진눈깨비가 가장 낮은 점수를 받았는데, 이는 상대적으로 진눈깨비의 발생 빈도가 낮기 때문일 수 있다. 이를 개선하기 위해 언더 샘플링이나 오버 샘플링 기술을 고려해 볼 수 있다. 

또한 논문에서 제안한 방법은 관측 지역에 따라 성능 차이가 있을 수 있는데, 이를 명시하지 않은 부분이 아쉬웠다. 지역의 기후와 지형 등을 고려하여, 그 지역에 맞는 기상 변수를 선택한다면 더 좋은 예측을 할 수 있겠다.
