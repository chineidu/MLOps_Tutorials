variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "vpc_name" {
  type    = string
  default = "demo_vpc"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "private_subnets" {
  default = {
    "private_subnet_1" = 1
    "private_subnet_2" = 2
    "private_subnet_3" = 3
  }
}

variable "public_subnets" {
  default = {
    "public_subnet_1" = 1
    "public_subnet_2" = 2
    "public_subnet_3" = 3
  }
}

variable "my_key_pair" {
  type        = string
  description = "Key-pair name"
  default     = "MyAWSKey"
}

variable "ingress_port_1" {
  type        = number
  description = "First ingress port (default allows HTTP traffic)"
  default     = 80
}

variable "ingress_port_2" {
  type        = number
  description = "Second ingress port (default allows HTTPS traffic)"
  default     = 443
}

variable "egress_port" {
  type        = number
  description = "Egress port (default allows HTTPS traffic)"
  default     = 0
}

variable "cidr_blocks" {
  type        = list(string)
  description = "Allowed ingress/egress CIDR blocks (default allows all outbound traffic)"
  default     = ["0.0.0.0/0"] # Allowing traffic from any IP address
}
