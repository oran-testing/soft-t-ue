CQI Manipulation Attack
=====================================================

Implementation (UE Side)
--------------------------
- **Override CQI**: Implement code to consistently send high CQI values

- **Monitoring Impact**:
   - **Measure Throughput**: Track throughput and bandwidth allocated to the UE
   - **Assess Network Impact**: Evaluate the effects on other users and overall network performance

Mitigation Components in srsRAN gNB under Test
------------------------------------------------
1. **Proportional Fair Scheduling (PFS)**:
    - **Balance Allocation**: Distributes resources considering both channel quality and historical throughput
    - **Limit Impact**: Adjusts allocation based on actual performance to mitigate exaggerated CQI effects

2. **CQI Reporting and Filtering**:
    - **Thresholds**: Applies thresholds to filter out unrealistic CQI values
    - **Configuration**: Configurable to detect and handle abnormal CQI reports

3. **Quality of Service (QoS) Management**:
    - **Prioritization**: Enforces QoS policies to ensure service needs are met, mitigating bandwidth hogging
    - **Resource Allocation**: Allocates resources based on QoS requirements

4. **Resource Allocation Limits**:
    - **Maximum Limits**: Configures resource limits to prevent excessive bandwidth use by any single UE
    - **Rate Limiting**: Implements rate limiting to ensure fair resource distribution

Metrics to Assess the Attack
------------------------------
1. **Bandwidth Utilization**:
    - **Throughput Measurement**: Quantify throughput allocated to the modified UE
    - **Bandwidth Consumption**: Track the percentage of total network bandwidth used by the UE

2. **Network Performance**:
    - **Impact on Other Users**: Monitor changes in service quality (e.g., throughput, latency) for other UEs
    - **Error Rates**: Observe increases in error rates or retransmissions due to congestion

3. **Network Load**:
    - **Resource Allocation Metrics**: Measure resource usage by the attacking UE compared to others
    - **System Performance**: Assess the impact on network CPU and memory usage due to increased load

Notes
------
- **Development Branch**: `cqi_attack_development <https://github.com/oran-testing/soft-t-ue/tree/cqi_attack_development>`_

