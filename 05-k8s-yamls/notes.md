- ClusterIP lets other nodes in the cluster access this pod
  - NodePort also lets traffic from outside thecluster access this pod
  - LoadBalancer also does loadbalancing (only available on EKS, AKS, etc)
- The configmap stores non-confidential key-value pairs (eg, configs)
  - You can mount the configmap as a file or as env variables
- In a secret you'd store passwords, OAuth tokens, SSH keys, etc

