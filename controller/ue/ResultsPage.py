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
        self.height = 50
        self.cols = 2
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

        SharedState.metrics_client.read_data()
        self.layout = GridLayout(cols=1, padding=[10,40,10,10], spacing=10,size_hint_y=None, height=1000)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.scrollview = ScrollView()
        self.scrollview.add_widget(self.layout)
        self.add_widget(self.scrollview)
        self.rendered_ue_list = []


    def init_results(self):
        for ue_ref in SharedState.process_list:
            if ue_ref['id'] in self.rendered_ue_list or not ue_ref["handle"].isConnected:
                continue

            graph = Graph(
                xlabel='time (s)',
                ylabel=f"UE{ue_ref['index']}",
                x_ticks_minor=1,
                x_ticks_major=5,
                y_ticks_minor=1,
                y_ticks_major=5,
                padding=5,
                x_grid=True,
                y_grid=True,
                ymin=0,
                xmin=0,
                xmax=100,
                ymax=200,
                size_hint_y=None,
                height=1000
            )
            self.rendered_ue_list.append(ue_ref["id"])
            container = BoxLayout(orientation="vertical", size_hint_y=None, height=1000)
            self.create_graph(graph,
                              ue_ref["handle"].iperf_client.output,
                              plot_color=SharedState.plot_map["iperf"]["color"],
                              plot_map_ref="iperf"
                              )
            self.create_graph(graph,
                              ue_ref["handle"].ping_client.output,
                              plot_color=SharedState.plot_map["ping"]["color"],
                              plot_map_ref="ping"
                              )

            legend_grid = GridLayout(cols=2)

            container.add_widget(Label(
                text=f"UE{ue_ref['index']}, rnti: {ue_ref['handle'].rnti}, Iperf running: {ue_ref['handle'].iperf_client.isRunning}",
                size_hint_y=None,
                height=20,
                font_size="20sp",
                font_name="./font/Ubuntu/Ubuntu-Bold.ttf"
            ))
            container.add_widget(graph)

            self.value_labels = {}
            self.grafana_enabled = True
            if ue_ref["handle"].rnti not in SharedState.metrics_client.ue_data.keys():
                self.grafana_enabled = False
            for plot_type, plot_config in SharedState.plot_map.items():
                label = LegendItem()
                label.add_widget(Label(
                    text=f"{plot_type}",
                    color=plot_config["color"],
                    font_size="20sp",
                    font_name="./font/Ubuntu/Ubuntu-Regular.ttf"
                ))
                label.add_widget(Label(
                    text=f"{plot_config['description']}",
                    font_size="20sp",
                    font_name="./font/Ubuntu/Ubuntu-Regular.ttf"
                ))
                self.value_labels[plot_type] = Label(text=f"0",
                                                     font_size="20sp",
                                                     font_name="./font/Ubuntu_Mono/UbuntuMono-Regular.ttf"
                                                     )
                label.add_widget(self.value_labels[plot_type])
                Clock.schedule_interval(lambda dt, p=plot_type: self.update_legend(p), 1)
                label.add_widget(Label(
                    text=f"{plot_config['unit']}",
                    font_size="20sp",
                    font_name="./font/Ubuntu_Mono/UbuntuMono-Regular.ttf"
                ))
                legend_grid.add_widget(label)
                if plot_type == "iperf" or plot_type == "ping":
                    continue
                if self.grafana_enabled:
                    self.create_graph(
                        graph,
                        SharedState.metrics_client.ue_data[ue_ref["handle"].rnti][plot_type]["values"],
                        plot_color=plot_config["color"],
                        plot_map_ref=plot_type
                    )
            container.add_widget(legend_grid)
            self.layout.add_widget(container)

    def update_legend(self, plot_type):
        self.value_labels[plot_type].text = str(SharedState.plot_map[plot_type]["current_value"])


    def create_graph(self,
                     graph,
                     ue_ref,
                     plot_color=[0,1,0,1],
                     plot_map_ref=None):

        plot = MeshLinePlot(color=plot_color)
        plot.line_width = 10
        graph.add_plot(plot)
        Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref, plot_map_ref), 1)


    def update_points(self, plot, data_ref, plot_map_ref):
        if len(data_ref) < 1:
            return
        if len(data_ref) < 100:
            plot.points = data_ref
        else:
            offset = len(data_ref) - 100
            plot.points = [(t[0] - offset, t[1]) for t in data_ref[-100:]]
        SharedState.plot_map[plot_map_ref]["current_value"] = data_ref[-1][1]

