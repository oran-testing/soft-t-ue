# NTIA Software Tester

An SDR security testing UE based on srsRAN's UE.

## Overview

This project is a security testing tool based on srsRAN Project's User Equipment, used to test 5G and open radio access networks (RANs) via the Uu air interface between the UE and the network. While this enables different types of testing, the focus of the software is on RAN security testing. This soft T-UE is fully software-defined and compatible with widely available, commercial off-the-shelf software radio hardware. Standardized 3GPP or O-RAN tests as well as custom test procedures can then be implemented and executed at minimal cost and at different stages of RAN development and integration. This system allows for testing many commercial and open source random access networks with minimal technical overhead. Many attacks on the RAN can be run automatically by the system.


![soft-t-ue.png](https://github.com/oran-testing/soft-t-ue/blob/main/docs/images/soft-t-ue.png)

## Installation

To install the UE run:
``` UE Install (Machine A)
./scripts/install-ue.
```

To install the gNB run:
``` gNB Install (Machine B)
./scripts/install-open5gs.sh
./scripts/install-gnb.sh
```
## Running

To start the gNB daemon:
```
sudo systemctl daemon-reload
sudo systemctl start gnb-controller.service
```

To run the controller:
```
cd controller/ue
python3 main.py
```

![Soft-T-UE-System.png](https://github.com/oran-testing/soft-t-ue/blob/main/docs/images/Soft-T-UE-System.png)
