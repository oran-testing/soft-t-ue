IP Routing
=============

Routing configuration
---------------------

gNB:

.. code:: bash

 sudo ip ro add 10.45.0.0/16 via 10.53.1.2
 ping 10.45.1.2

Note that all UE network commands must be run inside netns ue1 if you are running the UE with ZMQ on one machine.

ue:

.. code:: bash

 sudo ip route add default via 10.45.1.1 dev tun_srsue
 ping 10.45.1.1

Running Iperf
-------------

gnb:

.. code:: bash

 iperf3 -s -i 1

ue:

.. code:: bash

 # TCP
 iperf3 -c 10.53.1.1 -i 1 -t 60
 # or UDP
 iperf3 -c 10.53.1.1 -i 1 -t 60 -u -b 10M
