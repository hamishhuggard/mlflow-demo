- ClusterIP lets other nodes in the cluster access this pod
  - NodePort also lets traffic from outside thecluster access this pod
  - LoadBalancer also does loadbalancing (only available on EKS, AKS, etc)
- An Ingress 
- The configmap stores non-confidential key-value pairs (eg, configs)
  - You can mount the configmap as a file or as env variables
- In a secret you'd store passwords, OAuth tokens, SSH keys, etc
  - The "opaque" means that kubernetes shouldn't try to parse/validate the secret. It's not a jsonconfig or TLS cert. It's just normal key/value pairs.
- A configmap is basically a .env file
    - You can specify in other pods that you want the content of the configmap as env variables or as files


LoadBalancer vs Ingress:
- LoadBalancer:
    - operates at TCP/UDP layer.
    - doesn't do routing
    - doesn't handle SSL termination
- Ingress:
    - Application (HTTP/s) layer
    - reverse proxy and load balancing
    - handles name-based hosting (app.example.com, admin.example.com, api.example.com)
        - this way, all hosts can point to the same IP address in the DNS system
        - without it, you'd need the DNS to point to different IPs for each hostname
    - also handles path routing (/api, /user/1, /settings)
- You'd typically have the loadBalancer gating access from the Ingress to the outside world: world -> LoadBalancer -> Ingress -> Pods
