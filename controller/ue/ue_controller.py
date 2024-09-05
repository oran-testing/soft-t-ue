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

from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.uix.image import Image, AsyncImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen



# add the common directory to the import path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from ue_interface import Ue

class LandingPage(Screen):

    def __init__(self, **kwargs):
        self.animation_completed = 0
        super().__init__(**kwargs)

        layout = RelativeLayout()
        self.background = Image(source='Webimage.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(self.background)
        self.welcome_label = Label(
            text="Welcome to the NTIA Software Testing Platform!\nAn SDR security testing UE based on srsRAN's UE.",
            font_size='30sp',
            halign='center',
            valign='middle'
        )
    
        self.welcome_label.bind(size=self.welcome_label.setter('text_size'))
        layout.add_widget(self.welcome_label)
        self.welcome_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.animate_transition, 2)

    def animate_transition(self, *args):
        anim = Animation(opacity=0, duration=0.5)
        anim.start(self.welcome_label)
        anim.start(self.background) 

        self.animation_completed = 1
        anim.bind(on_complete=self.switch_to_processes)

    def switch_to_processes(self, *args):
        self.manager.current = 'processes'
        
class ProcessesPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.process_container = BoxLayout(
            orientation="vertical", 
            size_hint_y=None,
        )
        self.process_container.bind(minimum_height=self.process_container.setter('height'))
        self.process_scroll = ScrollView()
        self.process_scroll.add_widget(self.process_container)
        layout.add_widget(self.process_scroll)

        add_ue_button = Button(text='Add UE', on_press=self.open_add_ue_popup, background_color=[0,1,0,1], size_hint_y=None)
        layout.add_widget(add_ue_button)

        self.config_file = ""
        self.ue_type = "clean"
        self.ue_index = 1


        self.add_widget(layout)

    def open_add_ue_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.config_label = Label(text="Selected file: None")
        self.ue_type_label = Label(text=f"UE type: {self.ue_type}")

        cancel_button = Button(text="Cancel", size_hint_y=None, height=50)
        select_config_button = Button(text="Select config", size_hint_y=None, height=50)
        add_button = Button(text="Add", size_hint_y=None, height=50)

        ue_type_spinner = Spinner(
            text='clean',
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
        self.ue_type_label.text = f'UE type: {text}'
        self.ue_type = text

    def add_ue(self, instance):
        self.popup.dismiss()
        new_ue = Ue()
        global attack_args
        if self.ue_type == "clean":
            new_ue.start([self.config_file], self.ue_index)
        else:
            new_ue.start([self.config_file] + attack_args, self.ue_index)
        global ue_list
        ue_list.append({
            'id':str(uuid.uuid4()),
            'type': self.ue_type,
            'config': self.config_file,
            'handle': new_ue
        })
        self.ue_index += 1

        log_view = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=500
        )
        new_ue_text = Label(
            text=f"starting UE ({self.ue_type})...", 
            size_hint_y=None,
            font_size="15sp",
            padding=[10,20,10,20]
        )

        Clock.schedule_interval(lambda dt: self.collect_logs(new_ue_text, new_ue, log_view), 1)
        content_label = Label(
            text=f"sudo srsue {self.config_file} {attack_args}",
            font_size="20sp",
            padding=[10,20,10,20],
        )
        if self.ue_type == "clean":
            content_label.text = f"sudo srsue {self.config_file}"

        log_view.add_widget(content_label)
        log_view.add_widget(new_ue_text)
        self.process_container.add_widget(log_view)

        self.config_file = ""
        self.ue_type = "clean"

    def collect_logs(self, label_ref, ue_ref, log_ref):
        label_ref.text = ue_ref.output
        log_ref.scroll_y = 0



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
        self.layout = GridLayout(cols=3, padding=10, spacing=10)
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

        graph_container = BoxLayout(orientation='vertical')
        canvas_widget = Image(size_hint=(1, 1), keep_ratio=True)
        canvas_label = Label(text=f'Iperf of {str(ue_ref["handle"])}')

        graph_container.add_widget(canvas_widget)
        graph_container.add_widget(canvas_label)


        self.layout.add_widget(graph_container)
       
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

        self.landing = LandingPage(name='landing')
        self.processes = ProcessesPage(name='processes')
        self.attacks = AttacksPage(name='attacks')
        self.results = ResultsPage(name='results')

        self.screen_manager.add_widget(self.landing)
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

        self.button_layout.opacity = 0 
        animationStatus = LandingPage()

        if animationStatus.animation_completed == 1:
                self.button_layout.opacity = 1
        else:
            self.button_layout.opacity = 0  
        Clock.schedule_once(self.load_navigation, 1)

        return main_layout

    def load_navigation(self, *args):
        animate = Animation(opacity=1, duration = 5)
        animate.start(self.button_layout)

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
