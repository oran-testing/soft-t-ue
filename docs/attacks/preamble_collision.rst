Random Access User Equipment Preamble Collision
==========================================================

Implementation (UE):
--------------------------

- capture the preamble message of another UE
- send the capture preamble repeatedly to confuse the network
- repeat the process for every new UE connecting the the RAN

Mitigation (gNB):
------------------
- Once a UE sends the preamble attach, then invalidate that preamble so long as the UE is connected

Attack Metrics:
----------------
- Disconnected UEs
- Lowering of channel quality
- gNB crash / malfunction
