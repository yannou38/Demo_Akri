# Demo_Akri
A Demo for Akri on a k3s cluster
It can run on a single node k3 cluster


Demo:
Install a k3s single node (link TODO)
Install a custom docker registry (link TODO)
Install Loki (link TODO)
Build the opcua-alerter image and push it on the local repository
Install Akri in the cluster with the node IP

Change IP in the opc-ua-sensor-simulator code to set the node IP(it's set as 192.168.236.3)
run it with python


What should happen:
the Akri agent should detect the running instance, create a ressource in the cluster, which get used by Akri to create a pod, who will log an error in loki and send a mail to your adress each time a fault occur.