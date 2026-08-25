resource "aws_db_subnet_group" "main" {
  name       = "gdp-db-subnet-group-${var.environment}"
  subnet_ids = aws_subnet.database[*].id

  tags = {
    Name = "gdp-db-subnet-group-${var.environment}"
  }
}

resource "aws_security_group" "db" {
  name        = "gdp-db-sg-${var.environment}"
  description = "Allow inbound PostgreSQL traffic from EKS cluster"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
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
    Name = "gdp-db-sg-${var.environment}"
  }
}

resource "aws_db_instance" "main" {
  identifier                = "gdp-postgres-${var.environment}"
  allocated_storage         = 20
  max_allocated_storage     = 100
  engine                    = "postgres"
  engine_version            = "15"
  instance_class            = var.db_instance_class
  db_name                   = var.db_name
  username                  = "gdp_user"
  password                  = "ChangeMeInProduction123!"
  db_subnet_group_name      = aws_db_subnet_group.main.name
  vpc_security_group_ids    = [aws_security_group.db.id]
  multi_az                  = var.environment == "production" ? true : false
  storage_encrypted         = true
  skip_final_snapshot       = var.environment == "production" ? false : true
  final_snapshot_identifier = "gdp-db-final-snapshot-${var.environment}"

  backup_retention_period = var.environment == "production" ? 14 : 3
  backup_window           = "03:00-04:00"
  maintenance_window      = "Sun:04:30-Sun:05:30"
}
