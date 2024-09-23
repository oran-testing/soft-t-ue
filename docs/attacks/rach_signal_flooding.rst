RACH Signal Flooding Attack
==========================================================

Implementation (T-UE)
--------------------------
Initiate flooding on the UE side by:

- Overriding srsRAN Random Access Channel Request function to send a large number or concurrent requests
- Develop an environment with multiple UEs over UHD, where the results of the experiment can be seen in real time
- Create an attack option in the GUI

Mitigation (gNB)
--------------------------
- Blacklisting UEs with excessive RACH requests

Attack Metrics
----------------
- Possible throughput reduction of clean UEs on the network
- Disconnect of clean UEs
- gNB crash
