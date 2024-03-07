# Terraform

- [Official docs](https://www.terraform.io/)
- [Terraform Udemy Course](https://www.udemy.com/course/terraform-hands-on-labs/?couponCode=ST12MT030524)

[![image.png](https://i.postimg.cc/MKPB14j9/image.png)](https://postimg.cc/2VW3D0GW)

## Table of Content

- [Terraform](#terraform)
  - [Table of Content](#table-of-content)
  - [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
    - [IaC Providers](#iac-providers)
    - [Benefits of Iac](#benefits-of-iac)
  - [Terraform (IaC)](#terraform-iac)

## Infrastructure as Code (IaC)

- This is used to automate the provisioning of infrastructure including servers, databases, firewall policies, and almost any other resource.
- IaC is commonly used in cloud computing environments, where resources can be easily provisioned and scaled on-demand. However, it can also be used to manage on-premises infrastructure.

### IaC Providers

- **Terraform**

- **AWS CloudFormation**: A service provided by Amazon Web Services that helps you model and set up your Amazon Web Services resources so that you can spend less time managing those resources and more time focusing on your applications. It uses a simple text file called a CloudFormation template to describe your infrastructure.

- **Azure Resource Manager**: A service provided by Microsoft Azure that helps you manage and visualize resources for applications, services, and infrastructure. It uses a simple JSON or YAML template to describe your infrastructure.

- **Google Cloud Deployment Manager**: An infrastructure deployment service provided by Google Cloud that allows you to define your infrastructure using YAML templates.

- **Pulumi**: A relatively new player in the IaC market that allows you to define your infrastructure using general-purpose programming languages like Python, JavaScript, TypeScript, and Go. This approach offers the benefits of a familiar programming environment, including error checking, autocompletion, and more.

- **HashiCorp Packer**: A tool that automates the creation of machine images, with support for various cloud providers like Amazon EC2, CloudStack, DigitalOcean, Docker, Google Compute Engine, Microsoft Azure, QEMU, VirtualBox, and VMware

### Benefits of Iac

- **Automation**: IaC automates the provisioning and configuration of infrastructure, saving time and reducing errors.
- **Repeatability**: You can easily recreate the same infrastructure environment again and again, ensuring consistency across deployments.
- **Version control**: IaC code can be version controlled, allowing you to track changes and rollback to previous configurations if necessary.
- **Collaboration**: IaC code can be shared and collaboratively edited by teams, improving communication and efficiency.

## [Terraform (IaC)](https://www.terraform.io/)

- Terraform is an open-source infrastructure as code (IaC) tool developed by HashiCorp.
- It allows you to define and manage infrastructure for both cloud and on-premise environments using human-readable configuration files.
- These files are written in HashiCorp Configuration Language (HCL) or optionally JSON.
