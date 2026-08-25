variable "environment" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "eks_security_group_id" {
  type = string
}

variable "instance_class" {
  type = string
}

variable "db_name" {
  type = string
}
