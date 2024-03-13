## Related Paper

Asadi, Mohsen, et al. "A comparison of clustering algorithms for automatic modulation classification." 2019 International Conference on Robotics and Automation (ICRA). IEEE, 2019.

- Citations in Scopus : 32 (94th percentile)

- FWCI : 3.31

- Journal : Expert Systems with Applications

### 1. **논문 선정 이유**

최근 통신 시스템 및 군 통신 시스템에 대한 자동 변조 분류 (AMC)가 연구되고 있으며, 그 성능을 향상시키기 위해 DNN, RNN과 같은 다양한 인공지능 알고리즘이 연구되고 있음을 알고 있었다. 그러나 이 논문에서 ‘데이터마이닝’ 강의에서 배운 클러스터링 기법을 활용하여, 기존과 다른 방식으로 계산 복잡도를 낮추고 분류 정확도를 높일 수 있었다는 점이 흥미로웠다. 그 이유는, 정확도를 가진 채 빠른 연산이 AMC 분야에 적용되면 다음과 같은 이점을 얻을 수 있기 때문이다.     

자동 변조 분류 기술(AMC)은 인간의 개입 없이 자동으로 변조 방식을 감지하므로, 인력 비용을 줄일 수 있다. 신호 분류와 같은 작업은 전문적인 기술과 지식을 요구하므로, 이를 자동화할 수 있다는 것은 기술 역량이 떨어지는 지역에서도 무선 통신 기술을 사용할 수 있는 가능성을 높일 수 있다. 즉, 기술이 낙후된 지역까지 교통 등 무선 통신 기술을 응용한 기반을 구축할 수 있다.

수업 시간에 다룬 K-means Clustering, Hierarchical Clustering 등에서 나아가, 다양한 Clustering Analysis을 비교해 볼 뿐 아니라 이를 머신러닝 기반의 방법론들과 비교해 본 결과가 아주 흥미로웠다.

### 2. **논문의 배경 및 주제**

자동 변조 분류(Automatic Modulation Classification)는 사전 정보가 없는 신호가 어떠한 변조 방식을 사용하였는지를 판단하는 프로세스를 말한다. AMC는 민간 및 군용 응용 프로그램에서 주로 사용된다. 군용 프로그램에서는 변조 방식을 결정할 수 있으면 신호를 가로채서 복조할 수 있으며, 민간 통신 기술에도 인지 무선 등 다방면으로 적용이 가능하다.

이 논문에서는 K-means Clustering, Hierarchical Clustering, Fuzzy C-means Clustering 등 주요 군집 알고리즘이 자동 변조 분류에 적용될 수 있음을 보이고, 그 방법들을 비교 분석하였다. 이를 통해 좋은 성능을 보이는 알고리즘을 결합하여 새로운 AMC 방법을 제공한다. 이 새로운 방식과 기존에 AMC에서 사용하던 알고리즘을 비교함으로써, 클러스터링 방식의 효용성을 살펴보았다.

- **Data**

이 논문에서 사용된 샘플은 디지털 변조된 신호이다. 이 신호는 In-phase and Quadrature(I/Q) 평면 위에 나타낼 수 있는데, I/Q는 In-phase와 Quadrature-phase의 약자로, 각각 복소수평면에서, 복소수의 실수부와 허수부를 나타낸다.

▷ 참고

디지털 신호의 변조 - QAM / PSK 

**QAM**은 반송파 신호의 진폭과 위상 모두 독립적으로 변조된 디지털 신호이다. QAM은 케이블 모뎀 및 무선 LAN과 같은 고속 데이터 네트워크를 통해 디지털 신호를 전송하기 위한 널리 사용되는 변조 방식이다.

**PSK**에서는 반송파 신호의 위상만 변조된 디지털 신호이다. PSK는 간단하고 효율적인 변조 방식이며 Bluetooth, Wi-Fi 및 이동 통신 시스템과 같은 응용 프로그램에서 일반적으로 사용된다.

