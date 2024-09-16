Message Types
===============

RRC (Radio Resource Control)
------------------------------
- RRCSetupRequest: Sent by the UE to initiate the setup of an RRC connection.
- RRCSetup: Sent by the gNB to the UE to proceed with the RRC connection setup.
- RRCSetupComplete: Sent by the UE to the gNB to indicate that the RRC connection setup is complete.
- RRCConnectionReconfiguration: Sent by the gNB to modify an existing RRC connection (e.g., for handovers, bearer setup).
- RRCConnectionReconfigurationComplete: Sent by the UE to acknowledge the RRCConnectionReconfiguration message.
- RRCConnectionReconfigurationFailure: Sent by the UE to indicate that the reconfiguration failed.
- RRCConnectionRelease: Sent by the gNB to release an established RRC connection.
- RRCConnectionReleaseComplete: Sent by the UE to confirm the release of the RRC connection.
- RRCConnectionReject: Sent by the gNB to reject an RRC connection request.
- RRCConnectionSetupFailure: Sent by the UE to indicate that the setup process failed.

NAS (Non-Access Stratum)
---------------------------
- AttachRequest: Sent by the UE to attach to the network.
- AttachAccept: Sent by the core network to accept the attach request.
- AttachReject: Sent by the core network to reject the attach request.
- AuthenticationRequest: Sent by the core network to initiate authentication.
- AuthenticationResponse: Sent by the UE in response to the authentication request.
- SessionRequest: Sent by the UE to establish a session.
- SessionAccept: Sent by the core network to accept the session establishment.
- SessionReject: Sent by the core network to reject the session request.
- ServiceRequest: Sent by the UE to request a service (e.g., voice or data services).
- ServiceAccept: Sent by the core network to accept the service request.
- ServiceReject: Sent by the core network to reject the service request.
- BearerResourceCommand: Sent by the core network to modify bearer resources.
- BearerResourceModifyResponse: Sent by the UE in response to bearer resource modification.
- BearerResourceModifyRequest: Sent by the UE to request bearer resource modification.
- BearerResourceReleaseCommand: Sent by the core network to release bearer resources.
- BearerResourceReleaseResponse: Sent by the UE to acknowledge bearer resource release.

MAC (Medium Access Control)
--------------------------------
- Scheduling Request: Sent by the UE to request uplink resources.
- Downlink Control Information (DCI): Sent by the gNB to provide scheduling information for downlink/uplink data.
- Uplink Data: User data sent by the UE to the gNB.
- Downlink Data: User data sent by the gNB to the UE.

RLC (Radio Link Control)
-------------------------
- Data: Carries user and control data between the UE and the gNB.
- Status: Used for acknowledgment of received data or status reporting.

PDCP (Packet Data Convergence Protocol)
----------------------------------------
- Data: Carries user data between the UE and gNB, including security and header compression.
- Status Report: Reports on the status of data delivery.

Physical Layer Messages
------------------------
- PDCCH (Physical Downlink Control Channel): Carries control information for scheduling downlink/uplink resources.
- PDSCH (Physical Downlink Shared Channel): Carries user data in the downlink direction.
- PUCCH (Physical Uplink Control Channel): Carries control information in the uplink direction.
- PUSCH (Physical Uplink Shared Channel): Carries user data in the uplink direction.

Handover Messages
--------------------
- HandoverRequest: Sent by the target gNB to the source gNB to request handover information.
- HandoverRequestAcknowledge: Sent by the source gNB to the target gNB with the necessary handover information.
- HandoverCommand: Sent by the target gNB to the UE to initiate the handover process.
- HandoverPreparation: Sent by the UE to the target gNB to acknowledge the handover command.
- HandoverComplete: Sent by the UE to the target gNB to confirm successful handover.
