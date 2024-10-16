# Software Tester UE:

## Overview
The tester UE can be used on its own or with the python controller and GUI.

## Modified srsRAN User Equipment

To Install the customized srsRAN UE:
```bash
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```

The UE can be passed arguments described in the following pages to run various attacks:
- [cqi_manipulation.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/cqi_manipulation.rst)
- [gnb_impersonation_attack.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/gnb_impersonation_attack.rst)
- [imsi_capture.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/imsi_capture.rst)
- [preamble_collision.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/preamble_collision.rst)
- [rach_jamming.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/rach_jamming.rst)
- [rach_replay.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/rach_replay.rst)
- [rach_signal_flooding.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/rach_signal_flooding.rst)
- [rohc_poisoning_attack.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/rohc_poisoning_attack.rst)
- [rrc_signal_flooding.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/rrc_signal_flooding.rst)
- [sdu_fuzzing.rst](https://github.com/oran-testing/soft-t-ue/blob/main/docs/attacks/sdu_fuzzing.rst)

## Python Controller and Graphical User Interface

To run the controller:
```bash
cd controller/ue
python3 main.py
```

Controller arguments:
python3 main.py -h --config /path/to/config --gnb_config /path/to/gnb_config --ip IP --port PORT

Run an srsRAN gNB and Open5GS, then send metrics to the ue_controller

options:
  -h, --help
  --config default:../../configs/basic_ue_zmq.yaml     Path of the controller config file
  --gnb_config default:../../configs/zmq/gnb_zmq.conf     Path of the controller config file
  --ip default:127.0.0.1                                  IP used to communicate the gNB controller
  --port default:5000                                     Port used to communicate with the gNB controller

## Configuring the UE:

The UE controller reads a yaml config file with the following options:
gnb:
  config -> gNB config file (str)

namespaces:
  - name -> namespace to be created (str)

processes:
  - type -> type of process to run (clean | tester | jammer | ...)
    config_file -> config file for process (str)
    args -> OPTIONAL: arguments to pass to the process (str)

Example configuration files:
- [basic_ue_zmq.yaml](https://github.com/oran-testing/soft-t-ue/blob/main/configs/basic_ue_zmq.rst)
- [multi_ue_zmq.yaml](https://github.com/oran-testing/soft-t-ue/blob/main/configs/multi_ue_zmq.rst)
