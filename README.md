# NTIA Software Tester

An SDR security testing UE based on srsRAN's UE.

## Overview

The tester consists of a client PC running the test GUI and a server PC running
the base station. (In some cases, a single PC can run both the client and the
server.) The client GUI launches a series of applications to run a test. It
communicates with the server to indirectly launch server-side applications with
appropriate configurations.

<img src='https://g.gravizo.com/svg?
digraph G {
    subgraph cluster_client {
        label = "Client PC"
        client -> tue
        client -> pcap [ dir=both ]
        client -> grafana_gnb
        client -> grafana_5gc
        client -> iperf3 [ dir = both ]
        client [ label = "Client GUI\n(Python)"]
        tue [ label = "Soft T-UE"]
        pcap [ label = "Packet capture\n(scapy)"]
        grafana_gnb [ label = "Grafana gNodeB\ndata viz"]
        grafana_5gc [ label = "Grafana open 5G core\ndata viz"]
        iperf3 [ label = "iperf3\nclient"]
    }
    client -> server [ dir = both, style = dotted ]
    tue -> gnb [ dir = both, style = dotted ]
    gnb -> grafana_gnb [ style = dotted ]
    open5g -> grafana_5gc [ style = dotted ]
    iperf3 -> iperf3_server [ dir = both, style = dotted ]
    subgraph cluster_server {
        label = "Server PC"
        server -> iperf3_server
        server -> gnb
        gnb -> open5g [ style = dotted ]
        server [ label = "Server\n(Python)"]
        gnb [ label = "gNodeB"]
        open5g [ label = "Open5G\nCore"]
        iperf3_server [ label = "iperf3\nserver"]
    }
})'/>

Legend:

- A solid line indicates a process/subprocess relationship. If bidirectional,
  the subprocess provides data back to the process via pipes.
- A dotted line indicates data movement between two processes.
