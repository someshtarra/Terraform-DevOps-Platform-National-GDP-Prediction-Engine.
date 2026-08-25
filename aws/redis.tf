resource "aws_elasticache_subnet_group" "main" {
  name       = "gdp-redis-subnet-group-${var.environment}"
  subnet_ids = aws_subnet.database[*].id
}

resource "aws_security_group" "redis" {
  name        = "gdp-redis-sg-${var.environment}"
  description = "Allow inbound Redis traffic from EKS cluster"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_eks_cluster.main.vpc_config[0].cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "gdp-redis-sg-${var.environment}"
  }
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id = "gdp-redis-${var.environment}"
  description          = "Redis replication group for GDP prediction cache"
  node_type            = var.redis_node_type
  num_cache_clusters   = var.environment == "production" ? 2 : 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  automatic_failover_enabled = var.environment == "production" ? true : false
}
