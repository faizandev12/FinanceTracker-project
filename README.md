# 🚀 Finance Tracker - DevOps Implementation

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D.svg)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000.svg)](https://flask.palletsprojects.com/)
[![AWS](https://img.shields.io/badge/AWS-Fargate-FF9900.svg)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-1.x-623CE4.svg)](https://www.terraform.io/)

A cloud-native finance tracking application built with Vue.js/Flask and deployed using modern DevOps practices.

![Architecture Diagram](https://via.placeholder.com/800x500.png?text=Microservices+Architecture+Diagram)

## 🌟 Key Features

### Cloud Infrastructure
- 🐳 Dockerized microservices architecture
- ☁️ AWS Fargate serverless compute
- ⚖️ Application Load Balancer (ALB) with path-based routing
- 📦 Elastic Container Registry (ECR) for Docker images
- 🔐 VPC with security groups and NAT gateways
- 📈 Auto-scaling with AWS Fargate

### DevOps Implementation
- 🔄 CI/CD Pipeline with AWS CodePipeline/CodeBuild
- 🏗 Infrastructure as Code (IaC) using Terraform
- 🔒 IAM roles and security best practices
- 🌐 Multi-AZ deployment for high availability
- 💰 Cost-optimized architecture (~$200-$300/month)

### Application Features
- 👤 User authentication & authorization
- 💸 Income/expense tracking with categories
- 📊 Financial reports and analytics
- 🔄 RESTful API backend
- 📱 Responsive web interface

## 🛠 Tech Stack

**Frontend**  
Vue.js 3 | Axios | Tailwind CSS | Vite

**Backend**  
Python 3.10 | Flask | SQLAlchemy | JWT Auth

**Infrastructure**  
AWS Fargate | ECR | ALB | RDS PostgreSQL | Terraform | Docker

**DevOps**  
AWS CodePipeline | CloudWatch | VPC | IAM | GitHub Actions

## 📋 Architecture Overview

```plaintext
GitHub (Code) → AWS CodePipeline → Docker Build → ECR → Terraform → AWS Fargate
                     │
                     └── PostgreSQL RDS
                     └── Application Load Balancer
                     └── CloudWatch Monitoring
