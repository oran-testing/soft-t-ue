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

        for process in Config.options.get("processes", []):
            if process["type"] == "tester" or process["type"] == "clean":
                ue = process
                if not os.path.exists(ue["config_file"]):
                    raise ValueError(f"Error: UE config file not found {ue['config_file']}")
                new_ue = Ue(self.ue_index)
                if ue['type'] == "tester":
                    new_ue.start([ue["config_file"]] + ue["args"].split(" "))
                else:
                    new_ue.start([ue["config_file"]])
                self.process_list.append({
                    'id': str(uuid.uuid4()),
                    'type': ue['type'],
                    'config': ue['config_file'],
                    'handle': new_ue,
                    'index': self.ue_index
                })
                self.ue_index += 1
                logger.debug("STARTED:", new_ue)
            else:
                channel = process
                new_channel = None
                channel_config = ""
                if "config_file" in channel.keys():
                    new_channel = ChannelAgent(config_file=channel["config_file"])
                    channel_config = channel["config_file"]
                else:
                    new_channel = ChannelAgent()

                if channel["type"] == "listener":
                    new_channel.sense()
                elif channel["type"] == "jam_fixed":
                    new_channel.jam_fixed()
                elif channel["type"] == "jam_sequential":
                    new_channel.jam_sequential()
                elif channel["type"] == "jam_random":
                    new_channel.jam_random()

                self.process_list.append({
                    'id': str(uuid.uuid4()),
                    'type': channel['type'],
                    'config': channel_config,
                    'handle': new_channel,
                    'index': self.channel_index
                })
                self.channel_index += 1
