resource "github_repository" "repo" {
  name        = var.github_repository
  description = "Production Infrastructure, CI/CD, and Kubernetes Platform for National GDP Prediction Engine"
  visibility  = "public"

  has_issues   = true
  has_projects = true
  has_wiki     = false

  vulnerability_alerts = true
}
