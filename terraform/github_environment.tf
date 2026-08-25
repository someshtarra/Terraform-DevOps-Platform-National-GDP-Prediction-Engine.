resource "github_repository_environment" "environments" {
  for_each    = toset(["dev", "staging", "production"])
  environment = each.key
  repository  = github_repository.repo.name
}
