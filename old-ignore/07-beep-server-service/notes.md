kubectl apply -f beep-pod.yaml
kubectl port-forward pod/beep-pod 5002:5000
kubectl delete -f beep-pod.yaml
