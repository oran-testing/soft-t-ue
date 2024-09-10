from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation


from common.utils import send_command

from LandingPage import LandingPage
from ProcessesPage import ProcessesPage
from AttacksPage import AttacksPage
from ResultsPage import ResultsPage
from SharedState import SharedState

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
        Clock.schedule_once(self.load_navigation, 0.25)

        return main_layout

    def load_navigation(self, *args):
        animate = Animation(opacity=1, duration=2)
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

    def on_stop(self):
        print("App is stopping...")
        send_command(SharedState.cli_args.ip, SharedState.cli_args.port, "gnb:stop")
        for process in SharedState.process_list:
            process["handle"].stop()