M-QAM, M-PSK의 **M**은 통신 채널을 통해 데이터를 전송하는 데 사용할 수 있는 가능한 진폭 및 위상 조합의 수를 나타낸다. M 값이 클수록 데이터 전송률이 높아지고 스펙트럼 효율성이 향상된다.

연구에서 사용한 디지털 신호는 MATLAB 환경에서 무작위로 비트 스트림을 생성한 후, AWGN 채널에서 8-PSK 또는 16-QAM 변조로 변조되었다. 이후 0.2dB의 크기로 각 SNR 레벨이 500번 반복되었다. 샘플 수는 1024, 2048, 4096 중 하나이며, 각 변조 방식은 M이 {2, 4, 8, 16, 32, 64, 128, 256} 중 하나인 M-QAM 또는 M-PSK이다.

위 방식으로 변조된 신호 샘플은 가산성 백색 가우시안 잡음(AWGN) 채널을 통해 수신되어 I/Q 평면에 표현되는데, 클러스터링 알고리즘을 통해 수신된 샘플의 변조 차수와 수준(M)을 추정하여 변조 방식을 식별한다.

### 3. **논문의 Research Gap**

기존에는 AMC 내에서 특정 목적을 위해 개별 클러스터링 알고리즘을 연구했다면, 이 연구는 AMC에 대한 다양한 클러스터링 알고리즘을 직접 비교했다. 구체적으로, AMC의 맥락에서 k-means, fuzzy c-means, DBSCAN, OPTICS와 같은 다양한 클러스터링 알고리즘을 비교하는데, 이들을 직접적으로 비교하는 연구는 이전에 수행된 적이 없다.

추가로, 비교를 통해 선정한 클러스터링 방식 기반의 AMC 방법을 새로이 제안하여 기존의 클러스터링 방식 외 AMC 알고리즘과 연산 속도, 분류 정확도를 비교했다. 기존의 AMC 알고리즘은 아래와 같다.

- The Maximum Likelihood Ratio Test (MLRT)
- The Kolmogorov Smirnov (KS) Test
- High order cumulants with a K-Nearest Neighbour (KNN) classifier
- High order moments with a KNN classifier

이 네 가지 기존 AMC 방법과 클러스터링을 활용하여 새로이 제시한 방법을 샘플 수와 SNR(신호 대 잡음 비)에 따라 비교함으로써, 상황에 맞게 어떠한 방식을 사용하는 것이 적합한지 알려주는 점이 기존 연구와의 큰 차별점이다.

참고로, 이미 병렬 컴퓨팅, 분산 처리 등 확장성과 실행 시간을 개선하기 위한 클러스터링 알고리즘이 연구되었다. 그러나, 연구에서 알고리즘 간 비교를 수행할 때에는 단일 스레드 성능에만 집중하여 객관적이고 명확한 비교를 수행했다.

### 4. **사용된 방법론**

이 연구에서 제안된 AMC 방법은 아래의 그림과 같이 Order Estimation, Final Clustering 및 Modulation Type Classification 단계로 구성된다.

-Order Estimation 단계에서는 생성된 I/Q 샘플에 클러스터링 알고리즘을 적용한 후 추정된 군집 수를 출력한다. 이는 추정된 변조 순서를 나타낸다.

-Final Clustering 단계에서는 I/Q 샘플에 클러스터링 알고리즘을 사용하여 이전 단계에서 결정된 클러스터 수로 클러스터링하여 클러스터 중심을 출력한다. 그런 다음 이러한 클러스터의 중심을 변조 유형 분류 단계에서 알려진 변조 방식의 별자리 표현과 비교하여 변조 유형을 결정한다.

-Modulation Type Classification 단계에서는 전 단계에서 출력된 클러스터의 중심을 기존에 알려진 변조 방식과 비교하여 변조 유형을 결정한다.

