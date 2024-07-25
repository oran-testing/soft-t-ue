import time
import threading
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



from ue_interface import Ue
from gnb_interface import Gnb


class ProcessesPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        new_ue = Ue()
        new_ue.start([self.config_file])
        global ue_list
        ue_list.append({
            'type': self.ue_type,
            'config': self.config_file,
            'handle': new_ue
        })

        log_view = ScrollView(size_hint=(1, 0.9))

        new_ue_label = Label(text=f"starting UE ({self.ue_type})...", width=200)
        threading.Thread(target=self.collect_logs, args=(new_ue_label, new_ue, log_view), daemon=True).start()
        content_label = Label(text=f"sudo srsue {self.config_file} ({self.ue_type})")

        self.process_container.add_widget(content_label)
        log_view.add_widget(new_ue_label)
        self.process_container.add_widget(log_view)


        self._update_scroll_height()

        self.config_file = ""
        self.ue_type = "clean"
        self.popup.dismiss()

    def collect_logs(self, label_ref, output_ref, log_ref):
        while True:
            time.sleep(1)
            label_ref.text = output_ref.output
            log_ref.scroll_y = 0

    def _update_scroll_height(self):
        self.process_scroll_wrapper.scroll_y = 0


class AttacksPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='This is Page One')
        layout.add_widget(label)
        self.add_widget(layout)

class ResultsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='This is Page Two')
        layout.add_widget(label)
        self.add_widget(layout)

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
    global ue_list
    ue_list = list()
    MainApp().run()

if __name__ == '__main__':
    main()
