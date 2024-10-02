<<<<<<< HEAD
<<<<<<< HEAD
RACH Signal Flooding attack
=======
Random Access Channel Flooding
>>>>>>> 4196d37552bb0dd4264f2b7a3594da230898f4f8
=======
RACH Signal Flooding Attack
>>>>>>> 5ec96a2e963c0ad06db2e4921468af4e3c35120a
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
