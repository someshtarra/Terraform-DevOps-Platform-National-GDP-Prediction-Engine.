resource "github_repository" "repo" {
  name        = var.repository_name
  description = "Production Infrastructure, CI/CD, and Kubernetes Platform for National GDP Prediction Engine"
  visibility  = "public"

  has_issues   = true
  has_projects = true
  has_wiki     = false

  vulnerability_alerts = true
}

resource "github_branch_protection" "main" {
  repository_id = github_repository.repo.node_id
  pattern       = "main"

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    required_approving_review_count = 1
  }

  required_status_checks {
    strict   = true
    contexts = ["Code Quality & Testing", "Security Scans (Secrets & Terraform & Helm)"]
  }

  enforce_admins = false
}

resource "github_repository_environment" "environments" {
  for_each    = toset(["dev", "staging", "production"])
  environment = each.key
  repository  = github_repository.repo.name
}
