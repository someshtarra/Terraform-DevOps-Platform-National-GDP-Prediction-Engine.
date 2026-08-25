resource "github_branch_protection" "main" {
  repository_id = github_repository.repo.node_id
  pattern       = "main"

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    required_approving_review_count = 1
  }

  required_status_checks {
    strict   = true
    contexts = ["1. CI (Lint, Test, Security & Docker Scan)"]
  }

  enforce_admins = false
}
