## Related Paper

Bhavithra, J., and Saradha, A. "Personalized web page recommendation using case-based clustering and weighted association rule mining." Cluster Computing, vol. 22, no. Suppl 3, 2019, pp. 6991-7002, https://doi.org/10.1007/s10586-018-2053-y

- Citations in Scopus : 20 (78th percentile)

- FWCI : 1.31

- Journal : *Cluster Computing, Vol* 22

### 1. **논문 선정 이유**

과거와 달리 유튜브나 넷플릭스 등을 통해서 일반 대중들에게도 사용자 맞춤 추천 시스템이라는 개념이 익숙해졌고, 이에 따라 추천 알고리즘의 중요성도 상승하였다고 생각한다. 특히 강의에서 연관 분석의 사례로 무선 인터넷 컨텐츠의 사용패턴 분석을 다루었는데, 관련 분야에서 최근의 발전된 추천 시스템은 어떠한 방식으로 이루어지는지 알아보고자 하였다. 
해당 논문에서는 웹 페이지 추천을 다루고 있어 인터넷 컨텐츠 추천과 유사한 주제이기도 하고, 강의에서 다룬 k-NN 기반 CBR / 연관 분석 / collaborative filtering을 모두 다루고 있기 때문에 수업 내용이 어떻게 활용될 수 있는지 확인할 수 있는 좋은 주제라고 판단하여 선정하였다.

### 2. **논문의 배경 및 주제**

이 논문은 추천 시스템에 CBR(Case-Based Reasoning)과 WARM(Weighted Association Rule Mining) 알고리즘을 적용하여 웹페이지 추천을 더 정확하게 하고 검색 속도를 빠르게 하기 위해 연구한 것이다. 

이 방법은 웹 사용자가 방문할 가능성이 있는 웹 페이지를 예측하고 제안함으로써 검색 지연을 줄이고, 사용자가 웹 검색에서 원하는 목적을 달성할 수 있도록 개인화된 추천을 제공하며, 이는 현재 활발히 연구되고 있는 분야 중 하나이다.

- **Data**

이 연구에서는 287명의 사용자가 엑세스한 7175개의 웹 페이지로 구성된 AOL(American On Line) 로그 데이터셋을 사용하였다. 데이터의 구성은 {AnonID, Query, Query Time, Item Rank, ClickURL}으로 되어 있으며, 개인 정보 보호를 위해 IP 주소 대신 익명 ID(AnonID)를 사용했다. 이 데이터는 50개의 레코드가 있는 7개 샘플로 구성되어 있다. Item Rank는 검색 결과에서 클릭한 항목의 순위를 나타내며, ClickURL은 클릭한 URL의 도메인 부분을 나타낸다.

![image](https://user-images.githubusercontent.com/59306720/232668991-3bab073e-67e0-4143-9b8f-630aedd441f9.png)

### 3. **논문의 Research Gap**

추천 시스템에는 Collaborative Filtering 방법과 kNN(K-Nearest Neighboring) 접근 방식을 주로 사용한다. 그 외에도 협업 필터링, 연관 규칙(AR), 클러스터링, 순차 패턴, 하이브리드 방법, 시맨틱 웹 등 다양한 전통적인 방법이 있다. Collaborative Filtering은 유사한 사용자를 찾아 추천하는 가장 일반적인 방법으로, Normal Recovery CF 등 이를 개선하는 방법도 연구되고 있다.

하지만 Collaborative Filtering과 kNN 방식은 몇 가지 단점이 있다. 예를 들어, 최근에 생성되거나 수정된 페이지는 업데이트 후 사용자가 방문하지 않을 수 있어서 추천이 제대로 이루어지지 않는 문제가 있다. 이를 콜드 스타트 문제라고 한다. 

논문에서는 이러한 문제를 해결하기 위해 CBR과 WARM을 결합한 새로운 알고리즘을 제안한다. CBR은 사용자 프로필을 생성하고 유사성 지식을 사용하여 현재 활성 사용자에 대한 관련 프로필을 예측하고, WARM은 기존의 연관 규칙과 유사하지만 트랜잭션 및 항목 집합의 중요성을 고려하여 더 효율적이다. 이 방법을 사용하면 개인화된 결과를 더 잘 제공할 수 있다.

### 4. **사용된 방법론**

- **Collaborative Filtering**
    
    Collaborative Filtering(CF)은 추천 시스템의 일종으로, 사용자가 제공한 명시적 또는 암시적 등급을 사용하여 항목에 대한 사용자의 관심을 예측한다. 이를 위해 등급 매트릭스를 사용하거나 항목-항목 행렬을 평가 매트릭스로 사용할 수 있다. 웹 로그 파일을 사용하여 사용자 프로필을 구성하고, 이를 기반으로 CF를 적용하여 유사 사용자에게 추천 항목을 제공할 수 있다. 
    
    Normal Recovery Collaborative Filtering(NRCF)는 웹 페이지 추천에 사용되는 CF 방식 중 하나로, 유사한 사용자가 방문한 웹 페이지를 추천하는 데 사용된다. NRCF에서 두 사용자 간의 유사도는 다음 식으로 계산된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669002-17d1be81-4e8f-449e-ba34-a75c9960a5e5.png)
    
    여기서 i는 사용자 u와 v가 공동 방문하는 웹 페이지 집합이다. |I| 는 i의 수, 즉 사용자 u와 v가 함께 방문한 웹 페이지의 총 수이다. r은 사용자 웹 페이지 매트릭스에서 각 사용자 u, v가 특정 웹 페이지에서 보낸 웹 페이지 키워드 및 시간의 값이다.
    
