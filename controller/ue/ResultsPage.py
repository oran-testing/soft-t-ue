from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.scrollview import ScrollView
from SharedState import SharedState
import time
import threading


class ResultsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=[10,40,10,10], spacing=10,size_hint_y=None, height=1000)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.scrollview = ScrollView()
        self.scrollview.add_widget(self.layout)

        self.plot_map = {
            "bsr":          {"color": [1, 0, 0, 1],      "description": "Buffer Status Report",            "likely_value": "0 to 100 (bytes)"},
            "cqi":          {"color": [0, 1, 0, 1],      "description": "Channel Quality Indicator",       "likely_value": "1 to 15 (integer)"},
            "dl_brate":     {"color": [0, 0, 1, 1],      "description": "Downlink Bitrate",                "likely_value": "0 to several Gbps"},
            "dl_bs":        {"color": [1, 1, 0, 1],      "description": "Downlink Block Size",             "likely_value": "1000 to 15000 (bits)"},
            "dl_mcs":       {"color": [1, 0, 1, 1],      "description": "Downlink Modulation and Coding",  "likely_value": "0 to 28 (integer)"},
            "dl_nof_nok":   {"color": [0, 1, 1, 1],      "description": "Number of Downlink Failures",     "likely_value": "0 to 100 (integer)"},
            "dl_nof_ok":    {"color": [0.5, 0, 0.5, 1],  "description": "Number of Successful Downlinks",  "likely_value": "0 to 1000 (integer)"},
            "pci":          {"color": [0.8, 0.5, 0, 1],  "description": "Physical Cell ID",                "likely_value": "0 to 503 (integer)"},
            "pusch_snr_db": {"color": [0.5, 0.5, 0.5, 1],"description": "PUSCH SNR (Signal to Noise Ratio)","likely_value": "-20 to 30 dB"},
            "ri":           {"color": [0.6, 0.2, 0.8, 1],"description": "Rank Indicator",                  "likely_value": "1 to 2 (integer)"},
            "ul_brate":     {"color": [0.2, 0.8, 0.2, 1],"description": "Uplink Bitrate",                  "likely_value": "0 to several Gbps"},
            "ul_mcs":       {"color": [0.8, 0.2, 0.2, 1],"description": "Uplink Modulation and Coding",    "likely_value": "0 to 28 (integer)"},
            "ul_nof_nok":   {"color": [0.2, 0.2, 0.8, 1],"description": "Number of Uplink Failures",       "likely_value": "0 to 100 (integer)"},
            "ul_nof_ok":    {"color": [0.8, 0.8, 0.2, 1],"description": "Number of Successful Uplinks",    "likely_value": "0 to 1000 (integer)"},
            "iperf":        {"color": [0.2, 0.6, 0.8, 1],"description": "iPerf Bandwidth Test Result",      "likely_value": "Mbps to Gbps"},
            "ping":         {"color": [0.7, 0.4, 0.1, 1],"description": "Ping Latency",                    "likely_value": "0 to 100 ms (milliseconds)"}
        }

        self.add_widget(self.scrollview)
        self.rendered_ue_list = []


    def init_results(self):

        for ue_ref in SharedState.process_list:
            if ue_ref['id'] in self.rendered_ue_list:
                continue

            graph = Graph(
                xlabel='time (s)',
                ylabel=f"UE{ue_ref['index']}",
                x_ticks_minor=5,
                x_ticks_major=50,
                y_ticks_major=50,
                y_ticks_minor=5,
                y_grid_label=True,
                x_grid_label=True,
                padding=5,
                xlog=False,
                ylog=False,
                x_grid=True,
                y_grid=True,
                ymin=0,
                xmin=0,
                xmax=100,
                ymax=200,
                size_hint_y=None,
                height=500
            )
            self.rendered_ue_list.append(ue_ref["id"])
            container = BoxLayout(orientation="vertical", size_hint_y=None, height=1000)
            self.create_graph(graph, ue_ref["handle"].iperf_client.output, plot_color=self.plot_map["iperf"]["color"])
            self.create_graph(graph, ue_ref["handle"].ping_client.output, plot_color=self.plot_map["ping"]["color"])

            container.add_widget(Label(text=f"UE{ue_ref['id']}, rnti: {ue_ref['handle'].rnti}", size_hint_y=None, height=20, font_size="20sp"))
            container.add_widget(graph)

            SharedState.metrics_client.read_data()
            for plot_type, plot_config in self.plot_map.items():
                container.add_widget(
                    Label(text=f"{plot_type} -> {plot_config['description']}", color=plot_config["color"])
                )
                if plot_type == "iperf" or plot_type == "ping":
                    continue
                self.create_graph(
                    graph,
                    SharedState.metrics_client.ue_data[ue_ref["handle"].rnti][plot_type]["values"],
                    plot_color=plot_config["color"]
                )

            self.layout.add_widget(container)

       


    def create_graph(self,
                     graph,
                     ue_ref,
                     plot_color=[0,1,0,1]):

        plot = MeshLinePlot(color=plot_color)
        plot.line_width = 10
        graph.add_plot(plot)
        Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref), 1)


    def update_points(self, plot, data_ref):
        if len(data_ref) < 1:
            return
        if len(data_ref) < 100:
            plot.points = data_ref
        else:
            plot.points = data_ref[-100:]

