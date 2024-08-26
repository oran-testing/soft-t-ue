# How to run srsRAN with multiple Ues:
https://docs.srsran.com/projects/project/en/latest/tutorials/source/srsUE/source/index.html#multi-ue-emulation

Open5gs:

```
cd ./srsRAN_Project/docker
docker compose up --build 5gc
```

gNB:
```
cd ./srsRAN_Project/build/apps/gnb
sudo ./gnb -c gnb_zmq.yaml
```

Net namespaces:
```
sudo ip netns add ue1
sudo ip netns add ue2
sudo ip netns add ue3
```

srsUE:
```
cd ./srsRAN_4G/build/srsue/src
sudo ./srsue ./ue1_zmq.conf
sudo ./srsue ./ue2_zmq.conf
sudo ./srsue ./ue3_zmq.conf
```

gnb radio:
```
sudo gnuradio-companion ./multi_ue_scenario.grc
```
