PDCP message Parroting Attack
==============================

Implementation (independent)
-------------------------------

- Capture user plane messages from the UE as a byte buffer
- Repeatedly send the same messages to the RAN at random intervals

Mitigation (UE and gNB)
------------------------

- Use of sequence numbers and timestamps in PDCP headers

Attack Metrics
--------------

- Corrupted channel data
- Loss of connection
- gNB crash
- Packet or data loss