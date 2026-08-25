# Kubernetes Cluster & Workload Architecture

```mermaid
graph TD
    subgraph EKS Cluster v1.30
        subgraph Namespace: gdp-production
            ING[Ingress - ALB Controller]
            SVC[Service - ClusterIP]
            HPA[Horizontal Pod Autoscaler]
            PDB[Pod Disruption Budget]

            subgraph Deployment: gdp-prediction-app
                POD1[Pod 1]
                POD2[Pod 2]
                POD3[Pod 3]
            end
        end
    end

    ING --> SVC
    SVC --> POD1 & POD2 & POD3
    HPA -->|Scale 2-15 Pods| Deployment
```

## Key Workload Policies
- **HPA**: Auto-scales based on 75% CPU and 80% Memory targets.
- **PDB**: Maintains `minAvailable: 2` replicas during node rotation.
- **SecurityContext**: Non-root UID `10001`, read-only root filesystem, capabilities dropped.
