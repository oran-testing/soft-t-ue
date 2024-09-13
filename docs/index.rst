.. Soft-Tester UE documentation master file, created by
   sphinx-quickstart on Thu Sep 12 16:04:18 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Soft-Tester UE documentation
============================

This documentation is a part of our project, `Soft-Tester UE <https://www.rantesterue.org/>`_.

This project aims to develop a **software-defined tester UE for 5G and open RANs, focusing on security testing**. The soft T-UE will be compatible with commercial off-the-shelf software radio hardware, supporting both standardized and custom test.

.. toctree::
   :maxdepth: 1
   :caption: Attacks implemented

   attacks/cqi_manipulation.rst
   attacks/gnb_impersonation_attack.rst
   attacks/imsi_capture.rst
   attacks/preamble_collision.rst
   attacks/rach_jamming.rst
   attacks/rach_replay.rst
   attacks/rach_signal_flooding.rst
   attacks/rohc_poisoning_attack.rst