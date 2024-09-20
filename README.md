# NTIA Software Tester UE

Penetration Testing Tool for Software Defined Radio

## Overview

This project is a security testing tool based on srsRAN Project's User Equipment, used to test 5G and open radio access networks (RANs) via the Uu air interface between the UE and the network. While this enables different types of testing, the focus of the software is on RAN security testing. This soft T-UE is fully software-defined and compatible with widely available, commercial off-the-shelf software radio hardware. Standardized 3GPP or O-RAN tests as well as custom test procedures can then be implemented and executed at minimal cost and at different stages of RAN development and integration. This system allows for testing many commercial and open source random access networks with minimal technical overhead. Many attacks on the RAN can be run automatically by the system.

- [UE Documentation](https://github.com/oran-testing/soft-t-ue/blob/main/docs/UE.md)
- [gNB Documentation](https://github.com/oran-testing/soft-t-ue/blob/main/docs/gNB.md)
- [Attack Documentation](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks) 

**NOTE: This system is designed to run on ubuntu and is tested on ubuntu 20.04**

## Installation

If testing with ZMQ one machine can be used. If using an RU run with two machines A and B.

To install the UE run (Machine A):
``` bash
sudo ./scripts/install-ue.sh
```

To install the gNB run (Machine B):
``` bash
sudo ./scripts/install-open5gs.sh
sudo ./scripts/install-gnb.sh
```
## Running

To start the gNB daemon (Machine B):
``` bash
sudo systemctl daemon-reload
sudo systemctl start gnb-controller.service
```

To run the GUI (Machine A):
``` bash
cd controller/ue
python3 main.py
```

## System Architecture
![Soft-T-UE-System.png](https://github.com/oran-testing/soft-t-ue/blob/grafana_integration/docs/images/Soft-T-UE-System.png)
