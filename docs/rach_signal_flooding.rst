Random Access Channel Flooding
==========================================================

Implementation (T-UE):
--------------------------
Initiate flooding on the UE side by:

- overriding srsRAN Random Access Channel Request function to send a large number or concurrent requests
- develop an environment with multiple UEs over UHD, where the results of the experiment can be seen in real time
- create an attack option in the GUI

Mitigation (gNB):
--------------------------
- Blacklisting UEs with excessive RACH requests

Attack Metrics:
----------------
- Possible throughput reduction of clean UEs on the network
- Disconnect of clean UEs
- gNB crash
