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

        self.add_widget(self.scrollview)
        self.rendered_ue_list = []
        Clock.schedule_once(lambda dt: self.init_results())


    def init_results(self):
        row = 0
        ue_data = SharedState.metrics_client.read_data().items()
        for rnti, metrics in ue_data:
            for field, data in metrics.items():
                if row == 2:
                    break
                graph_block = BoxLayout(orientation="vertical", size_hint_y=None, height=500)
                graph_block.add_widget(self.create_graph(
                    field,
                    SharedState.metrics_client.ue_data,
                    rnti=rnti
                ))
                self.layout.add_widget(Label(text=f"{field}", size_hint_y=None, height=20, font_size="30sp"))
                self.layout.add_widget(graph_block)
                row +=1

        for ue_ref in SharedState.process_list:
            if ue_ref['id'] in self.rendered_ue_list:
                continue
            self.rendered_ue_list.append(ue_ref["id"])
            container = BoxLayout(orientation="vertical", size_hint_y=None, height=500)
            self.layout.add_widget(Label(text=f"Iperf", size_hint_y=None, height=20, font_size="30sp"))
            self.layout.add_widget(self.create_graph("iperf", ue_ref))
            self.layout.add_widget(Label(text=f"Ping", size_hint_y=None, height=20, font_size="30sp"))
            self.layout.add_widget(self.create_graph("ping", ue_ref, defined_label="Latency (ms)"))
            self.layout.add_widget(container)
        


    def create_graph(self,
                     graph_type,
                     ue_ref,
                     defined_label="Bandwidth (MBits/sec)",
                     rnti=""):
        plot = MeshLinePlot(color=[1,1,0,1])
        plot.line_width = 10
        graph = Graph(
            xlabel='time (s)',
            ylabel=defined_label,
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
            ymax=100,
            size_hint_y=None,
            height=500
        )


        graph.add_plot(plot)
        if graph_type == "ping":
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref["handle"].ping_client.output, graph), 1)
        elif graph_type == "iperf":
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref["handle"].iperf_client.output, graph), 1)
        else:
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref[rnti][graph_type]["values"], graph, ymax=ue_ref[rnti][graph_type]["ymax"]), 1)

        return graph

    def update_points(self, plot, data_ref, graph, ymax=None):
        if len(data_ref) < 1:
            return
        if ymax:
            graph.ymax = ymax

        if len(data_ref) < 100:
            plot.points = data_ref
        else:
            plot.points = data_ref[-100:]
            graph.xmax = data_ref[-1][0]
            graph.xmin = data_ref[-100][0]

