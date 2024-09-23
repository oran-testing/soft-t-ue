Random Access Channel Request Replay Attack
==========================================================

Implementation (UE):
--------------------------

- Capture the RACH requests of other UEs
- Replay these requests later to confuse the RAN

Mitigation (UE and gNB):
--------------------------
- add identifiers to RACH requests like timestamps or identifiers

Attack Metrics:
----------------
- Disconnected UEs
- Channel quality reduction
- gNB crash / malfunction
