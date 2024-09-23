Preamble Collision Attack
==========================================================

Introduction
--------------
A Preamble Collision Attack targets the Random Access Procedure in LTE and 5G networks by deliberately causing preamble collisions during the Random Access Channel (RACH) process. In standard network operations, UEs (User Equipment) select a random preamble from a set of available options to initiate a connection with the base station. However, in a Preamble Collision Attack, an adversary repeatedly sends the same preamble as legitimate UEs, causing multiple devices to use the same preamble simultaneously. This leads to collisions, resulting in failed or delayed connection attempts, as the base station cannot differentiate between the colliding UEs. Such an attack can degrade network performance, particularly in high-load scenarios, and can be used to disrupt the normal operation of UEs within the coverage area.

**Summary:**

- Capture the preamble message of another UE.
- Send the captured preamble repeatedly to confuse the network.
- Repeat the process for every new UE connecting to the RAN.

Implementation
---------------------

- Simulate multiple UEs in srsRAN to perform a Preamble Collision Attack.
- Modify the ue.conf file in srsUE to set a specific preamble index instead of selecting one randomly.
- Deploy multiple instances of srsUE, ensuring all transmit the same preamble simultaneously.
- Run srsGNB to act as the base station and monitor the RACH procedure.
- Observe the RACH request logs to monitor preamble collisions.
- Analyze the collision rate to assess the attack’s impact on the network's ability to handle connection requests.

This test helps us understand the network's vulnerability to preamble collisions and assess potential countermeasures, such as dynamic preamble allocation or collision resolution strategies.

Mitigation (gNB)
------------------
- Once a UE sends the preamble attach, invalidate that preamble as long as the UE remains connected.

Attack Metrics
----------------
- Disconnected UEs
- Lowering of channel quality
- gNB crash / malfunction
