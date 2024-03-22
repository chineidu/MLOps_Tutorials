# Terraform

- [Official docs](https://www.terraform.io/)
- [Terraform Udemy Course](https://www.udemy.com/course/terraform-hands-on-labs/?couponCode=ST12MT030524)

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
      - [Format HCL Files](#format-hcl-files)
      - [Validating a Configuration](#validating-a-configuration)
      - [Genenerating a Terraform Plan](#genenerating-a-terraform-plan)
      - [Applying a Terraform Plan](#applying-a-terraform-plan)
      - [Terraform Destroy](#terraform-destroy)
    - [Hashicorp Configuration Language (HCL)](#hashicorp-configuration-language-hcl)
    - [Terraform Resource Block](#terraform-resource-block)
    - [Terraform Input Variable Block](#terraform-input-variable-block)
    - [Terraform Data Block](#terraform-data-block)
    - [Terraform Provider Block](#terraform-provider-block)
    - [Example Terraform Usage](#example-terraform-usage)
    - [Terraform Plug-in Based Architecture](#terraform-plug-in-based-architecture)
      - [Install The Official Terraform AWS Provider](#install-the-official-terraform-aws-provider)
      - [View The Required Providers](#view-the-required-providers)
    - [Configure AWS Provider](#configure-aws-provider)
      - [Configure Terraform AWS Provider](#configure-terraform-aws-provider)
      - [Configure AWS Credentials for Terraform provider](#configure-aws-credentials-for-terraform-provider)
        - [Static credentials](#static-credentials)
        - [Environment variables](#environment-variables)
        - [Shared credentials/configuration file](#shared-credentialsconfiguration-file)

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

#### Format HCL Files

```sh
terraform fmt
```

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

### Hashicorp Configuration Language (HCL)

```hcl
# Template
<BLOCK TYPE> "<BLOCK LABEL>" "<BLOCK IDENTIFIER>" {

 # Block body
<IDENTIFIER> = <EXPRESSION> # Argument
}

# AWS EC2 Example (Resource Block)
resource "aws_instance" "web_server" { # BLOCK
  ami = "ami-04d29b6f966df1537" # Argument 1
  instance_type = var.instance_type # Argument 2
}
```

- The `IDENTIFIER` has to be unique. i.e. web_server_1, web_server_2, etc.

- Terraform Code Configuration block types include:
  - Terraform Settings Block
  - Terraform Provider Block
  - Terraform Resource Block
  - Terraform Data Block
  - Terraform Input Variables Block
  - Terraform Local Variables Block
  - Terraform Output Values Block
  - Terraform Modules Block

### Terraform Resource Block

```hcl
# AWS EC2 Example (Resource Block)
resource "aws_instance" "web_server" { # BLOCK
  ami = "ami-04d29b6f966df1537" # Argument 1
  instance_type = var.instance_type # Argument 2
}
```

### Terraform Input Variable Block

```hcl
# Define input variables (variables.tf)
variable "instance_type" {
  type = string
  description = "Type of instance to launch (e.g., t2.micro)"
  default = "t2.micro"
}

variable "ami" {
  type = string
  description = "ID of the AMI image to use for the instance"
  default = "ami-0c55b159cbfafe1f0"
}

# === Access The variables
# Resource using the input variables
resource "aws_instance" "web_server" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

### Terraform Data Block

```hcl
data "aws_s3_bucket" "example_bucket" {
  bucket = "my-existing-bucket-name"
}
```

### Terraform Provider Block

```hcl
# Configure the AWS provider
provider "aws" {
  region = "us-east-1"  # Specify the AWS region

  # Optional configuration options
  # alias = "east"  # Assign an alias for this provider configuration (optional)
  # source  = "hashicorp/aws"  # Explicitly define the provider source (usually inferred)
}

# Resource using the AWS provider
resource "aws_instance" "web_server" {
  ami           = "ami-0f782182b15e348b2"  # AMI ID for the web server image
  instance_type = "t2.micro"             # Instance type for the web server
}
```

### Example Terraform Usage

- Export your creds.

```sh
export AWS_ACCESS_KEY_ID="<YOUR ACCESS KEY>"
export AWS_SECRET_ACCESS_KEY="<YOUR SECRET KEY>"
```

```hcl
# === main.tf ===
# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Retrieve the list of AZs in the current AWS region
data "aws_availability_zones" "available" {}
data "aws_region" "current" {}

# Define the VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.vpc_cidr

  tags = {
    Name        = var.vpc_name
    Environment = "demo_environment"
    Terraform   = "true"
  }
}

# Deploy the private subnets
resource "aws_subnet" "private_subnets" {
  for_each          = var.private_subnets
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, each.value)
  availability_zone = tolist(data.aws_availability_zones.available.names)[each.value]

  tags = {
    Name      = each.key
    Terraform = "true"
  }
}

# Deploy the public subnets
resource "aws_subnet" "public_subnets" {
  for_each                = var.public_subnets
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, each.value + 100)
  availability_zone       = tolist(data.aws_availability_zones.available.names)[each.value]
  map_public_ip_on_launch = true

  tags = {
    Name      = each.key
    Terraform = "true"
  }
}

# Create route tables for public and private subnets
# Other config goes here ...


# === variables.tf ===
variable "aws_region" {
  type    = string
  default = "us-east-1"
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

```

- The first step to using Terraform is initializing the working directory. Run the following command:

```sh
terraform init
```

- To preview the changes , run the following command:

```sh
terraform plan
```

- Create the AWS resources defined in the configuration file(s) by running:

```sh
terraform apply -auto-approve
```

- To destroy the resources, run the following command:

```sh
terraform destroy -auto-approve
```

### Terraform Plug-in Based Architecture

- Terraform relies on plugins called "providers" to interact with remote systems and expand functionality.
- Terraform configurations must declare which providers they require so that Terraform can install and use them. This is performed within a Terraform configuration block.
- List of the official Terraform providers can be found [here](https://registry.terraform.io/).

#### Install The Official Terraform AWS Provider

```hcl
# filename: terraform.tf

terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.41.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}
```

- To install the provider(s), run:

```sh
terraform init
```

#### View The Required Providers

- If you ever would like to know which providers are installed in your working directory and those required by the configuration, you can issue a terraform version and terraform providers command.

```sh
terraform version
```

### [Configure AWS Provider](https://github.com/btkrausen/hashicorp/blob/master/terraform/Hands-On%20Labs/Section%2004%20-%20Understand%20Terraform%20Basics/04%20-%20Intro_to_the_Terraform_Provider_Block.md)

#### Configure Terraform AWS Provider

- Edit the provider block within the main.tf to configure the Terraform AWS provider.
- This informs Terraform that it will deploy services into the `us-east-1 region` within AWS.

```hcl
# filename: terraform.tf

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}
```

#### Configure AWS Credentials for Terraform provider

- The AWS Terraform provider offers a flexible means of providing credentials for authentication.
- The following methods are supported:

##### Static credentials

- Static credentials can be provided by adding an access_key and secret_key in-line in the AWS provider block:

```hcl
provider "aws" {
  region     = "us-east-1"
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}
```

##### Environment variables

- You can provide your credentials via the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, environment variables, representing your AWS Access Key and AWS Secret Key, respectively.

```hcl
provider "aws" {
}
```

```sh
export AWS_ACCESS_KEY_ID="anaccesskey"
export AWS_SECRET_ACCESS_KEY="asecretkey"
export AWS_DEFAULT_REGION="us-east-1"
```

##### Shared credentials/configuration file

- You can use an AWS credentials or configuration file to specify your credentials.
- The default location is `$HOME/.aws/credentials` on Linux and macOS, or `"%USERPROFILE%\.aws\credentials"` on Windows.
- You can optionally specify a different location in the Terraform configuration by providing the `shared_credentials_file` argument or using the `AWS_SHARED_CREDENTIALS_FILE` environment variable.
- This method also supports a profile configuration and matching AWS_PROFILE environment variable.

```hcl
provider "aws" {
  region                  = "us-east-1"
  shared_credentials_file = "/Users/tf_user/.aws/creds"
  profile                 = "customprofile"
}
```
