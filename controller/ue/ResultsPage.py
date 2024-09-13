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
        self.grafana_metrics()


    def grafana_metrics(self):
        for rnti, metrics in SharedState.metrics_client.read_data().items():
            for field, data in metrics.items():
                graph_block = BoxLayout(orientation="vertical", size_hint_y=None, height=500)
                graph_block.add_widget(self.create_graph(field, data))
                self.layout.add_widget(Label(text=f"{field}", size_hint_y=None, height=20, font_size="30sp"))
                self.layout.add_widget(graph_block)


    def init_results(self):
        for ue_ref in SharedState.process_list:
            if ue_ref['id'] in self.rendered_ue_list:
                continue
            self.rendered_ue_list.append(ue_ref["id"])
            container = BoxLayout(orientation="vertical", size_hint_y=None, height=500)
            ue_results_block = BoxLayout(size_hint_y=None, height=500)
            ue_results_block.add_widget(self.create_graph("iperf", ue_ref))
            ue_results_block.add_widget(self.create_graph("ping", ue_ref))
            self.layout.add_widget(Label(text=f"UE{ue_ref['index']}", size_hint_y=None, height=20, font_size="30sp"))
            container.add_widget(ue_results_block)
            self.layout.add_widget(container)


    def create_graph(self, graph_type, ue_ref):
        plot = MeshLinePlot(color=[0,1,0,1])
        plot.line_width = 6
        graph = None
        if graph_type == "ping":
            graph = Graph(
                xlabel='time (s)',
                ylabel='Bandwidth (MBits/sec)',
                x_ticks_minor=1,
                x_ticks_major=5,
                y_ticks_major=5,
                y_ticks_minor=1,
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
                size_hint_y=None,
                height=500
            )
        elif graph_type == "iperf":
            graph = Graph(
                xlabel='time (s)',
                ylabel='Bandwidth (MBits/sec)',
                x_ticks_minor=1,
                x_ticks_major=5,
                y_ticks_major=5,
                y_ticks_minor=1,
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
                size_hint_y=None,
                height=500
            )

        else:
            graph = Graph(
                xlabel='time (s)',
                ylabel='Bandwidth (MBits/sec)',
                x_ticks_minor=1,
                x_ticks_major=5,
                y_ticks_major=5,
                y_ticks_minor=1,
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
                size_hint_y=None,
                height=500
            )


        graph.add_plot(plot)
        if graph_type == "ping":
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref["handle"].ping_client.output), 1)
        elif graph_type == "iperf":
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref["handle"].iperf_client.output), 1)
        else:
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref), 1)

        return graph

    def update_points(self, plot, data_ref):
        plot.points = data_ref
