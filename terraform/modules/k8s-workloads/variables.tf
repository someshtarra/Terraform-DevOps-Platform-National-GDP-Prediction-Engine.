variable "environment" {
  type = string
}

variable "ecr_repository_url" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "acm_certificate_arn" {
  type    = string
  default = ""
}