- **Case Based Reasoning**
    - **Feature selection**
    
    Case Based Reasoning(CBR)은 유사한 과거 문제의 솔루션을 기반으로 새로운 문제에 대한 솔루션을 찾는 프로세스이다. 사용자의 관심, 검색 패턴 및 웹 액세스 현상을 설명하는 다음과 같은 10가지 사용자 프로필을 생성했다.
    
    ▶ 페이지에 머문 시간(TOP), 사이트에 머문 시간(TOS), 이 페이지에 머문 평균 시간(ATP), 이탈률(BR), 종료율(ER), 전환율(CR), 방문자 수(NOV), 평균 페이지 순위(APR), 상위 유사 키워드(SK), 키워드 간 평균 유사성(ASM)
    
    이 시스템은 또한 아래 표와 같이 각 기능에 대한 1~2 사이의 가중치(β)를 사용하여 추천의 정확도를 높인다. 또한 글로벌 웹 사용자 집합에서 "k"명의 이웃을 필터링하여 최적화와 검색 정확도 증가 사이의 균형을 맞춘다. 값 "k"는 최적화와 검색 정확도 증가 사이의 균형을 맞추기 위해 추천 엔진에서 설정할 수 있는 임계값 수준이다. 
    
    ![image](https://user-images.githubusercontent.com/59306720/232669029-10eee466-fa60-4110-b0b2-0ebdaeefd45b.png)
    
    “k"명의 사용자 프로필을 분석한 후, 현재 활성 사용자의 프로필과 비교하는데, 선택된 10명의 "k" 사용자의 기능을 사용하여 유사도를 계산한다. 이후, 유사도가 일정 임계값 미만인 사용자 중 상위 "N"명의 프로필을 선택한다. 제안된 시스템에서는 이 임계값이 동적으로 설정되며, 다음과 같은 식을 사용한다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669063-2bdc0779-5cbe-4525-b925-cd13396e4f2f.png)
    
    ![image](https://user-images.githubusercontent.com/59306720/232669084-1f0672f2-9064-4322-9c5c-8e4cf1c8d478.png)
    
    - **Finding similarity score**
    
    k 개의 기존 사용자 프로필과 현재 활성 사용자의 유사성을 식별하여 가상 유사한 이웃을 필터링한다. 아래 식을 통해 가장 유사한 사용자를 선택한다. 이 결과는 WARM 알고리즘을 사용한 추가 분석에 사용된다. 
    
    ![image](https://user-images.githubusercontent.com/59306720/232669108-d77ece45-6e6f-4f5b-97b1-7bfed24c1a96.png)
    
- **WARM**
    - **Identifying frequent item set**
    
    추천 정확도를 높이기 위해 Weighted Association Rules Mining(WARM) 알고리즘을 사용하여 연관 규칙을 찾는다. 이를 위해 n-NN 이웃 사용자를 고려하고, 아래의 식을 통해 가중치를 계산하여 빈발 항목 집합(S)을 찾는다. 집합 S를 기반으로 연관 규칙이 생성되며, 쿼리 단어를 포함하는 웹 페이지 집합은 필터링 되어 S’로 표현된다. 또한 추천에 적합하지 않은 규칙을 제거하기 위해 각 규칙의 지지도 및 신뢰도 값이 계산된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669153-75143546-9338-44bc-80eb-8abc24f637fb.png)
    
    예를 들어, 방정식 {pi, pj, pk} ⇒ {pm}의 규칙은 "pi", "pj", "pk" 웹 페이지를 방문한 사용자는 어떤 순서로든 "pm" 웹 페이지를 방문할 가능성이 가장 높다는 것을 의미한다. 따라서 현재 활성 사용자에게 웹 페이지 "pm"을 추천하는 것이 가장 적절하다. 
    
    다음은 가중치, 지지도 및 신뢰도를 계산하는 식이다.
    
    - 가중치
        
        ![image](https://user-images.githubusercontent.com/59306720/232669181-35d02506-800c-4b46-b1b0-380016a8cbdf.png)
        
    - 지지도
        
        ![image](https://user-images.githubusercontent.com/59306720/232669209-409f330f-9df3-4c41-bcfc-b18eaaedc71d.png)
        
    - 신뢰도
        
        ![image](https://user-images.githubusercontent.com/59306720/232669233-239bf091-ce9c-4705-a367-4f7d7b3a4f5f.png)
        
    - **Generation of association rules**
    
    전체 규칙 생성 프로세스는 다음 그림과 같으며, 연관 규칙은 신뢰도 값에 따라 정렬되어 신뢰도가 높은 가장 적절한 규칙이 맨 위에 나열된다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669343-360cccc8-e672-475b-8284-005da3e953eb.png)
    
    - **Recommendation process**
    
    신뢰도 값을 기준으로 순위가 매겨진 상위 "m" 규칙이 추천 프로세스를 위해 선택되고, "m"은 웹 서버/검색 엔진에 의해 설정된다. 제안한 알고리즘의 정확도를 분석하기 위해 m 값을 30, 40, 50으로 다양하게 실험하였고, 각 "m" 규칙의 RHS는 최종 사용자에게 추천할 최종 웹 페이지로 선택된다.
    

### 5. **결론 (도출할 수 있는 의미)**

이 문서는 웹 페이지 추천 시스템에 대한 CBR / AR(WARM) 알고리즘을 제안하고, 이를 평가하기 위해 F1 Score, Miss Rate, Fall out Rate 및 Matthews correlation을 사용한다. CBR + WARM 알고리즘이 기존 알고리즘에 비해 더 좋은 성능을 보이며, 연산 속도에 대한 제안된 알고리즘 성능 평가를 위해 TP, TN, FP, FN의 4개의 값을 계산한 후 다음과 같은 성능 지표를 사용하였다.

- **F1 Score**
    
    정밀도 (Precision = TP / (TP + FP))와 재현율 (Recall = TP / (TP + FN))의 조화평균으로 계산되며, 0과 1 사이의 값을 가진다. 정밀도와 재현율이 모두 높을 경우 높은 값을 가지며 더 좋은 결과로 해석된다.
    
    F1 Score는 test sample의 수에 따라 CBR에 사용되는 k를 어떻게 설정하는 것이 유리한지 판단하기 위해 사용하였으며, sample의 수에 관계없이 k = 20~25의 값으로 설정하였을 때 가장 좋은 결과가 도출되었다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669409-6ba5c717-75e7-49f3-83d7-53f5c8ff0380.png)
    
- **Miss Rate**
    
    FN / (TP + FN)으로 계산된다. 값이 낮을수록 좋은 결과로 해석되며, 실제로는 관련이 있지만 관련이 없다고 분류한 데이터가 적다는 것을 의미한다. 
    
    ![image](https://user-images.githubusercontent.com/59306720/232669457-b09cbd35-16c4-4827-a5f3-ac8547cbdb06.png)
    
- **Fall out Rate**
    
    FP / (FP + TN)으로 계산된다. 값이 낮을수록 좋은 결과로 해석되며, 실제로는 관련이 없지만 관련이 있다고 분류한 데이터가 적다는 것을 의미한다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669518-1a898d1f-0d1c-4ce6-9c3d-bea4a9013cdc.png)
    
- **Matthews correlation (MC)**
    
    TP, TN, FP, FN으로 계산된다. -1과 1 사이의 값을 가지며, 1에 가까울수록 예측값과 실제 정답이 유사하다는 것을 의미한다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232669566-b53bf9a3-df5d-4375-b377-f6dd1a302c39.png)
    

해당 3개의 평가 지표는 논문에서 새롭게 제안한 CBR with WARM 알고리즘이 기존 알고리즘에 비해 개선된 성능을 보이는지 검증하기 위해 사용되었다.

Miss Rate와 Fall out Rate에서 모두 CBR + WARM 알고리즘이 가장 낮은 rate, 즉 가장 좋은 성능을 보여주었다. 특히 샘플의 종류에 관계없이 모든 표본에서 Rate : CF > CBR > CBR + WARM로 나타나 어떤 표본에서도 기존 CF 알고리즘에 비해 좋은 성능을 보임을 확인할 수 있다. 

Matthews correlation 그래프에서도 동일한 결과를 도출할 수 있다. 샘플에 관계없이 CF < CBR < CBR + WARM의 성능을 보였으며, 새롭게 제안한 알고리즘이 좋은 성능을 보인다는 것을 확인하였다.

### 6. **논문을 개선시킬 수 있는 점 / 아쉬운 점**

연구에서는 추천 프로세스의 정확도를 f1 score, mc score 등을 통해 평가하고 높였으며, 구체적인 k 값을 제시해 주었다. 그런데, 웹 페이지 추천 시스템은 그 특성상 빠른 연산이 필수적이지만 이 연구는 이 부분에 대한 평가가 이루어지지 않았다. 정확도 뿐 아니라 여러 알고리즘 간 결과 도출에 소요되는 시간에 대한 비교까지 이루어진다면 보다 그 실용성과 효용성이 극대화될 수 있겠다.
