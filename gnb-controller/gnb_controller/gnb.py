import time
import threading
import tailer
import sys
import itertools

from core_interface import CoreNetwork
from gnb_interface import Gnb

class ue_controller:
    def __init__(self):
    	self.reset_file('/tmp/gnb.log')
    	    
    def reset_file(self, filename):
    	with open(filename, 'w') as file:
    	    pass

    def start(self):
    	#connect to ue controller
    	
    	#recieve configuration
    	
    	#start gnb and core
    	gnb_thread = threading.Thread(target=self.start_gnb).start()
    	core_thread = threading.Thread(target=self.start_core).start()
    
    	#sending metrics
    	self.metrics()
    	#wait for restart message from ue controller
    		#stop gnb, core, metrics, etc
    		#run a variation of main without calling ue_controller
    
    def metrics(self):
    	#get metrics
    	#KPIs
    	#crashes
    	#PCAP between gNB and core
    	#all logging
    	gnb_logs = threading.Thread(target=self.get_gnb_logs).start()
    	#iperf
    	
    def get_gnb_logs(self):
    	for line in tailer.follow(open('/tmp/gnb.log')):
    	    print(line) #replace with send_log

    def spinner_loading(self, handle, verbose=True):
    	spinner = itertools.cycle(['|', '/', '-', '\\'])
    	while not handle.initialized:
            if verbose:
            	sys.stdout.write(handle.output + '\n\n' + 50 * '=' + '\n')
            sys.stdout.write(f"{handle.name} " + next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(0.1)
            
    def start_gnb(self):
    	gnb_handle = Gnb()
    	gnb_handle.start([sys.argv[0]])
    	self.spinner_loading(gnb_handle, verbose=False)

    
    def start_core(self):
    	core_handle = CoreNetwork()
    	core_handle.start()
    	self.spinner_loading(core_handle)

def main():
    controller = ue_controller()
    controller.start()
    

if __name__ == '__main__':
    main()
