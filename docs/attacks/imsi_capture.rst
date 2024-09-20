<<<<<<< HEAD
IMSI Catching Attack
=======
International Mobile Subscriber Identity Catching Attack
>>>>>>> 4196d37552bb0dd4264f2b7a3594da230898f4f8
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
