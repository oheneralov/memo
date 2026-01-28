# Kubernetes Microservice Architecture

This directory contains complete Kubernetes configuration files and Helm charts for deploying microservices with production-ready patterns.

## Directory Structure

```
kubernetes/
├── deployment.yaml          # Deployment with health checks and resource management
├── service.yaml             # ClusterIP, NodePort, and LoadBalancer services
├── ingress.yaml             # Ingress controller with TLS
├── configmap.yaml           # Configuration management
├── secret.yaml              # Secret management
├── rbac.yaml                # Role-based access control
├── hpa.yaml                 # Horizontal Pod Autoscaler
└── helm/                    # Helm chart for reusable deployments
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── _helpers.tpl
        ├── deployment.yaml
        ├── service.yaml
        ├── ingress.yaml
        ├── configmap.yaml
        ├── secret.yaml
        ├── serviceaccount.yaml
        └── hpa.yaml
```

## Quick Start

### Deploy using kubectl

```bash
# Apply all configurations
kubectl apply -f kubernetes/

# Verify deployment
kubectl get deployments
kubectl get services
kubectl get ingress
kubectl get hpa
```

### Deploy using Helm

```bash
# Install the chart
helm install microservice-api kubernetes/helm/

# Upgrade the chart
helm upgrade microservice-api kubernetes/helm/

# Uninstall the chart
helm uninstall microservice-api

# Install with custom values
helm install microservice-api kubernetes/helm/ -f custom-values.yaml
```

## Configuration Files

### Deployment (deployment.yaml)
- **Replicas**: 3 (configurable via Helm)
- **Strategy**: Rolling update with 0 downtime
- **Resources**: CPU (250m-500m), Memory (256Mi-512Mi)
- **Health Checks**: Liveness and Readiness probes
- **Pod Anti-Affinity**: Spreads pods across nodes
- **Volume Mounts**: Config, logs, and temp storage

### Services (service.yaml)
1. **ClusterIP Service**: For internal communication
2. **NodePort Service**: For node-level access (port 30001)
3. **LoadBalancer Service**: For cloud provider load balancing with:
   - External traffic policy: Local
   - Health check node port: 30002
   - Session affinity: ClientIP

### Ingress (ingress.yaml)
- **Controller**: nginx
- **TLS**: Let's Encrypt with cert-manager
- **Paths**: /api/v1 and /api/v2
- **Rate Limiting**: 100 requests per second
- **SSL Redirect**: Enabled

### ConfigMap (configmap.yaml)
- Database configuration
- Redis configuration
- API version
- Application settings (YAML)

### Secrets (secret.yaml)
- Database password (base64 encoded)
- API key
- JWT secret

### RBAC (rbac.yaml)
- ServiceAccount creation
- Role with minimal permissions
- RoleBinding for pod access to ConfigMaps and Secrets

## YAML Structure and Fields

### Secret (secret.yaml) - Detailed Breakdown

```yaml
apiVersion: v1                          # Kubernetes API version
kind: Secret                            # Resource type
metadata:                               # Metadata section
  name: microservice-secrets            # Unique name within namespace
  namespace: default                    # Kubernetes namespace
  labels:                               # Key-value labels for organization
    app: microservice-api
type: Opaque                            # Secret type (Opaque, kubernetes.io/service-account-token, etc.)
data:                                   # Base64-encoded key-value pairs
  database_password: cGFzc3dvcmQxMjM=  # base64 encoded: password123
  api_key: YWxwaV9rZXlfMTIz            # base64 encoded: api_key_123
  jwt_secret: and0X3NlY3JldF9zdXBlcl9zZWN1cmU=  # base64 encoded: jwt_secret_super_secure
```

