SDU Fuzzing Attack
==============================

Introduction 
-------------
This attack randomly changes values in the SDU buffer of the RRC then sends the buffer to the gNB to cause malfunction.

The fuzzing attack we currently have is limited in its application since all the fuzzing being done is entirely random. There are a few ways this can be fixed in the implementation:

- Allow for a fuzzed_file with an asn1 encoding of the fuzzed message provided by the user
- Allow for generative AI to be used in generating fuzzed messages
- Allow user input to modify the message being sent (--rrc.fuzz_args "rnti:0 plmn:011")
