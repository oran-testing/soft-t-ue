from MetricsClient import MetricsClient

class SharedState:
    process_list = []
    attack_args = []
    cli_args = None
    ue_index = 1
    metrics_client = MetricsClient()
    plot_map = {
        "bsr":          {
            "color": [1, 0, 0, 1],
            "description": "Buffer Status Report",
            "unit": "bytes"
        },
        "cqi":          {
            "color": [0, 1, 0, 1],
            "description": "Channel Quality Indicator",
            "unit": "integer"
        },
        "dl_brate":     {
            "color": [0, 0, 1, 1],
            "description": "Downlink Bitrate",
            "unit": "Gbps"
        },
        "dl_bs":        {
            "color": [1, 1, 0, 1],
            "description": "Downlink Block Size",
            "unit": "bits"
        },
        "dl_mcs":       {
            "color": [1, 0, 1, 1],
            "description": "Downlink Modulation and Coding",
            "unit": "integer"
        },
        "dl_nof_nok":   {
            "color": [0, 1, 1, 1],
            "description": "Number of Downlink Failures",
            "unit": "integer"
        },
        "dl_nof_ok":    {
            "color": [0.5, 0, 0.5, 1],
            "description": "Number of Successful Downlinks",
            "unit": "integer"
        },
        "pci":          {
            "color": [0.8, 0.5, 0, 1],
            "description": "Physical Cell ID",
            "unit": "integer"
        },
        "pusch_snr_db": {
            "color": [0.8, 0.5, 0.8, 1],
            "description": "Signal to Noise Ratio",
            "unit": "dB"
        },
        "ri":           {
            "color": [0.6, 0.2, 0.8, 1],
            "description": "Rank Indicator",
            "unit": "integer"
        },
        "ul_brate":     {
            "color": [0.2, 0.8, 0.2, 1],
            "description": "Uplink Bitrate",
            "unit": "Gbps"
        },
        "ul_mcs":       {
            "color": [0.8, 0.2, 0.2, 1],
            "description": "Uplink Modulation and Coding",
            "unit": "integer"
        },
        "ul_nof_nok":   {
            "color": [0.2, 0.2, 0.8, 1],
            "description": "Number of Uplink Failures",
            "unit": "integer"
        },
        "ul_nof_ok":    {
            "color": [0.8, 0.8, 0.2, 1],
            "description": "Number of Successful Uplinks",
            "unit": "integer"
        },
        "iperf":        {
            "color": [0.2, 0.6, 0.8, 1],
            "description": "iPerf Bandwidth Test Result",
            "unit": "Gbps"
        },
        "ping":         {
            "color": [0.7, 0.4, 0.1, 1],
            "description": "Ping Latency",
            "unit": "milliseconds"
        }
    }
