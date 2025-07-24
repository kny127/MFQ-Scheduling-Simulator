# MFQ-Scheduling-Simulator

Multi-level Feedback Queue (MFQ) 스케줄링 기법을 구현한 시뮬레이터입니다. 3개의 Ready Queue를 갖는 MFQ 스케줄링 기법 구현이 구현되었으며, Gantt Chart 및 성능 지표 계산 결과가 출력됩니다.   
이때, 아래의 고려사항/가정을 따릅니다.
+ 동시 도착 처리: 여러 프로세스가 RQ0에 같은 시각에 도착할 경우, PID 오름차순 순서로 RQ0에 삽입
+ SPN 동일 우선순위: Q2에서 Burst Time이 동일한 프로세스가 여러 개일 경우, PID 오름차순 순서로 실행
+ 입력 형식: 각 프로세스의 PID가 1부터 연속된 오름차순 순서로 주어진다고 가정

## Queue 구성
1. Q0: Round Robin (Time Quantum = 2)

2. Q1: Round Robin (Time Quantum = 4)

3. Q2: Shortest Process Next (SPN)

우선순위 : Q0 > Q1 > Q2 순으로 높은 우선순위를 가집니다.

동작 원리 :
  * 모든 프로세스는 최초에 Q0으로 진입
  * Qi에서 time quantum을 모두 소모하면 Qi+1로 이동
  * Q2에서는 SPN 스케줄링 적용 (Q2 진입 시점의 남은 burst time 기준)

## 입력 형식
>number of Processes
>
>PID1 Arrival_Time1 Burst_Time1
>
>PID2 Arrival_Time2 Burst_Time2
>
>...

### 입력 예시 (input.txt)
>3   
>1 0 2   
>2 0 2   
>3 5 3

## 출력 형식
### Gantt Chart
* [-P1(3)---] 형식으로 표시
* 괄호 안 숫자는 실행 시간, P 뒤 숫자는 PID
* [-0(1)-]는 1초 동안 CPU가 아무 프로세스도 실행하지 않음을 의미

### 성능 지표
* 각 프로세스별 지표:
  P1 => TT=4, WT=2 형식으로 출력
  + Turnaround Time (TT)
  + Waiting Time (WT)
* 전체 평균:
  + Average TT = X.XX
  + Average WT = X.XX
 
### 출력 예시
>=== Gantt Chart ===   
>[-P1(2)--][-P2(2)--][-P1(1)-][-P3(3)---]   
>    
>=== 각 프로세스 TT, WT ===   
>P1 => TT=4, WT=2   
>P2 => TT=4, WT=2   
>P3 => TT=3, WT=0   
>   
>Average TT = 3.67, Average WT = 1.33   
