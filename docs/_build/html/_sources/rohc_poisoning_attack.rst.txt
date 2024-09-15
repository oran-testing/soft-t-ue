Robust Header Compression Poisoning Attack
==========================================================

Implementation (UE):
---------------------
- Generate messages with constantly changing and lengthy packet headers.
- Create high entropy in packet metadata.
- Send a high volume of corrupted packets to the RAN.


Mitigation (UE and gNB):
---------------------------
- Improve the RoHC algorithm or implement anomaly detection.


Attack Metrics:
----------------
- Disconnected UEs
- Reduced channel quality
- gNB crash/malfunction
- Increased packet latency
