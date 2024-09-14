from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Line, Color
from SharedState import SharedState
import time
import threading


class LegendItem(GridLayout):
    def __init__(self, **kwargs):
        super(LegendItem, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 40
        self.cols = 3
        self.padding = [40,0,40,0]

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Line(width=1)

        self.bind(size=self.update_border, pos=self.update_border)

    def update_border(self, *args):
        self.rect.rectangle = (self.x, self.y, self.width, self.height)


class ResultsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=[10,40,10,10], spacing=10,size_hint_y=None, height=1000)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.scrollview = ScrollView()
        self.scrollview.add_widget(self.layout)
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
            self.create_graph(graph, ue_ref["handle"].iperf_client.output, plot_color=SharedState.plot_map["iperf"]["color"])
            self.create_graph(graph, ue_ref["handle"].ping_client.output, plot_color=SharedState.plot_map["ping"]["color"])

            legend_grid = GridLayout(cols=2 , padding=[10,40,10,10], spacing=20)

            container.add_widget(Label(text=f"UE{ue_ref['index']}, rnti: {ue_ref['handle'].rnti}, Iperf running: {ue_ref['handle'].iperf_client.isRunning}", size_hint_y=None, height=20, font_size="20sp"))
            container.add_widget(graph)

            SharedState.metrics_client.read_data()
            for plot_type, plot_config in SharedState.plot_map.items():
                label = LegendItem()
                label.add_widget(Label(text=f"{plot_type}",color=plot_config["color"], font_size="20sp"))
                label.add_widget(Label(text=f"{plot_config['description']}"))
                label.add_widget(Label(text=f"{plot_config['unit']}"))
                legend_grid.add_widget(label)
                if plot_type == "iperf" or plot_type == "ping":
                    continue
                self.create_graph(
                    graph,
                    SharedState.metrics_client.ue_data[ue_ref["handle"].rnti][plot_type]["values"],
                    plot_color=plot_config["color"]
                )

            container.add_widget(legend_grid)
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

