import uuid

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

from Ue import Ue
from ChannelAgent import ChannelAgent
from Monitor import Monitor


class ProcessesPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ue_index = 1
        self.channel_index = 1
        self.process_list = []

