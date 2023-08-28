kubectl port-forward -n openfaas svc/prometheus 9091:9090
kubectl port-forward -n openfaas svc/gateway 8080:8080