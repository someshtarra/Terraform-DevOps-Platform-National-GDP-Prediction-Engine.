resource "github_actions_environment_secret" "aws_access_key" {
  for_each        = toset(["dev", "staging", "production"])
  repository      = github_repository.repo.name
  environment     = each.key
  secret_name     = "AWS_ACCESS_KEY_ID"
  plaintext_value = "EXAMPLE_ACCESS_KEY_ID"
}

resource "github_actions_environment_secret" "aws_secret_key" {
  for_each        = toset(["dev", "staging", "production"])
  repository      = github_repository.repo.name
  environment     = each.key
  secret_name     = "AWS_SECRET_ACCESS_KEY"
  plaintext_value = "EXAMPLE_SECRET_ACCESS_KEY"
}
