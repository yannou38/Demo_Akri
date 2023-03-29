# Demo_Akri
A Demo for Akri on a k3s cluster
It can run on a single node k3 cluster


Instructions (way more detail on the [wiki](https://github.com/yannou38/Demo_Akri/wiki)):
- Install a k3s single node
- Install a custom docker registry
- Install Loki
- Build the opcua-alerter image and push it on the local repository
- Install Akri in the cluster with the node IP
- Change IP in the opc-ua-sensor-simulator code to set the node IP(it's set as 192.168.236.3)
- Run it with python


What should happen:
the Akri agent should detect the running instance, create a ressource in the cluster, which get used by Akri to create a pod, who will log an error in loki and send a mail to your adress each time a fault occur.