**Field Descriptions:**
- `apiVersion`: The Kubernetes API group and version (v1 for core resources)
- `kind`: The type of Kubernetes resource (Secret, Deployment, Service, etc.)
- `metadata.name`: Unique identifier for the resource within the namespace
- `metadata.namespace`: Logical partition (default: "default")
- `metadata.labels`: Key-value pairs for organization, selection, and identification
- `type`: Specifies the secret type (Opaque for user-defined)
- `data`: Contains base64-encoded sensitive information

**To encode secrets:**
```bash
echo -n "password123" | base64
# Output: cGFzc3dvcmQxMjM=
```

### Deployment (deployment.yaml) - Detailed Breakdown

```yaml
apiVersion: apps/v1                     # API version for workload resources
kind: Deployment                        # Resource type for stateless workloads
metadata:
  name: microservice-api                # Deployment name
  namespace: default
  labels:
    app: microservice-api
spec:                                   # Deployment specification
  replicas: 3                           # Desired number of pod replicas
  strategy:                             # Update strategy
    type: RollingUpdate                 # Gradual replacement of pods
    rollingUpdate:
      maxSurge: 1                       # Max pods above desired count during update
      maxUnavailable: 0                 # Max pods that can be unavailable
  selector:                             # Label selector to find pods
    matchLabels:
      app: microservice-api
  template:                             # Pod template specification
    metadata:
      labels:
        app: microservice-api
      annotations:                      # Metadata for tools (Prometheus, etc.)
        prometheus.io/scrape: "true"
    spec:                               # Pod specification
      serviceAccountName: microservice-api  # ServiceAccount for RBAC
      containers:                       # List of containers
      - name: microservice-api          # Container name
        image: microservice-api:1.0.0   # Docker image name:tag
        imagePullPolicy: IfNotPresent   # When to pull image
        ports:                          # Exposed ports
        - name: http
          containerPort: 8080           # Port inside container
          protocol: TCP
        env:                            # Environment variables
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_PASSWORD       # Reference secret
          valueFrom:
            secretKeyRef:
              name: microservice-secrets
              key: database_password
        resources:                      # CPU and memory limits
          requests:                     # Minimum guaranteed resources
            cpu: 250m                   # Millicores (250m = 0.25 CPU)
            memory: 256Mi               # Mebibytes
          limits:                       # Maximum allowed resources
            cpu: 500m
            memory: 512Mi
        livenessProbe:                  # Is container alive?
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30       # Wait before first check
          periodSeconds: 10             # Check interval
          failureThreshold: 3           # Failed checks to restart
        readinessProbe:                 # Is container ready for traffic?
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:                   # Mount volumes
        - name: config
          mountPath: /etc/config        # Path inside container
          readOnly: true                # Read-only mount
      volumes:                          # Define volumes
      - name: config
        configMap:
          name: microservice-config     # ConfigMap to mount
      affinity:                         # Pod scheduling rules
        podAntiAffinity:                # Avoid scheduling on same node
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100                 # Soft preference (1-100)
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - microservice-api
              topologyKey: kubernetes.io/hostname  # Spread across nodes
      terminationGracePeriodSeconds: 30 # Wait before forcefully terminating
```

### Service (service.yaml) - Detailed Breakdown

```yaml
---
# ClusterIP Service (Internal)
apiVersion: v1
kind: Service
metadata:
  name: microservice-api
  labels:
    app: microservice-api
spec:
  type: ClusterIP                       # Service type (ClusterIP, NodePort, LoadBalancer)
  selector:                             # Label selector to find backing pods
    app: microservice-api
  ports:                                # Port mappings
  - name: http
    port: 80                            # Service port (exposed)
    targetPort: 8080                    # Container port (where service forwards to)
    protocol: TCP
  sessionAffinity: None                 # Route same client to same pod

---
# LoadBalancer Service (External)
apiVersion: v1
kind: Service
metadata:
  name: microservice-api-lb
spec:
  type: LoadBalancer                    # Cloud provider load balancer
  selector:
    app: microservice-api
  ports:
  - name: http
    port: 80
    targetPort: 8080
  externalTrafficPolicy: Local          # Preserve source IP, no cross-node forwarding
```

