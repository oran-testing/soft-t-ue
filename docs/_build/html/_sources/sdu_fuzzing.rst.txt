=========================
SDU Fuzzing Attack
=========================

Introduction
============

This attack randomly changes values in the SDU buffer of the RRC then sends the buffer to the gNB to cause malfunction

Contents
=========
.. code-block:: bash
  $ sudo srsue --rrc.sdu_fuzzed_bits 1 --rrc.fuzz_target_message "rrcSetupRequest"