![image](https://user-images.githubusercontent.com/59306720/232177984-f0fcdfa4-f02b-4266-8df7-e62a1e9a2dd5.png)
Order Estimation, Final Clustering 각 단계에서 여러 클러스터링 기법을 비교해 보며, 가장 높은 분류 정확도와 짧은 계산 시간의 방식을 선정했다. 이들을 결합한 방식을 새로운 AMC로서 제시하여, “5.결론”에서 기존의 4가지 알고리즘과 성능을 비교한 것이다.

- **Order estimation stage**

이 연구의 제안된 방법에서 첫 번째 단계는 변조 순서를 추정하는 것이다. 예시로, 아래의 그림은 AWGN 채널을 통해 전송된 16-QAM 변조 방식의 수신 샘플의 I/Q 평면 표현을 보여준다. 이로부터 두 가지 관찰이 가능하다.

1. 수신된 기호는 쉽게 식별할 수 있는 특정 중심 주위에 흩어져 있다.
2. 중심의 수는 심볼 레벨이라고도 하는 변조 방식의 차수(M)에 해당한다. 예시에서, 16-QAM 변조 방식에서는 수신된 신호가 16개 포인트 주위에 클러스터링된다.

![image](https://user-images.githubusercontent.com/59306720/232177999-f51365eb-9d19-40e6-8bfc-220d466810ef.png)이 “클러스터링”을 진행할 때, 크게 아래 5가지 방식으로 CA를 적용했다.

1. **The elbow method : K-Means / K-Medoids / Fuzzy c-means**
    
    K-means와 K-medoids는 데이터 포인트와 할당된 클러스터 간의 총 거리 오차를 최소화하는 것을 목표로 한다. 그러나 k-medoids는 k-평균에서 사용하는 산술 평균 대신 클러스터의 중심으로 클러스터에 속하는 중간 데이터 또는 medoid를 사용한다. 이것은 데이터의 특이치에 대해 k-medoids를 더 견고하게 만들어준다. 반면에 Fuzzy c-means는 각 데이터를 단일 클러스터에 할당하는 대신 각 클러스터의 소속 정도를 할당한다. 클러스터를 명확하게 구분하기 어려운 경우에 유용하다.
    
    연구에서는 이 방식들에 elbow method를 사용하였다. elbow method는 k-means, k-medoids 또는 fuzzy c-means와 같은 known-order 클러스터링 알고리즘에 사용하여 가능한 변조 방식의 차수(M)를 결정할 수 있다. M에 따른 전체 거리 오차를 그래프에 함수로 그리면, 날카로운 팔꿈치가 형성되어 M을 특정할 수 있다. 각 클러스터 수마다 거리 오차가 이전 수에 대비하여 얼마나 변화되는지 백분율로 계산하고 가장 큰 백분율 차이를 보이는 위치가 팔꿈치의 위치, 즉 M이 된다.
    
2. **DBSCAN**
    
    ![image](https://user-images.githubusercontent.com/59306720/232178007-c54eae7a-b535-42b5-96ee-bd55ade0d39e.png)
    
    DBSCAN은 밀도 기반 군집화 아이디어를 기반으로 한, 변조 차수 추정에 사용할 수 있는 클러스터링 알고리즘이다. 즉, 서로의 근접성이 아니라 데이터 요소의 밀도를 기반으로 군집을 식별한다.
    
    DBSCAN 알고리즘에는 데이터 주변의 이웃 크기를 제어하는 엡실론(ϵ)과 클러스터를 형성하는 데 필요한 최소 포인트 수를 제어하는 MinPts의 두 가지 입력 매개변수가 필요하다.
    
    그림의 (a)와 (b)는 일부 ϵ와 MinPts 조합만이 올바른 클러스터 수를 제공함을 보여준다. 각 값을 조금씩 변화하며 이러한 올바른 MinPts와 ϵ의 영역을 결정한 후, 가능한 최대 클러스터 수를 클러스터 추정치로 사용한다.
    
3. **OPTICS**
    
    DBSCAN을 개선한 OPTICS는 밀도를 기반으로 데이터의 순서를 제공한다. OPTICS는 MinPts만 요구하여 변경되는 입력 매개변수에 대한 감도를 줄인 후, 후처리 단계에서 도달 가능성 거리(ϵ)를 선택할 수 있다. 최소 점 수는 DBSCAN과 동일한 방법으로 계산되며, 순서는 임계값보다 큰 피크 수를 세어 결정한다. 이 그림은 OPTICS를 사용하여 데이터 밀도를 기반으로 클러스터를 식별한 것이다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232178012-b3047d53-f6dd-4a05-9780-94f972c664e9.png)
    
4. **Hierarchical clustering**
    
    Hierarchical clustering은 데이터 간의 유사성을 기반으로 하는 군집화 알고리즘이다. 각 데이터는 단일 클러스터의 일부로 시작하여, 클러스터 사이의 거리에 따라 클러스터를 반복적으로 병합하거나 분할하여 클러스터 계층을 생성한다. 이 계층 구조는 일반적으로 덴드로그램으로 표시되며, 수직선은 군집 사이의 거리를 나타내고 수평선은 군집의 병합 또는 분할을 나타낸다. 클러스터 수는 덴드로그램으로부터 함수를 그린 후, 엘보우 방법 등으로 결정할 수 있다.
    
    ![image](https://user-images.githubusercontent.com/59306720/232178022-450526c5-e78e-4613-bf1c-9f03993971d3.png)
    
5. **Fuzzy c-means with fuzzy overlap**
    
    Fuzzy c-means with fuzzy overlap(FCMFO)은 Fuzzy c-means 알고리즘의 변형이지만 클러스터에 데이터 포인트 할당을 처리하는 방법이 다르다. FCMFO는 클러스터 간의 퍼지 중첩을 허용하여 클러스터가 겹칠 수 있으며, 데이터가 부분적으로 둘 이상의 클러스터에 동시에 속할 수 있다. 즉, FCMFO는 클러스터 간의 퍼지 중첩 가능성을 포함하여 데이터를 클러스터에 보다 유연하게 할당할 수 있다.
    

- **Final clustering stage**

밀도 기반 클러스터링 알고리즘은 일반적으로 클러스터의 중심점을 출력하지 않는다. 제안된 방법을 사용하려면 Final Clustering 단계에서 기호 수준을 추정하는 군집 중심이 필요하다. 따라서 이러한 밀도 기반 알고리즘에 대한 각 클러스터의 중심을 각 클러스터와 관련된 모든 포인트의 **평균 위치**로 계산한다.

Final Clustering 단계의 출력인 추정된 기호 수준은 다음의 Modulation Type Classification 단계로 공급된다.

- **Modulation type classification stage**

Modulation Type Classification 단계에서는 Final Clustering 단계의 예상 기호 수준과 기존에 알려진 변조 방식의 기호 수준(M)을 비교하여, 실제로 변조 방식을 판단한다. 아래 그림에서, 각 추정 기호 수준(X)과 가장 가까운 참조 기호 수준(O) 사이의 거리를 계산하여 총거리 오차에 대해 합산하고, 이 점수가 가장 낮은 변조 방식을 택한다.

![image](https://user-images.githubusercontent.com/59306720/232178027-bed60481-e413-4294-b649-84e96b145b01.png)

복잡성과 실행 시간을 낮게 유지하기 위해 간단하고 결정론적인 “최소 거리 분류기”를 사용했다.

### 5. **결론 (도출할 수 있는 의미)**

Order Estimation 단계에서 비교한 Clustering 방법은 K-means, K-medoids, Fuzzy c-means, DBSCAN, OPTICS, Hierarchical, Fuzzy overlap 등이 있으며, 비교 결과는 Table 1과 2에서 확인할 수 있다.

Table 1에서는 90%의 정확도를 달성하기 위해 각 Clustering 방법에서 필요한 SNR 값을 나타낸다. 이때 clustering의 정확도는 샘플과 클러스터 중심 사이의 거리의 합을 의미하는 거리 오차를 활용하여 계산하였다.

![image](https://user-images.githubusercontent.com/59306720/232178031-b1e03ace-84c0-468e-93d4-ac4cbc951fb1.png)

![image](https://user-images.githubusercontent.com/59306720/232178041-ee37a59c-b021-4367-9aea-98759bfce83b.png)

Table 2에서는 각 Clustering 방법론의 시간복잡도와 실제 소요 시간을 나타낸다.

![image](https://user-images.githubusercontent.com/59306720/232178043-5cb6f98e-8da1-4558-a5b7-f2eff8f0b0af.png)

표를 해석하면, 평가 결과 **DBSCAN**이 비교적 낮은 SNR 수준에서도 좋은 정확도를 보여준다. 그러나 O(nlogn)의 시간복잡도를 가지기 때문에 샘플 수가 커지면 소요되는 시간이 증가한다. 단순히 실행 시간만 고려하였을 때는 **Hierarchical**이 가장 빠른 시간에 결과를 도출한다. 그러나 정확도와 성능을 종합적으로 고려했을 때 **Elbow : K-means** 방법론이 좋은 성능을 보여준다.

Final Clustering 단계에서도 위의 Order Estimation 단계와 유사한 결과가 도출되었다. 즉, **k-means clustering** 방법론이 제안된다. 

이에 따라 각 k-means 클러스터링 기법을 활용한, 최종적으로 선택된 알고리즘의 성능을 샘플 수의 변화에 따라 비교하면 다음과 같은 그래프가 그려진다. 이는 SNR 값에 따라 필요한 최소 샘플 수가 달라짐을 의미한다.

![image](https://user-images.githubusercontent.com/59306720/232178048-a2ff098c-001a-4539-97b3-edced16f8a33.png)

선정된 Clustering 방법론을 기존에 사용되는 non-clustering 방법론들과 비교하였다. 이때 비교 대상으로 MLRT, KS test, Moment KNN, Cumulant KNN 등 총 4개의 방법론을 사용하였다.

![image](https://user-images.githubusercontent.com/59306720/232178054-a43e2c71-9422-403a-b159-1ca084b732e6.png)

모든 실험에서 공통적으로 SNR이 낮은 상황에서 Clustering 방법론의 정확도가 빠르게 떨어진다는 점을 확인할 수 있다. 

그러나 충분한 SNR 값에서는 100%의 성능을 보여준다. 특히 이 연구에서 제시한 해당 방법론은 기계학습에 의존하지 않고 임계값을 사전에 설정할 필요도 없으며, 시간 복잡도도 낮기 때문에 상황에 맞게 적절히 사용할 경우 기존 AMC 방법을 크게 개선할 수 있다는 장점이 있다.

### 6. **논문을 개선시킬 수 있는 점 / 아쉬운 점**

이 논문에서는 각 방식의 분류 정확도, 연산 속도를 단일 스레드 성능에만 초점을 맞추어 비교했다. 그러나, 이는 병렬 및 분산 처리가 사용되는 실제 프로그램에서 클러스터링 알고리즘의 전반적인 성능을 정확하게 나타내지 않을 수 있다. 즉, 보다 포괄적인 비교를 제공하기 위해 향후 연구에는 단일 스레드 성능 외에도 병렬 및 분산 처리 성능이 포함되어야 할 것이다.

이러한 보다 현실에 부합하는 성능 비교는, Order Estimation 단계와 Final Clustering 단계에서 선정되는 클러스터링 방식의 차이로 이어질 수 있으며, 이는 연구가 기존 결론과 다른 방향으로 진행될 수 있음을 의미한다.

