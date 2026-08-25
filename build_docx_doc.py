import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def create_document():
    doc = Document()

    # Set Page Size to A4 (8.27 x 11.69 inches)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Add Helper Functions for Headings and Blocks
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(36)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
        return p

    def add_heading1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x22, 0x44, 0x88)
        return p

    def add_heading3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.font.name = 'Times New Roman'
            run_b.font.size = Pt(10)
            run_b.font.bold = True
        run_t = p.add_run(text)
        run_t.font.name = 'Times New Roman'
        run_t.font.size = Pt(10)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F4F6F9")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x11, 0x22, 0x44)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_callout(text, title="NOTE"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "EBF3FA")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        run_t = p.add_run(f"📌 {title}: ")
        run_t.font.name = 'Times New Roman'
        run_t.font.size = Pt(10)
        run_t.font.bold = True
        run_t.font.color.rgb = RGBColor(0x00, 0x44, 0x88)
        run_b = p.add_run(text)
        run_b.font.name = 'Times New Roman'
        run_b.font.size = Pt(10)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_table_data(headers, rows):
        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        # Format Header
        hdr_cells = tbl.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            set_cell_background(cell, "003366")
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(header_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Format Rows
        for r_idx, row_data in enumerate(rows):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_color = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, cell_value in enumerate(row_data):
                cell = row_cells[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(cell_value))
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # --------------------------------------------------------------------------
    # COVER PAGE
    # --------------------------------------------------------------------------
    add_title("Infrastructure as Code Based DevOps Platform Using Terraform, AWS, Kubernetes and CI/CD")
    add_subtitle("Complete Infrastructure, Automation, Deployment, Security, and Monitoring Technical Report")

    # Meta Table on Cover Page
    add_table_data(
        ["Project Metadata Field", "Specification Details"],
        [
            ["Project Title", "National GDP Prediction Engine Cloud Infrastructure Platform"],
            ["Author", "[Senior DevOps & Cloud Engineering Team]"],
            ["Organization", "[Enterprise Cloud & Platform Engineering]"],
            ["Version", "1.0.0 Production Release"],
            ["Target Environment", "AWS (Amazon Web Services) & Kubernetes (EKS v1.30)"],
            ["Infrastructure Manager", "Terraform (Single Source of Truth)"],
            ["CI/CD Engine", "GitHub Actions & OIDC Federated Authentication"],
            ["Microservice Application", "Python 3.11 FastAPI (Hybrid ARIMA + LSTM/GRU/CNN)"],
            ["Date", "2026-08-25"]
        ]
    )

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # TABLE OF CONTENTS
    # --------------------------------------------------------------------------
    add_heading1("Table of Contents")
    toc_items = [
        "Executive Summary",
        "Chapter 1 — Introduction to DevOps, Cloud & IaC",
        "Chapter 2 — Project Overview & Target Architecture",
        "Chapter 3 — Problem Statement & Solution Analysis",
        "Chapter 4 — Project Objectives & Governance Principles",
        "Chapter 5 — Existing System vs. Proposed Platform Comparison",
        "Chapter 6 — System Requirements (Hardware, Software, Cloud)",
        "Chapter 7 — Technology Stack Specifications",
        "Chapter 8 — Overall System Architecture",
        "Chapter 9 — AWS Cloud Infrastructure Architecture",
        "Chapter 10 — VPC Network & Subnet Topology",
        "Chapter 11 — Terraform Infrastructure as Code Engine",
        "Chapter 12 — Terraform Project Architecture & File Hierarchy",
        "Chapter 13 — Remote State Management & DynamoDB State Locking",
        "Chapter 14 — Docker Containerization & Multi-Stage Builds",
        "Chapter 15 — Amazon Elastic Container Registry (ECR)",
        "Chapter 16 — Kubernetes Workload Architecture",
        "Chapter 17 — Amazon Elastic Kubernetes Service (EKS v1.30)",
        "Chapter 18 — Application Deployment Architecture",
        "Chapter 19 — Continuous Integration (CI) Architecture",
        "Chapter 20 — Continuous Deployment (CD) & Environment Promotion",
        "Chapter 21 — GitHub Actions Workflow Engineering",
        "Chapter 22 — GitHub OIDC & AWS IAM Federated Authentication",
        "Chapter 23 — AWS Secrets Manager Integration",
        "Chapter 24 — Database & Caching Architecture (RDS PostgreSQL & ElastiCache Redis)",
        "Chapter 25 — DNS Routing & HTTPS Certificate Management (Route 53 & ACM)",
        "Chapter 26 — Observability, Monitoring & Log Management (CloudWatch & Prometheus)",
        "Chapter 27 — Autoscaling & Availability Architecture (HPA & PDB)",
        "Chapter 28 — DevSecOps Security Architecture & Scanners",
        "Chapter 29 — Multi-Environment Governance (Dev, Staging, Production)",
        "Chapter 30 — Disaster Recovery, RPO/RTO & Backup Strategies",
        "Chapter 31 — Automated Testing & Verification Suite",
        "Chapter 32 — Operational Troubleshooting Manual",
        "Chapter 33 — AWS Cost Optimization & Cleanup Procedures",
        "Chapter 34 — Complete Step-by-Step Installation & Setup Manual",
        "Chapter 35 — Production Deployment Walkthrough",
        "Chapter 36 — Application & Infrastructure Rollback Procedures",
        "Chapter 37 — Day-to-Day Operations Runbook",
        "Chapter 38 — Expected Project Results & Benefits",
        "Chapter 39 — Architectural Advantages & Trade-Offs",
        "Chapter 40 — System Limitations & Constraints",
        "Chapter 41 — Future Technical Enhancements",
        "Chapter 42 — Conclusion",
        "Chapter 43 — Academic & Industry References",
        "Appendix A — Terraform Command Reference",
        "Appendix B — AWS CLI Command Reference",
        "Appendix C — Kubernetes Kubectl Command Reference",
        "Appendix D — Docker Command Reference",
        "Appendix E — Git Command Reference",
        "Appendix F — Operational Troubleshooting Commands",
        "Appendix G — Complete Repository Tree Directory",
        "Appendix H — Environment Variables Specification"
    ]
    for idx, item in enumerate(toc_items, 1):
        add_bullet(f" {item}")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------------------------------
    add_heading1("Executive Summary")
    add_p(
        "Modern cloud software engineering demands automated, reliable, and secure deployment mechanisms to move application source code "
        "from local development environments to production cloud infrastructure. Traditional manual deployments suffer from configuration drift, "
        "human error, long-lived credential leakage risks, and lack of visibility. This technical document details the design, implementation, "
        "and operationalization of an enterprise-grade, cloud-native DevOps platform built on Amazon Web Services (AWS), Terraform, Amazon EKS (Kubernetes v1.30), "
        "Docker, Helm, GitHub Actions, and Prometheus/Grafana."
    )
    add_p(
        "The platform serves as the production infrastructure for the National GDP Prediction Engine—a Python 3.11 FastAPI microservice that models and "
        "forecasts national Gross Domestic Product (GDP) using a state-of-the-art hybrid approach combining statistical linear models (ARIMA) with deep learning "
        "sequence models (LSTM, GRU, and 1D CNN). The entire platform is governed by Infrastructure as Code (IaC) using HashiCorp Terraform as the single source of truth."
    )
    add_callout(
        "Terraform manages AWS Cloud Infrastructure, Kubernetes Workloads, and GitHub Repository Settings in unified declarative code, enabling a complete production deployment via 'make apply'.",
        "KEY ARCHITECTURAL HIGHLIGHT"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 1 — INTRODUCTION
    # --------------------------------------------------------------------------
    add_heading1("Chapter 1 — Introduction to DevOps, Cloud & IaC")
    add_p(
        "DevOps is a set of cultural philosophies, practices, and tools that increases an organization's ability to deliver applications and services at high velocity. "
        "By merging software development (Dev) and IT operations (Ops), organizations can automate infrastructure provisioning, testing, security, and continuous delivery."
    )
    add_bullet("Infrastructure as Code (IaC): Declaring cloud infrastructure using machine-readable configuration files (Terraform HCL).", "Core Concept 1: ")
    add_bullet("Containerization: Packaging application code and runtime dependencies into immutable containers (Docker).", "Core Concept 2: ")
    add_bullet("Container Orchestration: Managing container lifecycle, scaling, and networking at scale (Amazon EKS / Kubernetes).", "Core Concept 3: ")
    add_bullet("Continuous Integration / Continuous Delivery (CI/CD): Automating code validation, security scanning, container image publishing, and cluster deployment (GitHub Actions).", "Core Concept 4: ")

    # --------------------------------------------------------------------------
    # CHAPTER 2 — PROJECT OVERVIEW
    # --------------------------------------------------------------------------
    add_heading1("Chapter 2 — Project Overview & Target Architecture")
    add_p(
        "The National GDP Prediction Platform is designed to take a statistical and machine learning forecasting model from raw research scripts "
        "(`capstone project-3.ipynb` and historical dataset `GDP.csv`) to a production-hardened microservice running on AWS EKS."
    )
    add_code_block(
        "Developer -> Git Push -> GitHub -> GitHub Actions CI/CD -> Security Scan -> Docker Build -> ECR -> EKS Deployment -> ALB -> Users"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 3 — PROBLEM STATEMENT
    # --------------------------------------------------------------------------
    add_heading1("Chapter 3 — Problem Statement & Solution Analysis")
    add_p(
        "Traditional infrastructure management relying on manual cloud console clicks creates significant operational vulnerabilities: "
        "untracked configuration drift, hardcoded IAM keys in script files, unvalidated deployment pushes, and single points of failure. "
        "The proposed platform resolves these challenges by establishing Terraform as the single source of truth across cloud infrastructure, "
        "Kubernetes workloads, and GitHub repository controls."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 4 — OBJECTIVES
    # --------------------------------------------------------------------------
    add_heading1("Chapter 4 — Project Objectives & Governance Principles")
    add_bullet("Achieve 100% Infrastructure as Code automation for all AWS, Kubernetes, and GitHub resources.", "Objective 1: ")
    add_bullet("Eliminate static AWS IAM access keys in CI/CD using GitHub OIDC federated authentication.", "Objective 2: ")
    add_bullet("Enforce zero-downtime rolling updates with Horizontal Pod Autoscaling (HPA) and Pod Disruption Budgets (PDB).", "Objective 3: ")
    add_bullet("Integrate comprehensive security scanning across code (Bandit), dependencies (Pip-Audit), secrets (Gitleaks), container images (Trivy), and IaC (TFSec).", "Objective 4: ")

    # --------------------------------------------------------------------------
    # CHAPTER 5 — EXISTING VS PROPOSED SYSTEM
    # --------------------------------------------------------------------------
    add_heading1("Chapter 5 — Existing System vs. Proposed Platform Comparison")
    add_table_data(
        ["System Feature / Capability", "Traditional / Existing Approach", "Proposed Terraform DevOps Platform"],
        [
            ["Infrastructure Provisioning", "Manual AWS Management Console clicks", "Automated Terraform IaC (`make apply`)"],
            ["Deployment Process", "Manual SSH & script execution", "Automated GitHub Actions CI/CD Pipeline"],
            ["Container Registry", "Unmanaged or local storage", "AWS ECR with tag immutability & scan-on-push"],
            ["Orchestration & Scaling", "Single VM / Docker Compose", "AWS EKS Cluster with HPA (2 to 15 pods)"],
            ["Security & Secret Management", "Hardcoded credentials in code/.env", "AWS Secrets Manager & IRSA dynamic injection"],
            ["Authentication in CI/CD", "Static IAM Access Keys in GitHub", "Zero-key AWS OIDC federated token exchange"],
            ["Observability & Logging", "Local text log files", "CloudWatch JSON logs & Prometheus/Grafana dashboards"],
            ["Rollback Strategy", "Manual container rebuild", "Automated Helm rollback (`helm rollback 0`)"]
        ]
    )

    # --------------------------------------------------------------------------
    # CHAPTER 6 — REQUIREMENTS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 6 — System Requirements (Hardware, Software, Cloud)")
    add_p("The platform requires standard development machine tools and an active AWS Subscription:")
    add_bullet("Operating System: Linux, macOS, or Windows Subsystem for Linux (WSL2).", "Dev Workstation: ")
    add_bullet("Software Dependencies: Git 2.39+, Docker 24.0+, Python 3.11+, Terraform 1.7+, AWS CLI 2.15+, Kubectl 1.30+, Helm 3.14+.", "CLI Toolchain: ")
    add_bullet("AWS Account: Active IAM user permissions for VPC, EKS, ECR, RDS, ElastiCache, Secrets Manager, Route 53, and ACM.", "Cloud Account: ")

    # --------------------------------------------------------------------------
    # CHAPTER 7 — TECHNOLOGY STACK
    # --------------------------------------------------------------------------
    add_heading1("Chapter 7 — Technology Stack Specifications")
    add_table_data(
        ["Technology Component", "Version / Spec", "Operational Purpose"],
        [
            ["Terraform", "v1.7.5+", "Infrastructure as Code engine governing AWS, K8s, and GitHub"],
            ["Amazon EKS", "v1.30", "Managed Kubernetes container orchestration control plane"],
            ["FastAPI", "v0.111.0", "Asynchronous Python web framework serving prediction REST APIs"],
            ["Python / NumPy / Statsmodels", "v3.11 / v1.26 / v0.14", "Data processing & ARIMA + LSTM/GRU/CNN Hybrid ML engine"],
            ["Amazon ECR", "KMS Encrypted", "Private container registry storing immutable Docker images"],
            ["Amazon RDS", "PostgreSQL v15", "Multi-AZ relational database for prediction audit records"],
            ["Amazon ElastiCache", "Redis v7", "In-memory replication group caching forecast query results"],
            ["GitHub Actions", "OIDC Integration", "Automated multi-environment CI/CD deployment runner"],
            ["Prometheus & Grafana", "v2.52 / v11.0", "System metrics collection, alerting, and visualization dashboard"]
        ]
    )

    # --------------------------------------------------------------------------
    # CHAPTER 8 — OVERALL SYSTEM ARCHITECTURE
    # --------------------------------------------------------------------------
    add_heading1("Chapter 8 — Overall System Architecture")
    add_p(
        "The overall platform architecture integrates developer workflows, continuous integration pipelines, AWS managed services, "
        "and Kubernetes cluster orchestration into a cohesive unit."
    )
    add_code_block(
        "Client Request -> Route 53 DNS -> AWS ALB -> EKS Ingress -> ClusterIP Service -> FastAPI Pod -> Redis / RDS / S3"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 9 — AWS CLOUD INFRASTRUCTURE
    # --------------------------------------------------------------------------
    add_heading1("Chapter 9 — AWS Cloud Infrastructure Architecture")
    add_p(
        "AWS managed services provide enterprise reliability, high availability, and operational efficiency. "
        "By leveraging AWS EKS for Kubernetes master nodes, RDS Multi-AZ for PostgreSQL, and ElastiCache for Redis, "
        "the infrastructure minimizes operational management overhead."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 10 — VPC NETWORKING
    # --------------------------------------------------------------------------
    add_heading1("Chapter 10 — VPC Network & Subnet Topology")
    add_p(
        "The Amazon VPC network (`10.30.0.0/16`) spans 3 Availability Zones (us-east-1a, us-east-1b, us-east-1c) "
        "and implements strict 3-tier subnet separation:"
    )
    add_bullet("Public Subnets (10.30.0.0/20, 10.30.16.0/20, 10.30.32.0/20): Host AWS Application Load Balancers and NAT Gateways.", "Tier 1 — Public: ")
    add_bullet("Private Subnets (10.30.48.0/20, 10.30.64.0/20, 10.30.80.0/20): Host EKS Worker Node instances. Internet egress routes via NAT Gateways.", "Tier 2 — Private: ")
    add_bullet("Database Subnets (10.30.96.0/20, 10.30.112.0/20, 10.30.128.0/20): Isolated database subnets without internet access. Restrict access to EKS nodes.", "Tier 3 — Isolated DB: ")

    # --------------------------------------------------------------------------
    # CHAPTER 11 — TERRAFORM ENGINE
    # --------------------------------------------------------------------------
    add_heading1("Chapter 11 — Terraform Infrastructure as Code Engine")
    add_p(
        "HashiCorp Terraform executes declarative configuration files to provision, update, and manage cloud resources idempotently. "
        "Terraform reads `.tf` code, calculates execution diffs (`terraform plan`), and executes targeted AWS API calls (`terraform apply`)."
    )
    add_code_block(
        "# Example Terraform Provider Configuration\n"
        "provider \"aws\" {\n"
        "  region = var.aws_region\n"
        "  default_tags {\n"
        "    tags = { Environment = var.environment, ManagedBy = \"Terraform\" }\n"
        "  }\n"
        "}"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 12 — TERRAFORM PROJECT STRUCTURE
    # --------------------------------------------------------------------------
    add_heading1("Chapter 12 — Terraform Project Architecture & File Hierarchy")
    add_p(
        "The project provides a clean, flat, file-by-file `terraform/` directory matching enterprise standards:"
    )
    add_bullet("provider.tf, variables.tf, outputs.tf, locals.tf: Top-level provider and configuration definitions.", "Core Files: ")
    add_bullet("network.tf, eks.tf, ecr.tf, rds.tf, redis.tf, iam.tf, secrets.tf, dns.tf, acm.tf, monitoring.tf: AWS Cloud infrastructure files.", "AWS Infrastructure: ")
    add_bullet("github.tf, github_repository.tf, github_environment.tf, github_branch_protection.tf, github_actions.tf: GitHub governance files.", "GitHub Governance: ")
    add_bullet("kubernetes_namespace.tf, deployment.tf, service.tf, ingress.tf, hpa.tf, pdb.tf, configmap.tf, networkpolicy.tf: Kubernetes workload files.", "Kubernetes Workloads: ")

    # --------------------------------------------------------------------------
    # CHAPTER 13 — TERRAFORM STATE & LOCKING
    # --------------------------------------------------------------------------
    add_heading1("Chapter 13 — Remote State Management & DynamoDB State Locking")
    add_p(
        "Terraform tracks provisioned infrastructure in a state file (`terraform.tfstate`). To prevent state corruption during concurrent team applies, "
        "remote state is configured using AWS S3 with server-side KMS encryption and DynamoDB table locking (`gdp-prediction-tf-locks`)."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 14 — DOCKER CONTAINERIZATION
    # --------------------------------------------------------------------------
    add_heading1("Chapter 14 — Docker Containerization & Multi-Stage Builds")
    add_p(
        "The application is packaged into a multi-stage Docker image (`Dockerfile`). The builder stage compiles Python wheels, "
        "while the final runtime stage copies compiled binaries into a clean `python:3.11-slim` image, creating a small, secure 220MB container."
    )
    add_code_block(
        "FROM python:3.11-slim as runtime\n"
        "WORKDIR /app\n"
        "RUN addgroup --gid 10001 appgroup && adduser --uid 10001 --ingroup appgroup --disabled-password appuser\n"
        "COPY src /app/src\n"
        "USER 10001:10001\n"
        "CMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 15 — AMAZON ECR
    # --------------------------------------------------------------------------
    add_heading1("Chapter 15 — Amazon Elastic Container Registry (ECR)")
    add_p(
        "AWS ECR serves as the secure private container registry. Immutability is enabled on image tags (using `<git-sha>` tags), "
        "preventing overwritten images. Automated scanning on push checks images for vulnerability CVEs, and lifecycle policies clean up older builds."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 16 — KUBERNETES WORKLOADS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 16 — Kubernetes Workload Architecture")
    add_p(
        "Kubernetes workloads (`kubernetes/`) manage application pods, networking, and scaling declarative objects:"
    )
    add_bullet("Namespace (`gdp-production`): Provides complete virtual isolation for production workloads.", "Namespace: ")
    add_bullet("Deployment: Manages rolling pod updates (`maxSurge: 25%`, `maxUnavailable: 25%`).", "Deployment: ")
    add_bullet("Service (`ClusterIP`): Exposes internal pod IP addresses on port 8000.", "Service: ")
    add_bullet("Ingress (`ALB`): Integrates with AWS Load Balancer Controller to manage external HTTPS traffic.", "Ingress: ")

    # --------------------------------------------------------------------------
    # CHAPTER 17 — AMAZON EKS V1.30
    # --------------------------------------------------------------------------
    add_heading1("Chapter 17 — Amazon Elastic Kubernetes Service (EKS v1.30)")
    add_p(
        "AWS EKS v1.30 provides a highly available, managed Kubernetes control plane. Worker nodes run inside auto-scaling EC2 node groups "
        "distributed across 3 Availability Zones, utilizing AWS VPC CNI for native pod IP allocation."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 18 — APPLICATION DEPLOYMENT
    # --------------------------------------------------------------------------
    add_heading1("Chapter 18 — Application Deployment Architecture")
    add_p(
        "Application pods execute the FastAPI microservice, loading historical GDP dataset observations (`GDP.csv`) and running the "
        "ARIMA-LSTM/GRU/CNN Hybrid ML prediction engine to calculate future quarterly economic projections."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 19 — CONTINUOUS INTEGRATION (CI)
    # --------------------------------------------------------------------------
    add_heading1("Chapter 19 — Continuous Integration (CI) Architecture")
    add_p(
        "The CI pipeline (`.github/workflows/ci.yml`) runs quality checks on every pull request and push: "
        "Code Formatting (Black), Linting (Flake8), Unit Testing (Pytest), SAST (Bandit), Secret Scanning (Gitleaks), Helm Linting, and Container Scanning (Trivy)."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 20 — CONTINUOUS DEPLOYMENT (CD)
    # --------------------------------------------------------------------------
    add_heading1("Chapter 20 — Continuous Deployment (CD) & Environment Promotion")
    add_p(
        "The CD pipeline promotes container builds through DEV -> STAGING -> PRODUCTION environments. "
        "Production deployments require explicit manual reviewer approval in GitHub Environment settings before applying Helm upgrades to EKS."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 21 — GITHUB ACTIONS WORKFLOWS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 21 — GitHub Actions Workflow Engineering")
    add_p(
        "The master pipeline (`.github/workflows/pipeline.yml`) orchestrates all CI and CD jobs in a single, visual workflow file, "
        "enforcing strict dependency gates (`needs: [ci]`, `needs: [deploy-dev]`, `needs: [deploy-staging]`)."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 22 — GITHUB OIDC & AWS IAM
    # --------------------------------------------------------------------------
    add_heading1("Chapter 22 — GitHub OIDC & AWS IAM Federated Authentication")
    add_p(
        "By configuring an OpenID Connect (OIDC) identity provider in AWS IAM (`github/oidc.tf`), GitHub Actions runners authenticate using temporary "
        "JSON Web Tokens (JWT) exchanged for short-lived IAM credentials, completely eliminating static AWS access keys."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 23 — SECRETS MANAGEMENT
    # --------------------------------------------------------------------------
    add_heading1("Chapter 23 — AWS Secrets Manager Integration")
    add_p(
        "AWS Secrets Manager encrypts database passwords and token credentials at rest using AWS KMS. Application pods consume secrets "
        "dynamically via IAM Roles for Service Accounts (IRSA)."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 24 — DATABASE & CACHING
    # --------------------------------------------------------------------------
    add_heading1("Chapter 24 — Database & Caching Architecture (RDS PostgreSQL & ElastiCache Redis)")
    add_p(
        "The data layer utilizes AWS RDS PostgreSQL Multi-AZ for persistent audit log storage and AWS ElastiCache Redis for caching "
        "computed hybrid model forecast outputs with 1-hour TTLs, reducing backend latency."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 25 — DNS & HTTPS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 25 — DNS Routing & HTTPS Certificate Management (Route 53 & ACM)")
    add_p(
        "Amazon Route 53 manages public DNS resolution (`gdp.api.domain.com`), while AWS Certificate Manager (ACM) provisions SSL/TLS certificates "
        "with automated DNS validation, terminating TLS securely at the Application Load Balancer."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 26 — OBSERVABILITY & LOGGING
    # --------------------------------------------------------------------------
    add_heading1("Chapter 26 — Observability, Monitoring & Log Management (CloudWatch & Prometheus)")
    add_p(
        "The platform implements full-stack observability: Prometheus scrapes HTTP request counters and latency histograms from `/metrics`, "
        "Grafana visualizes dashboard charts (`monitoring/grafana-dashboard.json`), and CloudWatch collects structured JSON logs."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 27 — AUTOSCALING & AVAILABILITY
    # --------------------------------------------------------------------------
    add_heading1("Chapter 27 — Autoscaling & Availability Architecture (HPA & PDB)")
    add_p(
        "Horizontal Pod Autoscaler (HPA) automatically adjusts pod replica count from 2 to 15 pods based on CPU (75%) and Memory (80%) targets, "
        "while Pod Disruption Budget (PDB) guarantees `minAvailable: 2` pods during cluster maintenance."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 28 — DEVSECOPS SECURITY
    # --------------------------------------------------------------------------
    add_heading1("Chapter 28 — DevSecOps Security Architecture & Scanners")
    add_p(
        "DevSecOps controls are embedded into every layer: non-root UID `10001` container contexts, read-only root filesystems, dropped Linux capabilities, "
        "strict NetworkPolicy egress rules, and automated vulnerability scanners (Gitleaks, Bandit, Trivy, TFSec)."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 29 — MULTI-ENVIRONMENT GOVERNANCE
    # --------------------------------------------------------------------------
    add_heading1("Chapter 29 — Multi-Environment Governance (Dev, Staging, Production)")
    add_table_data(
        ["Governance Dimension", "Development (DEV)", "Staging (STAGING)", "Production (PRODUCTION)"],
        [
            ["Kubernetes Replicas", "2 Pods", "2 Pods", "4 to 15 Pods (HPA Auto-scaling)"],
            ["RDS Sizing", "db.t4g.micro (Single-AZ)", "db.t4g.small (Single-AZ)", "db.m6g.large (Multi-AZ High Availability)"],
            ["Redis Sizing", "cache.t4g.micro", "cache.t4g.micro", "cache.m6g.large"],
            ["Approval Requirements", "Automated deployment on push", "Automated deploy on release tag", "Manual Reviewer Approval Gate required"]
        ]
    )

    # --------------------------------------------------------------------------
    # CHAPTER 30 — DISASTER RECOVERY
    # --------------------------------------------------------------------------
    add_heading1("Chapter 30 — Disaster Recovery, RPO/RTO & Backup Strategies")
    add_p(
        "Disaster recovery controls guarantee an RPO < 15 minutes and RTO < 1 hour through automated RDS point-in-time recovery, "
        "S3 object versioning, and the automated `scripts/disaster_recovery.sh` backup and restore script."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 31 — TESTING & VERIFICATION
    # --------------------------------------------------------------------------
    add_heading1("Chapter 31 — Automated Testing & Verification Suite")
    add_p(
        "Testing includes Pytest unit/integration test suites (`tests/`), post-deployment smoke tests (`scripts/smoke_test.sh`), "
        "and deep health validation (`scripts/health_check.py`)."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 32 — TROUBLESHOOTING MANUAL
    # --------------------------------------------------------------------------
    add_heading1("Chapter 32 — Operational Troubleshooting Manual")
    add_p("Comprehensive troubleshooting procedures for common cloud and Kubernetes incidents:")
    add_bullet("Run 'kubectl logs -n gdp-production -l app=gdp-prediction-app' and check database connection strings.", "CrashLoopBackOff: ")
    add_bullet("Verify ECR image tag exists and verify EKS Worker Node IAM permissions.", "ImagePullBackOff: ")
    add_bullet("Run 'terraform force-unlock <LOCK_ID>' to release stale DynamoDB locks.", "Terraform State Lock: ")

    # --------------------------------------------------------------------------
    # CHAPTER 33 — COST OPTIMIZATION
    # --------------------------------------------------------------------------
    add_heading1("Chapter 33 — AWS Cost Optimization & Cleanup Procedures")
    add_p(
        "Cost optimization strategies include spot instances for non-prod node groups, Graviton t4g instance types, "
        "and ECR lifecycle policies expiring tagged images past 30 builds. Run `make destroy` to teardown dev infrastructure."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 34 — SETUP MANUAL
    # --------------------------------------------------------------------------
    add_heading1("Chapter 34 — Complete Step-by-Step Installation & Setup Manual")
    add_code_block(
        "# 1. Clone Repository\n"
        "git clone https://github.com/someshtarra/TERRAFORM.git && cd TERRAFORM\n\n"
        "# 2. Configure AWS CLI\n"
        "aws configure\n\n"
        "# 3. Run Bootstrap (Creates S3 State Bucket & DynamoDB Lock Table)\n"
        "make bootstrap\n\n"
        "# 4. Initialize & Apply Terraform Infrastructure\n"
        "cp terraform.tfvars.example terraform.tfvars\n"
        "make init && make plan && make apply"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 35 — DEPLOYMENT WALKTHROUGH
    # --------------------------------------------------------------------------
    add_heading1("Chapter 35 — Production Deployment Walkthrough")
    add_p(
        "After `make apply` completes, update your local kubeconfig and verify EKS cluster nodes:"
    )
    add_code_block(
        "aws eks update-kubeconfig --region us-east-1 --name gdp-eks-production\n"
        "kubectl get nodes\n"
        "kubectl get pods -n gdp-production"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 36 — ROLLBACK PROCEDURES
    # --------------------------------------------------------------------------
    add_heading1("Chapter 36 — Application & Infrastructure Rollback Procedures")
    add_p(
        "If a production application deployment fails, execute instant Helm rollback to revert to the previous revision:"
    )
    add_code_block(
        "helm rollback gdp-app-prod 0 --namespace gdp-production"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 37 — OPERATIONS RUNBOOK
    # --------------------------------------------------------------------------
    add_heading1("Chapter 37 — Day-to-Day Operations Runbook")
    add_bullet("Monitor Pod Status: kubectl get pods -n gdp-production", "Daily Check 1: ")
    add_bullet("Check HPA Autoscaling: kubectl get hpa -n gdp-production", "Daily Check 2: ")
    add_bullet("Verify Grafana Dashboards: http://localhost:3000", "Daily Check 3: ")

    # --------------------------------------------------------------------------
    # CHAPTER 38 — EXPECTED RESULTS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 38 — Expected Project Results & Benefits")
    add_bullet("100% automated infrastructure provisioning via Terraform IaC.", "Result 1: ")
    add_bullet("Zero static AWS keys stored in GitHub Actions due to OIDC federated auth.", "Result 2: ")
    add_bullet("Zero-downtime rolling updates backed by HPA and PDB availability guarantees.", "Result 3: ")

    # --------------------------------------------------------------------------
    # CHAPTER 39 — ADVANTAGES
    # --------------------------------------------------------------------------
    add_heading1("Chapter 39 — Architectural Advantages & Trade-Offs")
    add_p(
        "The unified Terraform approach guarantees complete consistency across cloud infrastructure, container registries, "
        "Kubernetes workloads, and GitHub repository controls."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 40 — LIMITATIONS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 40 — System Limitations & Constraints")
    add_bullet("AWS Cloud Dependency: Modules are tailored for AWS managed services.", "Limitation 1: ")
    add_bullet("Initial Bootstrap Step: Requires executing 'make bootstrap' prior to main terraform apply.", "Limitation 2: ")

    # --------------------------------------------------------------------------
    # CHAPTER 41 — FUTURE ENHANCEMENTS
    # --------------------------------------------------------------------------
    add_heading1("Chapter 41 — Future Technical Enhancements")
    add_bullet("Integration of Istio Service Mesh for mutual TLS (mTLS) pod encryption.", "Future Enhancement 1: ")
    add_bullet("Implementation of KEDA (Kubernetes Event-driven Autoscaling) for custom Prometheus metrics.", "Future Enhancement 2: ")

    # --------------------------------------------------------------------------
    # CHAPTER 42 — CONCLUSION
    # --------------------------------------------------------------------------
    add_heading1("Chapter 42 — Conclusion")
    add_p(
        "The Infrastructure as Code based DevOps Platform demonstrates an enterprise-grade cloud architecture for deploying machine learning microservices. "
        "By utilizing Terraform as the single source of truth across AWS, Kubernetes, and GitHub, the platform delivers automated, secure, scalable, and reproducible deployments."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 43 — REFERENCES
    # --------------------------------------------------------------------------
    add_heading1("Chapter 43 — Academic & Industry References")
    add_bullet("HashiCorp Terraform AWS & GitHub Provider Documentation (2026). https://registry.terraform.io/", "Reference 1: ")
    add_bullet("Amazon Web Services. AWS EKS User Guide & Security Best Practices (2026). https://docs.aws.amazon.com/eks/", "Reference 2: ")
    add_bullet("Kubernetes Documentation. Workloads, HPA, PDB & NetworkPolicies (2026). https://kubernetes.io/docs/", "Reference 3: ")

    # --------------------------------------------------------------------------
    # APPENDICES A - H
    # --------------------------------------------------------------------------
    add_heading1("Appendix A — Terraform Command Reference")
    add_code_block("make bootstrap\nmake init\nmake validate\nmake plan\nmake apply\nmake destroy")

    add_heading1("Appendix B — AWS CLI Command Reference")
    add_code_block("aws configure\naws sts get-caller-identity\naws eks update-kubeconfig --region us-east-1 --name gdp-eks-production")

    add_heading1("Appendix C — Kubernetes Kubectl Command Reference")
    add_code_block("kubectl get nodes\nkubectl get pods -A\nkubectl get svc -n gdp-production\nkubectl get ingress -n gdp-production")

    add_heading1("Appendix D — Docker Command Reference")
    add_code_block("make docker-up\nmake docker-down\ndocker build -t gdp-prediction-app:latest .")

    add_heading1("Appendix E — Git Command Reference")
    add_code_block("git status\ngit add .\ngit commit -m \"feat: updates\"\ngit push origin main")

    add_heading1("Appendix F — Operational Troubleshooting Commands")
    add_code_block("kubectl logs -n gdp-production -l app=gdp-prediction-app --tail=100\nterraform force-unlock <LOCK_ID>")

    add_heading1("Appendix G — Complete Repository Tree Directory")
    add_code_block("TERRAFORM/\n├── bootstrap/\n├── aws/\n├── kubernetes/\n├── github/\n├── ci-cd/\n├── src/\n├── tests/\n├── helm/\n├── docs/\n└── README.md")

    add_heading1("Appendix H — Environment Variables Specification")
    add_code_block("APP_ENV=production\nPOSTGRES_HOST=gdp-postgres.internal\nPOSTGRES_PORT=5432\nPOSTGRES_DB=gdp_db_prod\nREDIS_HOST=gdp-redis.internal\nREDIS_PORT=6379")

    # Save Word Document
    output_filename = "Terraform_DevOps_Project_Documentation.docx"
    doc.save(output_filename)
    print(f"Successfully generated Word Document: {output_filename}")

if __name__ == "__main__":
    create_document()
