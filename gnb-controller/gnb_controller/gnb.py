import time
import threading
#import tailer
import sys
import itertools


from core_interface import CoreNetwork
from gnb_interface import Gnb

def spinner_loading(handle, verbose=True):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not handle.initialized:
        if verbose:
            sys.stdout.write(handle.output + '\n\n' + 50 * '=' + '\n')
        sys.stdout.write(f"{handle.name} " + next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)


def ue_controller():
    
    #recieve configuration
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
    #for line in tailer.follow(open("/etc/gnb.log")):
    	#print(line)
    	#iperf
    return 0

def main():
    gnb_handle = Gnb()
    core_handle = CoreNetwork()
    core_handle.start()
    spinner_loading(core_handle)
    gnb_handle.start([sys.argv[1]])
    spinner_loading(gnb_handle, verbose=False)


if __name__ == '__main__':
    main()
