# Routing configuration
gnb:
```
sudo ip ro add 10.45.0.0/16 via 10.53.1.2
```
ue:
```
sudo ip route add default via 10.45.1.1 dev tun_srsue
```

# Running Iperf
gnb:
```
iperf3 -s -i 1

```
ue:
```
# TCP
iperf3 -c 10.53.1.1 -i 1 -t 60
# or UDP
iperf3 -c 10.53.1.1 -i 1 -t 60 -u -b 10M

```
