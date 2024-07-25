import time
import threading
import tailer
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

def ue_controller():
    #connect to ue controller
    
    #recieve configuration
    self.config_file = "idk"
    #start gnb and core
    gnb_thread = threading.Thread(target=start_gnb).start()
    #core_thread = threading.Thread(target=start_core).start()
    
    #thread sending metrics
    #metrics_thread = threading.Thread(target=metrics).start()
    #wait for restart message from ue controller
    	#stop gnb, core, metrics, etc
    	#run a variation of main without calling ue_controller
    
def metrics():
    #get metrics
    	#KPIs
    	#crashes
    	#PCAP between gNB and core
    	#all logging
    for line in tailer.follow(open("/etc/gnb.log")):
    	print(line)
    	#iperf
    return 0

def start_gnb():
    gnb = Gnb()
    gnb.start([self.config_file])
    
#def start_core(self, instance):
    #make sure core isn't already running
    #run core

def main():
    ue_controller()
    

if __name__ == '__main__':
    main()
