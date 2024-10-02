from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from SharedState import SharedState
from kivy.uix.textinput import TextInput


class AttacksPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.title = Label(text="", font_size="32sp")
        self.layout.add_widget(self.title)
        attack_option = Spinner(
            text='imsi_capture',
            values=(
                'rrc_random_fuzzing',
                'rrc_selective_fuzzing',
                'rrc_signal_flooding',
                'cqi_manipulation',
                'rach_jamming',
                'rach_replay',
                'rach_collision',
                'rach_flooding',
                'gnb_impersonation',
                'random_jamming',
                'fixed_jamming',
                'sequential_jamming',
                'targeted_replay',
                'targeted_spoofing',
                'fronthaul_dos',
                'uhd_dos'
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
        self.attack_widgets = []

    def set_attack_type(self, spinner, text):
        self.attack_type = text

        for spinner in self.attack_widgets:
            self.layout.remove_widget(spinner)
        self.attack_widgets = []
        # TODO: make functions for each attack type
        getattr(self, "set_" + text)()


        # TODO: Document each attack in detail
        new_doc = RstDocument(source=f"../../docs/attacks/{text}.rst",)
        self.layout.add_widget(new_doc)
        if self.previous_doc:
            self.layout.remove_widget(self.previous_doc)
        self.previous_doc = new_doc

    def set_rrc_random_fuzzing(self):

        target_message = Spinner(
            text='All',
            values=('All', 'rrcSetupRequest','rrcRegistrationRequest'),
            size_hint=(None, None),
            size=(400, 44)
        )
        bits_to_fuzz = TextInput(
            hint_text='Number of Bits to Fuzz',
            multiline=False,
            font_size=32,
            size_hint=(None, None),
            size=(200, 44)
        )
        bits_to_fuzz.bind(text= lambda widget, text : self.rrc_random_fuzzing(text, target_message.text))
        self.layout.add_widget(target_message)
        self.layout.add_widget(bits_to_fuzz)
        self.attack_widgets.append(target_message)
        self.attack_widgets.append(bits_to_fuzz)


    def rrc_random_fuzzing(self, bits_text, target_text):
        if target_text != "All":
            SharedState.attack_args = ["--rrc.sdu_fuzzed_bits", str(bits_text),
                           "--rrc.fuzz_target_message", target_text]
            self.title.text = f"--rrc.sdu_fuzzed_bits {bits_text} --rrc.fuzz_target_message {target_text}"
        else:
            SharedState.attack_args = ["--rrc.sdu_fuzzed_bits", str(bits_text)]
            self.title.text = f"--rrc.sdu_fuzzed_bits {bits_text}"

    def set_cqi_manipulation(self):
        cqi_value = TextInput(
            hint_text='CQI Value',
            size_hint=(None, None),
            size=(200, 44),
            font_size=32,
        )
        cqi_value.bind(text=self.cqi_manipulation)
        self.layout.add_widget(cqi_value)
        self.attack_widgets.append(cqi_value)


    def cqi_manipulation(self, spinner, text):
        SharedState.attack_args = ["--phy.cqi_max", text, "--phy.cqi_fixed", text]
        self.title.text = f"--phy.cqi_max {text} --phy.cqi_fixed {text}"


