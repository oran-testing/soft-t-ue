1. Channel Quality Indicator (CQI)
Definition: Represents the quality of the downlink channel as perceived by the UE. It indicates the highest modulation and coding scheme (MCS) that can be used while maintaining a target block error rate (typically 10%).
Types:
Wideband CQI: A single value representing the overall channel quality across the entire downlink bandwidth.
Subband CQI: Reports the quality of specific subbands, offering finer granularity.
2. Rank Indicator (RI)
Definition: Indicates the preferred number of spatial streams the UE can effectively use. It is used for MIMO (Multiple Input Multiple Output) configurations.
Purpose: Allows the gNB to decide how many layers or spatial streams to use for transmission.
Values: Range from 1 (single-stream transmission) to a maximum value determined by the number of transmit antennas at the gNB and the UE's capability.
3. Precoding Matrix Indicator (PMI)
Definition: Indicates the preferred precoding matrix to be used for MIMO transmissions. It helps the gNB in selecting the best precoding vector for beamforming.
Components:
Codebook-based PMI: Reports specific entries from a predefined set of precoding matrices.
Wideband PMI: Refers to a single precoding matrix for the entire bandwidth.
Subband PMI: Refers to different precoding matrices for specific subbands.
4. Channel State Information Reference Signal (CSI-RS) Received Power (CRI/RSRP)
Definition: Reports the received power level of CSI-RS, which is a reference signal used for channel estimation.
Purpose: Helps in beam management by indicating the best beam or the strongest received signal strength.
Types:
RSRP (Reference Signal Received Power): Average received power of reference signals over the channel.
CRI (CSI-RS Resource Indicator): Identifies which CSI-RS resource has the strongest signal.
5. Layer Indicator (LI)
Definition: Indicates the number of MIMO layers preferred by the UE.
Purpose: Used in conjunction with RI to determine the exact layering for downlink transmissions.
Usage: Typically relevant in scenarios involving multiple transmission layers.
6. CSI-SINR (Signal-to-Interference-plus-Noise Ratio)
Definition: Provides the SINR values for the CSI-RS, indicating the channel quality while taking interference into account.
Purpose: Helps in fine-tuning adaptive modulation and coding schemes (AMCS).
7. CSI Report Type (Report Quantity)
Definition: Defines the overall type of CSI report, which can include combinations of the metrics above.
Examples:
CRI + RI + CQI: A report containing information on channel rank, the CSI-RS resource, and channel quality.
CRI + RSRP: Focuses on beam management and signal strength.
8. Beam Index (SSB Index + RSRP)
Definition: Indicates the index of the best beam and its associated RSRP value.
Purpose: Used for beam selection and mobility management, helping the gNB identify which beam provides the best signal quality.
9. Interference Measurements (e.g., CSI-IM RSRP)
Definition: Measures the interference power from neighboring cells or beams using CSI-Interference Measurement (CSI-IM) signals.
Purpose: Allows the gNB to understand interference conditions and make adjustments in scheduling and resource allocation.
