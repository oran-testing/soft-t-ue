import time
import uuid
import threading
import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.image import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import io
from kivy.graphics.texture import Texture
import PIL.Image




# add the common directory to the import path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from ue_interface import Ue


class ProcessesPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ue_index = 1
        layout = BoxLayout(orientation='vertical')
        self.process_container = BoxLayout(orientation='vertical', padding=0, height=500)
        self.process_scroll_wrapper = ScrollView()
        self.process_scroll_wrapper.add_widget(self.process_container)
        layout.add_widget(self.process_scroll_wrapper)

        add_ue_button = Button(text='Add UE', on_press=self.open_add_ue_popup, background_color=[0,1,0,1], size_hint_y=None)
        layout.add_widget(add_ue_button)

        self.config_file = ""
        self.ue_type = "clean"


        self.add_widget(layout)

    def open_add_ue_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.config_label = Label(text="Selected file: None")
        self.ue_type_label = Label(text=f"UE type: {self.ue_type}")

        cancel_button = Button(text="Cancel", size_hint_y=None, height=50)
        select_config_button = Button(text="Select config", size_hint_y=None, height=50)
        add_button = Button(text="Add", size_hint_y=None, height=50)

        ue_type_spinner = Spinner(
            text='Select an option',
            values=('clean', 'tester'),
            size_hint=(None, None),
            size=(200, 44)
        )

        button_wrapper = BoxLayout(orientation='horizontal')

        content.add_widget(self.config_label)
        content.add_widget(select_config_button)
        content.add_widget(self.ue_type_label)
        content.add_widget(ue_type_spinner)
        button_wrapper.add_widget(cancel_button)
        button_wrapper.add_widget(add_button)
        content.add_widget(button_wrapper)

        self.popup = Popup(title='Add New UE', content=content, size_hint=(0.5, 0.5))
        cancel_button.bind(on_press=self.popup.dismiss)
        add_button.bind(on_press=self.add_ue)
        select_config_button.bind(on_press=self.open_select_file_popup)
        ue_type_spinner.bind(text=self.set_ue_type)
        self.popup.open()

    def open_select_file_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(path='/home/')
        button_layout = BoxLayout(size_hint_y=None, height=50)
        select_button = Button(text="Select", size_hint_y=None, height=50)
        cancel_button = Button(text="Cancel", size_hint_y=None, height=50)

        button_layout.add_widget(select_button)
        button_layout.add_widget(cancel_button)
        content.add_widget(filechooser)
        content.add_widget(button_layout)

        popup = Popup(title='Choose a File', content=content, size_hint=(0.9, 0.9))

        select_button.bind(on_press=lambda x: self.select_file(filechooser, popup))
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()

    def select_file(self, filechooser, popup):
        selected = filechooser.selection
        if selected:
            self.config_file = selected[0]
            self.config_label.text = f'Selected file: {selected[0]}'
        popup.dismiss()

    def set_ue_type(self, spinner, text):
        # Update the label with the selected option
        self.ue_type_label.text = f'UE type: {text}'
        self.ue_type = text

    def add_ue(self, instance):
        self.popup.dismiss()
        new_ue = Ue(self.ue_index)
        #global attack_args
        attack_args = ["--phy.cqi_max", "200", "--phy.cqi_fixed", "200"]
        if self.ue_type == "tester":
            print(attack_args)
            new_ue.start([self.config_file] + attack_args)
        else:
            new_ue.start([self.config_file])
        global ue_list
        ue_list.append({
            'id':str(uuid.uuid4()),
            'type': self.ue_type,
            'config': self.config_file,
            'handle': new_ue
        })

        log_view = ScrollView(size_hint=(1, 2))
        iperf_view = ScrollView(size_hint=(1, 2))

        new_ue_label = Label(text=f"starting UE ({self.ue_type})...", width=200)
        new_iperf_label = Label(text=f"starting iperf for UE ({self.ue_type})...", width=200)
        Clock.schedule_interval(lambda dt: self.collect_logs(new_ue_label, new_iperf_label,new_ue, log_view, iperf_view), 1)
        content_label = Label(text=f"sudo srsue {self.config_file} ({self.ue_type})")

        self.process_container.add_widget(content_label)
        log_view.add_widget(new_ue_label)
        iperf_view.add_widget(new_iperf_label)
        self.process_container.add_widget(log_view)
        self.process_container.add_widget(iperf_view)


        self._update_scroll_height()

        self.config_file = ""
        self.ue_type = "clean"
        self.ue_index += 1


    def collect_logs(self, label_ref, iperf_label_ref, output_ref, log_ref, iperf_ref):
        label_ref.text = output_ref.output
        iperf_label_ref.text = str(output_ref.iperf_client.output)
        log_ref.scroll_y = 0
        iperf_ref.scroll_y = 0

    def _update_scroll_height(self):
        self.process_scroll_wrapper.scroll_y = 0


class AttacksPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        attack_option = Spinner(
            text='Attack Type',
            values=('None', 'SDU Fuzzing'),
            size_hint=(None, None),
            size=(400, 44)
        )
        attack_option.bind(text=self.set_attack_type)
        layout.add_widget(attack_option)
        self.title = Label(text="Attack Type: None")
        self.attack_type = "None"
        self.attack_settings = BoxLayout(orientation='vertical')
        layout.add_widget(self.title)
        layout.add_widget(self.attack_settings)
        self.add_widget(layout)
        self.num_fuzzed_bits = 1
        self.target_message = "All"

    def set_attack_type(self, spinner, text):
        self.title.text = f'Attack Type: {text}'
        self.attack_type = text
        if text == "SDU Fuzzing":
            target_message = Spinner(
                text='Target Message',
                values=('All', 'rrcSetupRequest','rrcRegistrationRequest'),
                size_hint=(None, None),
                size=(400, 44)
            )
            target_message.bind(text=self.set_target_message)
            bits_to_fuzz = Spinner(
                text='Number of Bits to Fuzz',
                values=[str(i) for i in range(1, 11)],
                size_hint=(None, None),
                size=(200, 44)
            )
            bits_to_fuzz.bind(text=self.set_fuzzed_bits)
            self.attack_settings.add_widget(target_message)
            self.attack_settings.add_widget(bits_to_fuzz)

    def set_target_message(self, spinner, text):
        self.target_message = text
        if text != "All":
            global attack_args
            attack_args = ["--rrc.sdu_fuzzed_bits", str(self.num_fuzzed_bits)
                           , "--rrc.fuzz_target_message", self.target_message]
            self.title.text = f"--rrc.sdu_fuzzed_bits {self.num_fuzzed_bits} --rrc.fuzz_target_message {self.target_message}"

    def set_fuzzed_bits(self, spinner, text):
        self.num_fuzzed_bits = int(text)
        global attack_args
        attack_args = ["--rrc.sdu_fuzzed_bits", str(self.num_fuzzed_bits)
                       , "--rrc.fuzz_target_message", self.target_message]
        self.title.text = f"--rrc.sdu_fuzzed_bits {self.num_fuzzed_bits} --rrc.fuzz_target_message {self.target_message}"


class ResultsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        self.rendered_ue_list = []

    def init_results(self):
        global ue_list
        for ue_ref in ue_list:
            if ue_ref['id'] in self.rendered_ue_list:
                continue
            self.rendered_ue_list.append(ue_ref["id"])
            self.create_graph("iperf", ue_ref)
            self.create_graph("ping", ue_ref)


    def create_graph(self, graph_type, ue_ref):
        canvas_widget = Image()
        canvas_label = Label(text=f'Iperf of {str(ue_ref["handle"])}')
        self.layout.add_widget(canvas_label)
        self.layout.add_widget(canvas_widget)
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(axis='both', colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        ax.set_xlim(0, 30)
        ax.set_ylim(0, 10)
        line, = ax.plot([], [], lw=2)
        xdata, ydata = list(range(30)), list(np.zeros(30))
        if graph_type == "iperf":
            iperf_ref = ue_ref["handle"].iperf_client.output
            Clock.schedule_interval(lambda dt: self.update_graph(iperf_ref, xdata, ydata, ax, fig, canvas_widget), 1)
        else:
            ping_ref = ue_ref["handle"].ping_client.output
            Clock.schedule_interval(lambda dt: self.update_graph(ping_ref, xdata, ydata, ax, fig, canvas_widget), 1)


    def update_graph(self, iperf_ref, xdata, ydata, ax, fig, canvas_widget):
        new_x = xdata[-1] + 1 if xdata else 0
        new_y = 0
        if len(iperf_ref) > 0:
            new_y = iperf_ref[-1]
        xdata.append(new_x)
        ydata.append(new_y)

        # Update the plot
        ax.clear()
        ax.plot(xdata, ydata, lw=2)
        ax.set_xlim(max(0, new_x - 30), new_x + 1)

        fig.canvas.draw()
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        canvas_widget.texture = self.texture_from_image(buf)

    def texture_from_image(self, buf):
        from kivy.graphics.texture import Texture
        image = PIL.Image.open(buf)
        image = image.convert('RGB')
        image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        texture = Texture.create(size=image.size, colorfmt='rgb')
        texture.blit_buffer(image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        return texture


class MainApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.processes = ProcessesPage(name='processes')
        self.attacks = AttacksPage(name='attacks')
        self.results = ResultsPage(name='results')

        self.screen_manager.add_widget(self.processes)
        self.screen_manager.add_widget(self.attacks)
        self.screen_manager.add_widget(self.results)

        # Define the button colors
        self.default_color = [1, 1, 1, 1]  # White
        self.highlighted_color = [0, 1, 0, 1]  # Green

        # Create a layout for the buttons on top
        self.button_layout = BoxLayout(size_hint_y=None, height=50)

        self.button_process_page = Button(text='Processes', on_press=self.switch_to_processes, background_color=self.highlighted_color)
        self.button_attacks_page = Button(text='Attacks', on_press=self.switch_to_attacks, background_color=self.default_color)
        self.button_results_page = Button(text='Results', on_press=self.switch_to_results, background_color=self.default_color)

        self.button_layout.add_widget(self.button_process_page)
        self.button_layout.add_widget(self.button_attacks_page)
        self.button_layout.add_widget(self.button_results_page)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.button_layout)
        main_layout.add_widget(self.screen_manager)

        return main_layout

    def switch_to_processes(self, instance):
        self.screen_manager.current = 'processes'
        self.update_button_colors(self.button_process_page)

    def switch_to_attacks(self, instance):
        self.screen_manager.current = 'attacks'
        self.update_button_colors(self.button_attacks_page)

    def switch_to_results(self, instance):
        self.screen_manager.get_screen('results').init_results()
        self.screen_manager.current = 'results'
        self.update_button_colors(self.button_results_page)

    def update_button_colors(self, active_button):
        # Reset all buttons to the default color
        self.button_process_page.background_color = self.default_color
        self.button_results_page.background_color = self.default_color
        self.button_attacks_page.background_color = self.default_color

        # Highlight the active button
        active_button.background_color = self.highlighted_color
    
def main():
    os.system("sudo kill -9 $(ps aux | awk '/srsue/{print $2}')")
    global ue_list
    ue_list = list()
    global attack_args
    attack_args = list()
    MainApp().run()

if __name__ == '__main__':
    main()
