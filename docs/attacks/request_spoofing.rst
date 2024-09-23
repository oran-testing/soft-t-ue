RRC Release Request Spoofing
==============================

Implementation (independent)
-------------------------------

- Listen for connected UEs on the network
- Decrypt incoming messages
- Use messages to construct a spoofed RRC setup Request
- Send the message to the gNB

Mitigation (UE and gNB)
------------------------

- Message validation
- Checksums
- Evaluating message source
- Unique timed based identifiers in messages

Attack Metrics
--------------

- UE disconnect
- gNB malfunction/crash