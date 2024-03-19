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
    - [Basics Commands](#basics-commands)
      - [Verify Terraform Installation And Version](#verify-terraform-installation-and-version)
      - [Terraform Init](#terraform-init)
      - [Validating a Configuration](#validating-a-configuration)
      - [Genenerating a Terraform Plan](#genenerating-a-terraform-plan)
      - [Applying a Terraform Plan](#applying-a-terraform-plan)
      - [Terraform Destroy](#terraform-destroy)

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

### Basics Commands

- There are a handful of basic terraform commands, including:

- `terraform init`
- `terraform validate`
- `terraform plan`
- `terraform apply`
- `terraform destroy`

#### Verify Terraform Installation And Version

- You can get the version of Terraform running on your machine with the following command:

```bash
terraform -version
```

- If you need to recall a specific subcommand, you can get a list of available commands and arguments with the help argument.

```bash
terraform -help
```

#### Terraform Init

- Initializing your workspace is used to initialize a working directory containing Terraform configuration files.

Once saved, you can return to your shell and run the init command shown below. This tells Terraform to scan your code and download anything it needs locally.

```bash
terraform init
```

Once your Terraform workspace has been initialized you are ready to begin planning and provisioning your resources.

#### Validating a Configuration

- The terraform validate command validates the configuration files in your working directory.
- To validate there are no syntax problems with our terraform configuration file run:

```bash
terraform validate
```

`output:`

```bash
Success! The configuration is valid.
```

#### Genenerating a Terraform Plan

- Terraform has a dry run mode where you can preview what Terraform will change without making any actual changes to your infrastructure.
- This dry run is performed by running a `terraform plan`.

```bash
terraform plan
```

#### Applying a Terraform Plan

- Run the command below to build the resources within your plan file.

```bash
terraform apply
```

#### Terraform Destroy

- The `terraform destroy` command is a convenient way to destroy all remote objects managed by a particular Terraform configuration.
- It does not delete your configuration file(s), `main.tf`, etc. It destroys the resources built from your Terraform code.
- Run the command as shown below to run a planned destroy:

```bash
terraform destroy
```
