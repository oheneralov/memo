# Kubernetes API Deployment Test Cases

## Basic Deployment Tests

### Test 1: Deploy Microservice
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get deployments
kubectl get services
```

### Test 2: Check Pod Status
```bash
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Test 3: Verify Health Checks
```bash
kubectl port-forward svc/microservice-api 8080:80
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready
```

## Service Tests

### Test 4: Test ClusterIP Service
```bash
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  wget -O- http://microservice-api.default.svc.cluster.local/api/v1
```

### Test 5: Test NodePort Service
```bash
kubectl get services -o wide
# Access via <node-ip>:30001
curl http://<node-ip>:30001/
```

### Test 6: Test LoadBalancer Service
```bash
kubectl get services microservice-api-lb
# Wait for EXTERNAL-IP to be assigned
curl http://<external-ip>/
```

## Ingress Tests

### Test 7: Configure Local DNS (Optional)
```bash
# Add to /etc/hosts or hosts file
# <ingress-ip> api.example.com
```

### Test 8: Test Ingress
```bash
kubectl get ingress
kubectl describe ingress microservice-ingress
curl -H "Host: api.example.com" http://<ingress-ip>/api/v1
```

## Scaling Tests

### Test 9: Manual Scaling
```bash
kubectl scale deployment microservice-api --replicas=5
kubectl get pods -w
```

### Test 10: HPA Scaling
```bash
kubectl apply -f hpa.yaml
kubectl get hpa -w
# Generate load to trigger scaling
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- \
  /bin/sh -c "while sleep 0.01; do wget -q -O- http://microservice-api; done"
```

## Configuration Tests

### Test 11: ConfigMap
```bash
kubectl get configmap microservice-config -o yaml
kubectl edit configmap microservice-config
kubectl rollout restart deployment/microservice-api
```

### Test 12: Secrets
```bash
kubectl get secret microservice-secrets -o yaml
kubectl describe secret microservice-secrets
```

## RBAC Tests

### Test 13: Service Account Permissions
```bash
kubectl get serviceaccount microservice-api -o yaml
kubectl get role microservice-api -o yaml
kubectl get rolebinding microservice-api -o yaml
```

## Helm Chart Tests

### Test 14: Helm Template Rendering
```bash
helm template microservice-api ./kubernetes/helm
helm template microservice-api ./kubernetes/helm --values values-production.yaml
```

### Test 15: Helm Dry Run
```bash
helm install microservice-api ./kubernetes/helm --dry-run --debug
helm upgrade microservice-api ./kubernetes/helm --dry-run --debug
```

### Test 16: Helm Lint
```bash
helm lint ./kubernetes/helm
```

### Test 17: Helm Install
```bash
helm install microservice-api ./kubernetes/helm
helm get values microservice-api
helm get manifest microservice-api
```

### Test 18: Helm Upgrade
```bash
helm upgrade microservice-api ./kubernetes/helm --values values-production.yaml
helm rollback microservice-api 0
```

## Cleanup

### Remove Helm Release
```bash
helm uninstall microservice-api
```

### Remove Kubernetes Resources
```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f ingress.yaml
kubectl delete -f hpa.yaml
kubectl delete -f rbac.yaml
kubectl delete -f configmap.yaml
kubectl delete -f secret.yaml
```

## Performance Tests

### Test 19: Load Testing
```bash
# Using Apache Bench
ab -n 10000 -c 100 http://microservice-api/api/v1

# Using Apache Bench with LoadBalancer
ab -n 10000 -c 100 http://<lb-ip>/api/v1
```

### Test 20: Monitor Resource Usage
```bash
kubectl top pods -n default
kubectl top nodes
```

## Monitoring

### Check Prometheus Metrics
```bash
kubectl port-forward svc/microservice-api 9090:9090
# Access http://localhost:9090
```

### View Event Logs
```bash
kubectl get events -n default
kubectl describe pod <pod-name>
```