**Service Types:**
- **ClusterIP**: Internal-only service with stable cluster IP (default)
- **NodePort**: External access via `<node-ip>:<node-port>`
- **LoadBalancer**: Cloud provider external load balancer

### ConfigMap (configmap.yaml) - Detailed Breakdown

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: microservice-config
  labels:
    app: microservice-api
data:                                   # Non-sensitive configuration data
  database_host: "postgres.default.svc.cluster.local"
  database_port: "5432"
  redis_host: "redis.default.svc.cluster.local"
  redis_port: "6379"
  api_version: "v1"
  app_config.yaml: |                    # Multi-line YAML value
    server:
      port: 8080
      timeout: 30s
    database:
      pool_size: 10
```

**Key Differences from Secret:**
- ConfigMap: Non-sensitive configuration (plain text)
- Secret: Sensitive data (base64 encoded)
- ConfigMaps are larger (~1MB limit)
- Secrets are smaller (~1MB limit)

### Ingress (ingress.yaml) - Detailed Breakdown

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: microservice-ingress
  annotations:                          # Ingress controller configuration
    kubernetes.io/ingress.class: nginx  # Which controller to use
    cert-manager.io/cluster-issuer: letsencrypt-prod  # TLS issuer
spec:
  tls:                                  # TLS/HTTPS configuration
  - hosts:
    - api.example.com                   # Domain name
    secretName: microservice-tls        # Where to store certificate
  rules:                                # Routing rules
  - host: api.example.com               # Hostname
    http:
      paths:
      - path: /api/v1                   # URL path prefix
        pathType: Prefix                # Prefix or Exact matching
        backend:
          service:
            name: microservice-api      # Target service
            port:
              number: 80                # Target service port
```

### Horizontal Pod Autoscaler (hpa.yaml) - Detailed Breakdown

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: microservice-api-hpa
spec:
  scaleTargetRef:                       # What to scale
    apiVersion: apps/v1
    kind: Deployment
    name: microservice-api
  minReplicas: 2                        # Minimum pods
  maxReplicas: 10                       # Maximum pods
  metrics:                              # Scaling triggers
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization               # % of requests
        averageUtilization: 70          # Scale up if avg > 70%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:                             # Scaling behavior
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait before scaling down
      policies:
      - type: Percent
        value: 50                       # Remove max 50% of pods
        periodSeconds: 60               # Check interval
    scaleUp:
      stabilizationWindowSeconds: 0     # Scale up immediately
      policies:
      - type: Percent
        value: 100                      # Add up to 100% (double) of pods
        periodSeconds: 30
```

### RBAC (rbac.yaml) - Detailed Breakdown

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: microservice-api                # ServiceAccount for pods to authenticate
  namespace: default

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: microservice-api
rules:                                  # Permissions
  - apiGroups: [""]                     # Core API group
    resources: ["configmaps"]           # What resource
    verbs: ["get", "list", "watch"]     # What actions (get, list, create, delete)

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: microservice-api
roleRef:                                # Reference to role
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: microservice-api
subjects:                               # Who gets this role
  - kind: ServiceAccount
    name: microservice-api
    namespace: default
```

### StatefulSet (statefulset.yaml) - Detailed Breakdown

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: microservice-stateful
spec:
  serviceName: microservice-stateful    # Headless service name (IMPORTANT)
  replicas: 3                           # Number of replicas
  selector:
    matchLabels:
      app: microservice-stateful
  template:                             # Pod template (same as Deployment)
    metadata:
      labels:
        app: microservice-stateful
    spec:
      containers:
      - name: microservice-stateful
        image: microservice-stateful:1.0.0
        volumeMounts:
        - name: data
          mountPath: /data              # Where to mount persistent storage
  volumeClaimTemplates:                 # Create PVC for each replica
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]    # How volume can be accessed
      storageClassName: standard        # Storage class (provider-specific)
      resources:
        requests:
          storage: 10Gi                 # Requested storage size
