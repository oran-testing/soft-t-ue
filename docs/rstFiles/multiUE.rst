How to run srsRAN with multiple Ues
---------------------------------------

`Multi-UE emulation <https://docs.srsran.com/projects/project/en/latest/tutorials/source/srsUE/source/index.html#multi-ue-emulation>`_

Open5gs:

.. code:: bash

   cd ./srsRAN_Project/docker
   docker compose up --build 5gc

gNB:

.. code:: bash

   cd ./srsRAN_Project/build/apps/gnb
   sudo ./gnb -c gnb_zmq.yaml

Net namespaces:

.. code:: bash

   sudo ip netns add ue1
   sudo ip netns add ue2
   sudo ip netns add ue3

srsUE:

.. code:: bash

   cd ./srsRAN_4G/build/srsue/src
   sudo ./srsue ./ue1_zmq.conf
   sudo ./srsue ./ue2_zmq.conf
   sudo ./srsue ./ue3_zmq.conf

gNB radio:

.. code:: bash

   sudo gnuradio-companion ./multi_ue_scenario.grc
