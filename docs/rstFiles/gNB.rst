ORAN srsRAN gNB controller
==========================

Overview
--------

Our gNB controller software manages four main processes: 
- Open5GS Core
Network 
- srsRAN generational Node B 
- Python Metrics Server 
- InfluxDB

Installation and Usage
----------------------

To install the gNB:

.. code:: bash

   sudo ./scripts/install-open5gs.sh
   sudo ./scripts/install-gnb.sh

This will create a ``gnb-controller.service`` file in
``/etc/systemd/system/``

Then run:

.. code:: bash

   sudo systemctl daemon-reload
   sudo systemctl start gnb-controller.service

The daemon will take around one minute to build and start all containers
depending on the system

Optionally the controller can be run without systemctl:

.. code:: bash

   cd controller/gnb
   sudo python3 main.py

Message structure
-----------------

Each message passed from UE to gNB controllers is as follows:

{ “target”: service to target (str) “action”: action to perform (start
\| stop) “port”: OPTIONAL port to use (int) }
