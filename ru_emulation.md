# Running srsRAN RU emulator

There are three main parts to running emulator:
1. Setting up DPDK
2. Running a testing gNB
3. Running the RU emulator itself



## Step 1: setting up DPDK

In detail instructions on installing DPDK can be found ![here](https://docs.srsran.com/projects/project/en/latest/tutorials/source/dpdk/source/index.html)

Once it is installed run the following commands to bind the correct pci device:

to find the pci address:
`sudo dpdk-devbind -s`

to bind that address to vfio-pci:
```
sudo dpdk-devbind --unbind 0000:01:00.0
sudo dpdk-devbind --bind vfio-pci 0000:01:00.0
```
rerun this command to verify:
`sudo dpdk-devbind -s`

this should be the output:
> 0000:01:00.1 82599ES 10-Gigabit SFI/SFP+ Network Connection 10fb if=enp1s0f1 drv=vfio-pci unused=igb_uio,uio_pci_generic,ixgbe

## Step 2: running the testing gNB

Create a minimal config file ~/gnb.yml, then run the following:
```
cat << EOF > ~/gnb.yml
ru_ofh: 
  gps_alpha: 0 
  gps_beta: 0 
  ru_bandwidth_MHz: 20  
  t1a_max_cp_dl: 500   
  t1a_min_cp_dl: 258  
  t1a_max_cp_ul: 500 
  t1a_min_cp_ul: 258
  t1a_max_up: 300  
  t1a_min_up: 85  
  ta4_max: 300   
  ta4_min: 85   
  is_prach_cp_enabled: true   
  is_dl_broadcast_enabled: false
  ignore_ecpri_seq_id: false  
  ignore_ecpri_payload_size: false
  warn_unreceived_ru_frames: true
  compr_method_ul: bfp        
  compr_bitwidth_ul: 9       
  compr_method_dl: bfp      
  compr_bitwidth_dl: 9     
  compr_method_prach: bfp 
  compr_bitwidth_prach: 9
  enable_ul_static_compr_hdr: true   
  enable_dl_static_compr_hdr: true  
  iq_scaling: 0.35                 
  cells:
    - network_interface: 0000:17:00.0
      ru_mac_addr: 80:61:5f:0d:df:ab
      du_mac_addr: 64:b3:79:10:00:37
      vlan_tag_cp: 2               
      vlan_tag_up: 2              
      prach_port_id: [4,5]       
      dl_port_id: [0,1]         
      ul_port_id: [0,1]          

cell_cfg:
  dl_arfcn: 637212                                               
  band: 78                                                       
  channel_bandwidth_MHz: 20                                     
  common_scs: 30                                                 
  plmn: "00101"                                                  
  tac: 7                                                         
  pci: 1                                                         
  nof_antennas_dl: 2                                             
  nof_antennas_ul: 2                                             
  prach:
    prach_config_index: 7                                        
    prach_root_sequence_index: 1                                 
    zero_correlation_zone: 0                                     
    prach_frequency_start: 0                                     
  tdd_ul_dl_cfg:
    dl_ul_tx_period: 10                                          
    nof_dl_slots: 7                                              
    nof_dl_symbols: 6                                            
    nof_ul_slots: 2                                              
    nof_ul_symbols: 4

hal:
  eal_args: "--lcores (0-1)@(0-15) -a 0000:17:00.0"
EOF
```

Then run the gNB in test mode: `sudo ./gnb -c ~/gnb.yml amf --no_core true test_mode test_ue --rnti 0x1 --ri 2`

once the RU emulator is functional run without the test ue and use the soft T-UE

## Step 3: running the RU emulator

create a file ~/ru_em.yaml and run the following:
```
cat << EOF > ~/ru_em.yaml
log:
  filename: /tmp/ru_em.log
  level: warning

dpdk:
  eal_args: "--lcores (0-1)@(0-15)"

ru_emu:
  cells:
  - bandwidth: 100
    network_interface: 0000:01:00.0
    ru_mac_addr: 80:61:5f:0d:df:ab
    du_mac_addr: 64:b3:79:10:00:37
    vlan_tag: 2
    ul_port_id: [0]
    compr_method_ul: "bfp"
    compr_bitwidth_ul: 9
EOF
```

the run the following to start the RU:
```
cd ~/srsRAN_Project/build/tests/integrationtests/ofh/
sudo ./ru_emulator -c ~/ru_em.yml
```

Then the output should be:
```
> EAL: Detected CPU lcores: 16
> EAL: Detected NUMA nodes: 1
> EAL: Detected shared linkage of DPDK
> EAL: Multi-process socket /var/run/dpdk/rte/mp_socket
> EAL: Selected IOVA mode 'VA'
> EAL: VFIO support initialized
> EAL: Using IOMMU type 1 (Type 1)
> EAL: Ignore mapping IO port bar(2)
> EAL: Probe PCI driver: net_ixgbe (8086:10fb) device: 0000:01:00.1 (socket -1)
> TELEMETRY: No legacy callbacks, legacy socket not created
> Running. Waiting for incoming packets...
> Cell #0: 2024-03-15 17:08:11 Received 14 UL C-Plane packets
> Cell #0: 2024-03-15 17:08:12 Received 401 UL C-Plane packets
> Cell #0: 2024-03-15 17:08:13 Received 795 UL C-Plane packets
> Cell #0: 2024-03-15 17:08:14 Received 1195 UL C-Plane packets
> Cell #0: 2024-03-15 17:08:15 Received 1595 UL C-Plane packets
```
