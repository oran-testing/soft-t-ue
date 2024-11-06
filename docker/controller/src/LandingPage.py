from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen


class LandingPage(Screen):

    def __init__(self, **kwargs):
        self.animation_completed = 0
        super().__init__(**kwargs)

        layout = RelativeLayout()
        self.background = Image(source='assets/Webimage.png', allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.background)
        self.welcome_label = Label(
            text="NTIA Soft T UE",
            font_size='60sp',
            halign='center',
            valign='middle'
        )
    
        self.welcome_label.bind(size=self.welcome_label.setter('text_size'))
        layout.add_widget(self.welcome_label)
        self.welcome_label.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.animate_transition, 1)

    def animate_transition(self, *args):
        anim = Animation(opacity=0, duration=1)
        anim.start(self.welcome_label)
        anim.start(self.background) 

        self.animation_completed = 1

