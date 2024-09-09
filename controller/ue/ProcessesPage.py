from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.clock import Clock

import uuid

from Ue import Ue
from SharedState import SharedState

class ProcessesPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ue_index = SharedState.ue_index
        layout = BoxLayout(orientation='vertical')
        self.process_container = BoxLayout(
            orientation="vertical", 
            size_hint_y=None,
        )
        self.process_container.bind(minimum_height=self.process_container.setter('height'))
        self.process_scroll = ScrollView()
        self.process_scroll.add_widget(self.process_container)
        layout.add_widget(self.process_scroll)

        add_ue_button = Button(text='New UE', on_press=self.open_add_ue_popup, background_color=[0,1,0,1], size_hint_y=None)
        layout.add_widget(add_ue_button)

        self.config_file = ""
        self.ue_type = "clean"

        for ue in SharedState.ue_list:
            self.add_ue_log(ue["type"], ue["config"], [], ue["handle"])

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
        new_ue = Ue(self.ue_index)

        if self.ue_type == "clean":
            new_ue.start([self.config_file])
        else:
            new_ue.start([self.config_file] + SharedState.attack_args)
            
        SharedState.ue_list.append({
            'id': str(uuid.uuid4()),
            'type': self.ue_type,
            'config': self.config_file,
            'handle': new_ue,
            'index': self.ue_index
        })

        self.add_ue_log(self.ue_type, self.config_file, SharedState.attack_args, new_ue)

        self.config_file = ""
        self.ue_type = "clean"
        self.ue_index += 1

    def collect_logs(self, label_ref, ue_ref, log_ref, title_ref):
        label_ref.text = ue_ref.output
        if not ue_ref.isRunning:
            title_ref.color = [1,0,0,1]
        elif not ue_ref.isConnected:
            title_ref.color = [1,1,0,1]
        else:
            title_ref.color = [0,1,0,1]
        log_ref.scroll_y = 0

    def add_ue_log(self, ue_type, config, arguments, handle):
        log_view = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=500
        )
        new_ue_text = Label(
            text=f"starting UE ({ue_type})...", 
            size_hint_y=None,
            font_size="15sp",
            padding=[10,20,10,20]
        )

        content_label = Label(
            text=f"sudo srsue {config}",
            font_size="20sp",
            padding=[10,20,10,20],
        )

        if self.ue_type == "tester":
            content_label.text = f"sudo srsue {config} {arguments}"

        Clock.schedule_interval(lambda dt: self.collect_logs(new_ue_text, handle, log_view, content_label), 1)
        log_view.add_widget(content_label)
        log_view.add_widget(new_ue_text)
        self.process_container.add_widget(log_view)


