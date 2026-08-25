# AWS IAM OpenID Connect Provider for GitHub Actions
resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1", "1c58a218597df77013e8c1024f00257348d281a9"]

  tags = {
    Name      = "github-actions-oidc"
    ManagedBy = "Terraform"
  }
}

# AWS IAM Role for GitHub Actions OIDC Federated Access
resource "aws_iam_role" "github_actions" {
  name = "gdp-github-actions-oidc-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Federated = aws_iam_openid_connect_provider.github_actions.arn
      }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:${var.github_owner}/${var.github_repository}:*"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "github_actions_ecr" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
  role       = aws_iam_role.github_actions.name
}

resource "aws_iam_role_policy_attachment" "github_actions_eks" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.github_actions.name
}
