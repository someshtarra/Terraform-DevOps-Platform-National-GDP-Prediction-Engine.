resource "github_actions_environment_secret" "aws_role_arn" {
  for_each        = toset(["dev", "staging", "production"])
  repository      = github_repository.repo.name
  environment     = each.key
  secret_name     = "AWS_ROLE_TO_ASSUME"
  plaintext_value = aws_iam_role.github_actions.arn
}

resource "github_actions_environment_secret" "aws_region" {
  for_each        = toset(["dev", "staging", "production"])
  repository      = github_repository.repo.name
  environment     = each.key
  secret_name     = "AWS_REGION"
  plaintext_value = "us-east-1"
}