```

**Pod Naming in StatefulSet:**
- Pod 0: `microservice-stateful-0`
- Pod 1: `microservice-stateful-1`
- Pod 2: `microservice-stateful-2`
- DNS: `microservice-stateful-0.microservice-stateful.default.svc.cluster.local`

## Common Kubernetes Patterns

### Label Selectors
Labels allow organizing and selecting resources:
```yaml
labels:
  app: microservice-api       # Application name
  version: v1                 # Version
  environment: production     # Environment
```

### Environment Variables (3 methods)
```yaml
env:
  # 1. Direct value
  - name: DIRECT_VALUE
    value: "hello"
  
  # 2. From ConfigMap
  - name: CONFIG_VALUE
    valueFrom:
      configMapKeyRef:
        name: microservice-config
        key: database_host
  
  # 3. From Secret
  - name: SECRET_VALUE
    valueFrom:
      secretKeyRef:
        name: microservice-secrets
        key: database_password
  
  # 4. From Pod metadata
  - name: POD_NAME
    valueFrom:
      fieldRef:
        fieldPath: metadata.name
```

### Resource Requests and Limits
```yaml
resources:
  requests:                   # Guaranteed resources
    cpu: 250m                 # 0.25 CPU cores
    memory: 256Mi             # 256 Mebibytes
  limits:                     # Maximum resources
    cpu: 500m                 # 0.5 CPU cores
    memory: 512Mi
```

**CPU Units:** 1000m (millicores) = 1 core
**Memory Units:** 1Mi (Mebibyte) = 1024 KiB, 1Gi = 1024 Mi

### HPA (hpa.yaml)
- Min replicas: 2
- Max replicas: 10
- CPU target: 70% utilization
- Memory target: 80% utilization
- Scale-up policies: 100% increase or 2 pods per 30s
- Scale-down policies: 50% decrease per 60s

### StatefulSet (statefulset.yaml)
- Ordered, stable pod identity
- Persistent storage with volumeClaimTemplates
- Headless service for DNS
- Pod naming: `<statefulset-name>-0`, `<statefulset-name>-1`, etc.
- Graceful deployment and scaling
- Optional LoadBalancer service
- HPA support with min 2, max 5 replicas

## Helm Chart

### values.yaml
Highly customizable values for:
- Image repository and tag
- Replica count and autoscaling
- Resource limits and requests
- Service types (ClusterIP, LoadBalancer)
- Ingress configuration
- Environment variables
- Database and Redis configuration
- Secrets management

### Templates
- `_helpers.tpl`: Template helper functions
- `deployment.yaml`: Deployment template
- `service.yaml`: Service template (ClusterIP + LoadBalancer)
- `ingress.yaml`: Ingress template
- `configmap.yaml`: ConfigMap template
- `secret.yaml`: Secret template
- `serviceaccount.yaml`: ServiceAccount and RBAC
- `hpa.yaml`: HorizontalPodAutoscaler template
- `statefulset.yaml`: StatefulSet template for stateful workloads
- `service-stateful.yaml`: Headless and LoadBalancer services for StatefulSet
- `configmap-stateful.yaml`: ConfigMap for StatefulSet
- `secret-stateful.yaml`: Secret for StatefulSet
- `serviceaccount-stateful.yaml`: ServiceAccount and RBAC for StatefulSet
- `hpa-stateful.yaml`: HPA for StatefulSet scaling

## Deployment Examples

### Example 1: Development Environment

```bash
helm install microservice-api kubernetes/helm/ \
  --set replicaCount=1 \
  --set serviceLoadBalancer.enabled=false \
  --set autoscaling.enabled=false
```

### Example 2: Production Environment with High Availability

```bash
helm install microservice-api kubernetes/helm/ \
  --set replicaCount=3 \
  --set autoscaling.enabled=true \
  --set autoscaling.maxReplicas=20 \
  --set serviceLoadBalancer.enabled=true \
  --set ingress.enabled=true
