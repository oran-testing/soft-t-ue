# RRC Messages documentation:

<details>
<summary>UpLink CCCH messages:</summary>
const char* dl_ccch_msg_type_c::c1_c_::types_opts::to_string() const
{
  static const char* options[] = {"rrcConnectionReestablishment",
                                  "rrcConnectionReestablishmentReject",
                                  "rrcConnectionReject",
                                  "rrcConnectionSetup"};
  return convert_enum_idx(options, 4, value, "dl_ccch_msg_type_c::c1_c_::types");
}
</details>

<details>
<summary>UpLink CCCH message declarations:</summary>
struct rrc_conn_reest_request_r8_ies_s {
  reestab_ue_id_s    ue_id;
  reest_cause_e      reest_cause;
  fixed_bitstring<2> spare;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};

// RRCConnectionRequest-5GC-r15-IEs ::= SEQUENCE
struct rrc_conn_request_minus5_gc_r15_ies_s {
  init_ue_id_minus5_gc_r15_c          ue_id_r15;
  establishment_cause_minus5_gc_r15_e establishment_cause_r15;
  fixed_bitstring<1>                  spare;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};
</details>
<details>
<summary> DownLink CCCH messages:</summary>
const char* dl_ccch_msg_type_c::c1_c_::types_opts::to_string() const
{
  static const char* options[] = {"rrcConnectionReestablishment",
                                  "rrcConnectionReestablishmentReject",
                                  "rrcConnectionReject",
                                  "rrcConnectionSetup"};
  return convert_enum_idx(options, 4, value, "dl_ccch_msg_type_c::c1_c_::types");
}
</details>


<details>
<summary>DownLink CCCH Message declarations:</summary>
// RRCConnectionReestablishment-v8a0-IEs ::= SEQUENCE
struct rrc_conn_reest_v8a0_ies_s {
  bool          late_non_crit_ext_present = false;
  bool          non_crit_ext_present      = false;
  dyn_octstring late_non_crit_ext;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};

// RRCConnectionReestablishmentReject-v8a0-IEs ::= SEQUENCE
struct rrc_conn_reest_reject_v8a0_ies_s {
  bool          late_non_crit_ext_present = false;
  bool          non_crit_ext_present      = false;
  dyn_octstring late_non_crit_ext;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};

// RRCConnectionReject-v8a0-IEs ::= SEQUENCE
struct rrc_conn_reject_v8a0_ies_s {
  bool                        late_non_crit_ext_present = false;
  bool                        non_crit_ext_present      = false;
  dyn_octstring               late_non_crit_ext;
  rrc_conn_reject_v1020_ies_s non_crit_ext;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};


// RRCConnectionReject-v1020-IEs ::= SEQUENCE
struct rrc_conn_reject_v1020_ies_s {
  bool                        extended_wait_time_r10_present = false;
  bool                        non_crit_ext_present           = false;
  uint16_t                    extended_wait_time_r10         = 1;
  rrc_conn_reject_v1130_ies_s non_crit_ext;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};

// RRCConnectionSetup-v1610-IEs ::= SEQUENCE
struct rrc_conn_setup_v1610_ies_s {
  bool          ded_info_nas_r16_present = false;
  bool          non_crit_ext_present     = false;
  dyn_octstring ded_info_nas_r16;

  // sequence methods
  SRSASN_CODE pack(bit_ref& bref) const;
  SRSASN_CODE unpack(cbit_ref& bref);
  void        to_json(json_writer& j) const;
};
<details>


<details>
<summary>Uplink DCCH messages:</summary>
const char* dl_dcch_msg_type_c::c1_c_::types_opts::to_string() const
{
  static const char* options[] = {"csfbParametersResponseCDMA2000",
                                  "dlInformationTransfer",
                                  "handoverFromEUTRAPreparationRequest",
                                  "mobilityFromEUTRACommand",
                                  "rrcConnectionReconfiguration",
                                  "rrcConnectionRelease",
                                  "securityModeCommand",
                                  "ueCapabilityEnquiry",
                                  "counterCheck",
                                  "ueInformationRequest-r9",
                                  "loggedMeasurementConfiguration-r10",
                                  "rnReconfiguration-r10",
                                  "rrcConnectionResume-r13",
                                  "dlDedicatedMessageSegment-r16",
                                  "spare2",
                                  "spare1"};
  return convert_enum_idx(options, 16, value, "dl_dcch_msg_type_c::c1_c_::types");
}
</details>


<details>
<summary> DownLink DCCH messages:</summary>
const char* dl_dcch_msg_type_c::c1_c_::types_opts::to_string() const
{
  static const char* options[] = {"csfbParametersResponseCDMA2000",
                                  "dlInformationTransfer",
                                  "handoverFromEUTRAPreparationRequest",
                                  "mobilityFromEUTRACommand",
                                  "rrcConnectionReconfiguration",
                                  "rrcConnectionRelease",
                                  "securityModeCommand",
                                  "ueCapabilityEnquiry",
                                  "counterCheck",
                                  "ueInformationRequest-r9",
                                  "loggedMeasurementConfiguration-r10",
                                  "rnReconfiguration-r10",
                                  "rrcConnectionResume-r13",
                                  "dlDedicatedMessageSegment-r16",
                                  "spare2",
                                  "spare1"};
  return convert_enum_idx(options, 16, value, "dl_dcch_msg_type_c::c1_c_::types");
}
</details>
