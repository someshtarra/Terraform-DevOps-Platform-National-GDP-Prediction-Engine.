# DevSecOps & Security Architecture

```mermaid
graph TD
    subgraph GitHub OIDC Authentication
        GHA[GitHub Actions Runner] -->|Request OIDC Token| STS[AWS STS]
        STS -->|Issue Temp Credentials| GHA
    end

    subgraph Pod IAM Roles IRSA
        POD[Kubernetes Pod] -->|ServiceAccount Annotations| OIDC[EKS OIDC Provider]
        OIDC -->|Assume IAM Role| AWS_SVC[AWS S3 / Secrets Manager]
    end
```

## Security Posture
- **Zero Static Credentials**: OIDC eliminates long-lived AWS IAM access keys in CI/CD.
- **IRSA**: Pods assume least-privilege IAM roles dynamically.
- **Scans**: Gitleaks (Secrets), Bandit (SAST), Trivy (Containers), TFSec (Terraform).