```

### Example 3: Staging with Custom Values

```bash
helm install microservice-api kubernetes/helm/ \
  -f helm-values-staging.yaml
```

### Example 4: Stateful Workload (Database, Cache, etc.)

```bash
helm install microservice-db kubernetes/helm/ \
  -f values-production.yaml \
  --set statefulSet.enabled=true \
  --set statefulSet.replicaCount=3 \
  --set statefulSet.storageSize=100Gi \
  --set statefulSet.storageClassName=fast-ssd
```

## Networking

### Internal Communication
- Use `microservice-api` service with port 80
- Internal DNS: `microservice-api.default.svc.cluster.local:80`

### StatefulSet Internal Communication
- Use headless service: `microservice-stateful.default.svc.cluster.local`
- Pod-specific DNS: `microservice-stateful-0.microservice-stateful.default.svc.cluster.local`
- Useful for ordered, direct pod communication

### External Access
- **LoadBalancer**: Exposed via cloud provider load balancer
- **Ingress**: HTTPS on api.example.com/api/v1
- **NodePort**: Available on any node port 30001

## Scaling

The deployment supports three scaling methods:

1. **Manual Scaling**
   ```bash
   kubectl scale deployment microservice-api --replicas=5
   kubectl scale statefulset microservice-stateful --replicas=5
   ```

2. **Horizontal Pod Autoscaler**
   ```bash
   kubectl get hpa microservice-api-hpa
   kubectl get hpa microservice-stateful-hpa
   kubectl describe hpa microservice-api-hpa
   ```

3. **Helm Value Adjustment**
   ```bash
   helm upgrade microservice-api kubernetes/helm/ \
     --set replicaCount=5
   helm upgrade microservice-db kubernetes/helm/ \
     --set statefulSet.replicaCount=5
   ```

## StatefulSet vs Deployment

### Use StatefulSet for:
- Databases (PostgreSQL, MySQL, MongoDB)
- Message brokers (RabbitMQ, Kafka)
- Distributed cache systems (Redis cluster)
- Any workload requiring stable pod identity and persistent storage

### Use Deployment for:
- Stateless APIs and microservices
- Web applications
- Load-balanced services
- Horizontally scalable workloads

## Security

- ServiceAccount with minimal RBAC permissions
- Secret management for credentials
- Security context: Non-root user (1000)
- Read-only root filesystem
- No privilege escalation
- AppArmor/SELinux ready
- PersistentVolume access controls for StatefulSet

## Monitoring

- Prometheus metrics on port 9090
- Liveness probe: /health/live
- Readiness probe: /health/ready
- Resource metrics for HPA

## Updating Images

```bash
# Update using kubectl
kubectl set image deployment/microservice-api \
  microservice-api=microservice-api:2.0.0

# Update using Helm
helm upgrade microservice-api kubernetes/helm/ \
  --set image.tag=2.0.0
```

## Troubleshooting

```bash
# Check pod logs
kubectl logs deployment/microservice-api

# Describe pod
kubectl describe pod <pod-name>

# Check service endpoints
kubectl get endpoints microservice-api

# Check ingress status
kubectl describe ingress microservice-ingress

# Check HPA status
kubectl describe hpa microservice-api-hpa
```

## Production Checklist

- [ ] Update image repository and tag
- [ ] Configure database host/credentials
- [ ] Configure Redis host/credentials
- [ ] Update ingress hostname
- [ ] Generate JWT secrets
- [ ] Configure TLS certificate
- [ ] Set resource limits appropriately
- [ ] Configure HPA thresholds
- [ ] Set up monitoring/alerts
- [ ] Configure log aggregation
- [ ] Test health check endpoints
- [ ] Validate RBAC permissions
- [ ] For StatefulSet: Configure storage class and size
- [ ] For StatefulSet: Verify persistent volume provisioning
- [ ] For StatefulSet: Test pod identity and DNS resolution
