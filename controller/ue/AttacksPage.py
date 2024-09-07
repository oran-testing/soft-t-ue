from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument

from SharedState import SharedState


class AttacksPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        attack_option = Spinner(
            text='imsi_capture',
            values=(
                'sdu_fuzzing',
                'cqi_manipulation',
                'rrc_signal_flooding',
                'rach_jamming',
                'rach_replay',
                'preamble_collision',
                'rach_signal_flooding',
                'imsi_capture',
            ),
            size_hint=(None, None),
            size=(400, 30)
        )
        attack_option.bind(text=self.set_attack_type)
        self.layout.add_widget(attack_option)
        self.attack_type = "None"
        self.add_widget(self.layout)
        self.num_fuzzed_bits = 1
        self.target_message = "All"
        self.previous_doc = RstDocument(source=f"../../docs/attacks/imsi_capture.rst",)
        self.layout.add_widget(self.previous_doc)
        self.previous_spinners = []

    def set_attack_type(self, spinner, text):
        self.attack_type = text

        for spinner in self.previous_spinners:
            self.layout.remove_widget(spinner)
        self.previous_spinners = []

        if text == "sdu_fuzzing":
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
            self.layout.add_widget(target_message)
            self.layout.add_widget(bits_to_fuzz)
            self.previous_spinners.append(target_message)
            self.previous_spinners.append(bits_to_fuzz)
        if text == "CQI Manipulation":
            cqi_value = Spinner(
                text='CQI Value',
                values=[str(i * 100) for i in range(10)],
                size_hint=(None, None),
                size=(200, 44)
            )
            cqi_value.bind(text=self.set_cqi_value)
            self.layout.add_widget(cqi_value)
            self.previous_spinners.append(cqi_value)

        new_doc = RstDocument(source=f"../../docs/attacks/{text}.rst",)
        self.layout.add_widget(new_doc)
        if self.previous_doc:
            self.layout.remove_widget(self.previous_doc)
        self.previous_doc = new_doc


    def set_target_message(self, spinner, text):
        self.target_message = text
        if text != "All":
            SharedState.attack_args = ["--rrc.sdu_fuzzed_bits", str(self.num_fuzzed_bits)
                           , "--rrc.fuzz_target_message", self.target_message]
            self.title.text = f"--rrc.sdu_fuzzed_bits {self.num_fuzzed_bits} --rrc.fuzz_target_message {self.target_message}"

    def set_fuzzed_bits(self, spinner, text):
        self.num_fuzzed_bits = int(text)
        SharedState.attack_args = ["--rrc.sdu_fuzzed_bits", str(self.num_fuzzed_bits)
                       , "--rrc.fuzz_target_message", self.target_message]
        self.title.text = f"--rrc.sdu_fuzzed_bits {self.num_fuzzed_bits} --rrc.fuzz_target_message {self.target_message}"

    def set_cqi_value(self, spinner, text):
        SharedState.attack_args = ["--phy.cqi_max", text, "--phy.cqi_fixed", text]
        self.title.text = f"--phy.cqi_max {text} --phy.cqi_fixed {text}"


