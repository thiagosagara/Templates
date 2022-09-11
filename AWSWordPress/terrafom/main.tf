terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "=> 4.16" 
      }
    }
}

provider "aws" {
    region = "us-east-1"
  
}

# VPC:
#   CIDR: 192.168.0.0/20
#   subnetA_privada: 192.168.0.0/24 (1a)
#   subnetB_privada: 192.168.2.0/24 (1b)
#   NatGateway
resource "aws_vpc" "blog-sagaratec-vpc" {
 
}



# EC2: 
#   instalação no userdata:
#       apt update -y
#       apt install ansible unzip -y
#       curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#       unzip awscliv2.zip
#       sudo ./aws/install
#       wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
#       echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
#       sudo apt update && sudo apt install terraform
#
#   Security-Group:
#       name: blog-sagaratec-web
#       porta: HTTP
resource "aws_instance" "blog-sagaratec-app" {
  ami = "ami-052efd3df9dad4825"
  instance_type = "t3.micro"

  tag = {
    Name = "srv-blog-sagaratec-template"
  }

}


# RDS:
#   engine: mysql 5.7
#   user:   wpuser
#   name:   wordpress
#   pass:   Wp@12345
#   type: t2.micro
#   storage: 20Gb
#   AZ: 1a e 1b
#   Security-Group:
#       name: blog-sagaratec-db
#       porta: 3306
#       Allow: blog-sagaratec-web
#
#   Setar multiAZ
resource "aws_rds_cluster_instance" "blog-sagaratec-db" {
  
}



# ElastiCache:
#   Security-Group
#       name: blog-sagaratec-sessoes
#       allow: blog-sagaratec-web 
#       porta: 11211
#   Subnet:
#       name: cache-sessoes-blog-sagaratec
#    Cluster MemCached:
#       name: blog-sagaratec-sessoes
#       type: cache.t4g.micro
#       versao: 1.6.6
#       nós: 2
#       AZ: 1a e 1b
#       
resource "aws_elasticache_cluster" "blog-sagaratec-sessoes" {
  
}



# Load Balancer:
#   ALB
#   forward 80 to 443
#   health_check: info.php
resource "aws_alb" "blog-sagaratec-lb" {
  
}























