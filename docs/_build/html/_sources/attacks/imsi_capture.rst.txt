IMSI Catching Attack
==========================================================

Implementation (gNB)
--------------------------
Create a dummy gNB:

- configure the gNB to have a higher signal strength than the other
- configure the dummy gNB to send IMSI and other sensitive data to a server

Mitigation
------------
- Verify gNB identity
- Use encryption

Attack Metrics
----------------
- captured IMSIs
- disconnected UEs
- disrupted network function
