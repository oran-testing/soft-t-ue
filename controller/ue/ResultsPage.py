from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy_garden.graph import Graph, MeshLinePlot
from SharedState import SharedState


class ResultsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=[10,40,10,10], spacing=10,)
        self.add_widget(self.layout)
        self.rendered_ue_list = []

    def init_results(self):
        for ue_ref in SharedState.process_list:
            if ue_ref['id'] in self.rendered_ue_list:
                continue
            self.rendered_ue_list.append(ue_ref["id"])
            ue_results_block = BoxLayout()
            ue_results_block.add_widget(self.create_graph("iperf", ue_ref))
            ue_results_block.add_widget(self.create_graph("ping", ue_ref))
            self.layout.add_widget(Label(text=f"UE{ue_ref['index']}", size_hint_y=None, height=20, font_size="30sp"))
            self.layout.add_widget(ue_results_block)


    def create_graph(self, graph_type, ue_ref):
        plot = MeshLinePlot(color=[0,1,0,1])
        plot.line_width = 6
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
            ymax=70,
            xmin=0,
            xmax=100
        )
        if graph_type == "ping":
            graph.ylabel = "Latency (ms)"
            graph.ymax = 150

        graph.add_plot(plot)
        xdata = list(range(100))
        ydata = [0] * 100
        if graph_type == "ping":
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref["handle"].ping_client.output, xdata, ydata), 1)
        else:
            Clock.schedule_interval(lambda dt: self.update_points(plot, ue_ref["handle"].iperf_client.output, xdata, ydata), 1)

        return graph

    def update_points(self, plot, data_ref, xdata, ydata):
        if len(data_ref) > 0:
            new_y = data_ref[-1]
            ydata.append(new_y)
            if len(ydata) > len(xdata):
                ydata.pop(0)

        while len(xdata) > len(ydata):
            xdata.pop(0)

        plot.points = list(zip(xdata, ydata))


