Signaling Storm Injection Attack
=====================================================

Implementation (UE Side)
--------------------------
1. **Custom Firmware/Software**: 
    - **Gain Acess**: Root or administrative access to modify UE firmware/software.
    - **Flood Signaling Messages**:
        - **Send High Volume**: Implement code to send a large number of signaling messages, such as attach requests, handover requests, or service requests, to the gNB.
        - **Simulate Overload**: Configure the UE to continuously generate and transmit signaling messages to simulate a signaling storm.

2. **Custom Application**:
   - **Develop & Deploy**: Create an application on the UE that periodically sends signaling messages at high frequencies.
   - **Testing**: Ensure the application can handle different types of signaling messages and adapt to varying network conditions.

3. **Monitoring Impact**:
   - **Network Response**: Observe how the gNB processes and manages the influx of signaling messages.
   - **Resource Utilization**: Assess the effect of signaling overload on the gNB’s processing capabilities and overall network performance.


Mitigation Components in srsRAN gNB
------------------------------------------------

Are there rate-limiting strategies in srsRAN gNB that can be under test?

Metrics to Assess the Attack
------------------------------
1. **Signaling Message Rate**:
    - **Rate Measurement**: Quantify the rate at which signaling messages are sent by the UE and received by the gNB.
    - **Volume Analysis**: Measure the total number of signaling messages received by the gNB over a specified period.

2. **Network Performance**:
    - **Impact on Throughput**: Assess changes in network throughput and overall performance due to the influx of signaling messages.
    - **Service Disruption**: Monitor any disruptions or delays in service availability for other UEs as a result of the signaling storm.

3. **Resource Utilization**:
    - **CPU and Memory Usage**: Track CPU and memory usage on the gNB to evaluate the effect of processing high volumes of signaling messages.
    - **Network Load**: Measure overall network load and resource consumption resulting from the signaling overload.

Papers
------
`https://dl.acm.org/doi/pdf/10.1145/2642687.2642688 <https://dl.acm.org/doi/pdf/10.1145/2642687.2642688>`_
