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
      - [Generating a Terraform Plan](#generating-a-terraform-plan)
      - [Generating a Terraform Plan File](#generating-a-terraform-plan-file)
      - [Applying a Terraform Plan](#applying-a-terraform-plan)
      - [List All The Currently Managed Resources By Terraform](#list-all-the-currently-managed-resources-by-terraform)
      - [Terraform Destroy](#terraform-destroy)
    - [Hashicorp Configuration Language (HCL)](#hashicorp-configuration-language-hcl)
      - [Terraform Resource Block](#terraform-resource-block)
      - [Terraform Input Variable Block](#terraform-input-variable-block)
      - [Terraform Data Block](#terraform-data-block)
      - [Terraform Provider Block](#terraform-provider-block)
      - [Terraform Outputs Block](#terraform-outputs-block)
    - [Example Terraform Usage](#example-terraform-usage)
    - [Terraform Plug-in Based Architecture](#terraform-plug-in-based-architecture)
      - [Install The Official Terraform AWS Provider](#install-the-official-terraform-aws-provider)
      - [View The Required Providers](#view-the-required-providers)
    - [Configure AWS Provider](#configure-aws-provider)
      - [Configure Terraform AWS Provider](#configure-terraform-aws-provider)
      - [Configure AWS Credentials for Terraform Provider](#configure-aws-credentials-for-terraform-provider)
        - [Static Credentials](#static-credentials)
        - [Environment Variables](#environment-variables)
        - [Shared Credentials/Configuration File](#shared-credentialsconfiguration-file)
  - [Terraform Resource Blocks](#terraform-resource-blocks)
    - [Resource Blocks Examples](#resource-blocks-examples)
      - [Add A New Resource To Deploy An Amazon S3 Bucket](#add-a-new-resource-to-deploy-an-amazon-s3-bucket)
      - [Configure A Resource From The Random Provider](#configure-a-resource-from-the-random-provider)
    - [Introduction To The Terraform Variables Block](#introduction-to-the-terraform-variables-block)
      - [Variables Template](#variables-template)
      - [Task: Add A New VPC Resource Block By Adding Defaults](#task-add-a-new-vpc-resource-block-by-adding-defaults)
    - [Introduction To The Terraform Locals Block](#introduction-to-the-terraform-locals-block)
      - [Locals Block Template](#locals-block-template)
      - [Access Local Variables](#access-local-variables)
    - [Introduction to the Terraform Data Block](#introduction-to-the-terraform-data-block)
      - [Data Block Template](#data-block-template)
      - [Task: Add A New Data Source To Query The Current AWS Region Being Used](#task-add-a-new-data-source-to-query-the-current-aws-region-being-used)
      - [Syntax For Accessing Data In A Data Block](#syntax-for-accessing-data-in-a-data-block)
      - [Task: Add A New Data Source For Querying A Different Ubuntu Image](#task-add-a-new-data-source-for-querying-a-different-ubuntu-image)
    - [Terraform Import](#terraform-import)
      - [Import An AWS EC2 Instance](#import-an-aws-ec2-instance)
    - [Terraform Workspaces - OSS](#terraform-workspaces---oss)
      - [Terraform Workspaces Use Cases](#terraform-workspaces-use-cases)
      - [Show All The Terraform Workspaces](#show-all-the-terraform-workspaces)
      - [Check The Current Terraform Workspace](#check-the-current-terraform-workspace)
      - [Create New Workspace](#create-new-workspace)
      - [Select Workspace](#select-workspace)
    - [Terraform Modules](#terraform-modules)
      - [Terraform Modules Example](#terraform-modules-example)
      - [Access Local Modules](#access-local-modules)
      - [Install and Apply Module](#install-and-apply-module)
    - [Terraform Module Sources](#terraform-module-sources)
      - [1. Public Module Registry](#1-public-module-registry)
      - [2. Source A Module From GitHub](#2-source-a-module-from-github)
  - [Generate Private Key](#generate-private-key)

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
- `terraform fmt`
- `terraform plan`
- `terraform apply`
- `terraform state list`
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

# Recursively format files
terraform fmt -recursive
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

#### Generating a Terraform Plan

- Terraform has a dry run mode where you can preview what Terraform will change without making any actual changes to your infrastructure.
- This dry run is performed by running a `terraform plan`.

```bash
terraform plan
```

#### Generating a Terraform Plan File

- The terraform plan command with the `-out` option in Terraform allows you to save the generated execution plan to a file.
- This plan outlines the changes Terraform intends to make to your infrastructure if you run terraform apply.

- **Benefits**:
  - By saving the plan, you can analyze the intended infrastructure modifications at your convenience, even without an internet connection.
  - The saved plan file can be easily shared with colleagues for review and discussion before applying the changes.
  - You can integrate the plan file into your version control system to track changes in the planned infrastructure state over time.

```sh
terraform plan -out <plan_name>

# e.g.
terraform plan -out tfplan
```

#### Applying a Terraform Plan

- Run the command below to build the resources within your plan file.

```bash
terraform apply
```

#### List All The Currently Managed Resources By Terraform

- Run the command:

```bash
terraform state list
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

#### Terraform Resource Block

```hcl
# AWS EC2 Example (Resource Block)
resource "aws_instance" "web_server" { # BLOCK
  ami = "ami-04d29b6f966df1537" # Argument 1
  instance_type = var.instance_type # Argument 2
}
```

#### Terraform Input Variable Block

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

# === Access The variables ===
# Resource using the input variables
resource "aws_instance" "web_server" {
  ami           = var.ami
  instance_type = var.instance_type
}
```

#### Terraform Data Block

- A `data block`, also sometimes called a data source block, is used to retrieve information from existing resources or external systems.
- Unlike resource blocks that create or manage infrastructure, data blocks act as a read-only mechanism to fetch specific data points Terraform needs for your configuration.

```hcl
data "aws_s3_bucket" "example_bucket" {
  bucket = "my-existing-bucket-name"
}
```

#### Terraform Provider Block

- A `provider block` is a fundamental element used to configure interactions with external infrastructure platforms or services.
- It essentially acts as a bridge between Terraform and the specific provider you're using to manage resources.

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

#### Terraform Outputs Block

- An `output block` is a way to extract and present data about your infrastructure after it's been provisioned.
- It essentially allows you to export specific values from your Terraform configuration.

```hcl
output "instance_public_ip" {
  value = aws_instance.my_instance.public_ip
  description = "Public IP address of the instance"
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
# ==========================================================
# Provider Block(s)
# ==========================================================
provider "aws" {
  region = "us-east-1"
}

# Retrieve the list of AZs in the current AWS region
data "aws_availability_zones" "available" {}
data "aws_region" "current" {}

# ==========================================================
# Resource Block(s)
# ==========================================================
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

# ==========================================================
# Input Variable Block(s)
# ==========================================================
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

#### Configure AWS Credentials for Terraform Provider

- The AWS Terraform provider offers a flexible means of providing credentials for authentication.
- The following methods are supported:

##### Static Credentials

- Static credentials can be provided by adding an access_key and secret_key in-line in the AWS provider block:

```hcl
provider "aws" {
  region     = "us-east-1"
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}
```

##### Environment Variables

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

##### Shared Credentials/Configuration File

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

## Terraform Resource Blocks

- Terraform uses resource blocks to manage infrastructure, such as virtual networks, compute instances, or higher-level components such as DNS records.
- Resource blocks represent one or more infrastructure objects in your Terraform configuration.
- Most Terraform providers have a number of different resources that map to the appropriate APIs to manage that particular infrastructure type.

```hcl
# Template
<BLOCK TYPE> "<BLOCK LABEL>" "<BLOCK LABEL>" {

  # Block body
  <IDENTIFIER> = <EXPRESSION> # Argument
}
```

| Resource   | AWS Provider       | AWS Infrastructure |
| ---------- | ------------------ | ------------------ |
| Resource 1 | aws_instance       | EC2 Instance       |
| Resource 2 | aws_security_group | Security Group     |
| Resource 3 | aws_s3_bucket      | AWS S3 Bucket      |
| Resource 4 | aws_key_pair       | AWS Key Pair       |

- When working with a specific provider, like AWS, Azure, or GCP, the resources are defined in the provider documentation.
- Each resource is fully documented in regards to the valid and required arguments required for each individual resource.
- For example, the `aws_key_pair` resource has a "Required" argument of `public_key` but optional arguments like `key_name` and `tags`.
- You'll need to look at the provider documentation to understand what the supported resources are and how to define them in your Terraform configuration.

```hcl
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    gateway_id     = aws_internet_gateway.internet_gateway.id
  }

  tags = {
    Name      = "demo_public_rtb"
    Terraform = "true"
  }
}
```

> Note: Your resource blocks must have a unique resource id (combination of resource type along with resource name). In our example, our resource id is `aws_route_table.public_route_table`, which is the combination of our `resource type` aws_route_table and `resource name` public_route_table. This naming and interpolation nomenclature is powerful part of HCL that allows us to reference arguments from other resource blocks.

### Resource Blocks Examples

#### Add A New Resource To Deploy An Amazon S3 Bucket

- [Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls)

```hcl
resource "aws_s3_bucket" "my-new-S3-bucket" {
  bucket = "my-new-tf-test-bucket-bryan"

  tags = {
    Name = "My S3 Bucket"
    Purpose = "Intro to Resource Blocks Lab"
  }
}

resource "aws_s3_bucket_ownership_controls" "my_new_bucket_acl" {
  bucket = aws_s3_bucket.my-new-S3-bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
```

#### Configure A Resource From The Random Provider

- Terraform supports many resources that don't interact with any other services.
- It's a provider that can be used to create random data to be used in your Terraform.
- e.g. add a new resource block to Terraform using the random provider in `main.tf` file and add the following resource block:

```hcl
resource "random_id" "randomness" {
  byte_length = 16
}

# Reference the random ID
resource "aws_s3_bucket" "my-new-S3-bucket" {
  bucket = "my-new-tf-test-bucket-${random_id.randomness.hex}"

  tags = {
    Name    = "My S3 Bucket"
    Purpose = "Intro to Resource Blocks Lab"
  }
}
```

### Introduction To The Terraform Variables Block

- **Variable Declaration and Organization**:
  - Variables are typically declared in a separate file named `variables.tf`, although this is not mandatory.
  - Organizing variable declarations in one file streamlines management and enhances clarity.
  - Each variable is declared within a variable block, containing essential information such as the `variable name`, `type`, `description`, `default value`, and `additional options`.

- **Focus on Reusability and DRY Development**:
  - Terraform templates benefit from a focus on reusability and DRY (Don't Repeat Yourself) development practices.
  - Utilizing variables is key to simplifying and enhancing the usability of Terraform configurations.

- **Input Variables for Customization**:
  - Input variables, often referred to simply as "variables," enable customization of aspects within a module or configuration without modifying its source code directly.
  - This flexibility facilitates sharing modules across different configurations.

#### Variables Template

```hcl
variable “<VARIABLE_NAME>” {
  # Block body
  type = <VARIABLE_TYPE>
  description = <DESCRIPTION>
  default = <EXPRESSION>
  sensitive = <BOOLEAN>
  validation = <RULES>
}

# e.g.
variable "aws_region" {
  type        = string
  description = "region used to deploy workloads"
  default     = "us-east-1"
  validation {
    condition     = can(regex("^us-", var.aws_region))
    error_message = "The aws_region value must be a valid region in the
    USA, starting with \"us-\"."
  }
}
```

#### Task: Add A New VPC Resource Block By Adding Defaults

```hcl
# filename: variables.tf
variable "variables_sub_cidr" {
  description = "CIDR Block for the Variables Subnet"
  type        = string
  default     = "10.0.250.0/24"
}

variable "variables_sub_az" {
  description = "Availability Zone used Variables Subnet"
  type        = string
  default     = "us-east-1a"
}

variable "variables_sub_auto_ip" {
  description = "Set Automatic IP Assigment for Variables Subnet"
  type        = bool
  default     = "true"

}
```

- Access the variables

```hcl
# filename: main.tf
resource "aws_subnet" "variables-subnet" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = var.variables_sub_cidr
  availability_zone       = var.variables_sub_az
  map_public_ip_on_launch = var.variables_sub_auto_ip

  tags = {
    Name      = "sub-variables-${ var.variables_sub_az }"
    Terraform = "true"
  }
}
```

### Introduction To The Terraform Locals Block

- Locals blocks (often referred to as locals) are defined values in Terraform that are used to reduce repetitive references to expressions or values.
- Locals are very similar to traditional input variables and can be referred to throughout your Terraform configuration.

#### Locals Block Template

```hcl
locals {
  # Block body
  local_variable_name = <EXPRESSION OR VALUE>
  local_variable_name = <EXPRESSION OR VALUE>
}

# e.g.
locals {
  team = "api_mgmt_dev"
  application = "corp_api"
  server_name = "ec2-${var.environment}-api-${var.variables_sub_az}"
}
```

- Note: `environment` and `variables_sub_az` are input variables located in `variables.tf`.

#### Access Local Variables

```hcl
resource "aws_instance" "web_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_subnets["public_subnet_1"].id
  tags = {
    Name = local.server_name
    Owner = local.team
    App = local.application
  }
}
```

### Introduction to the Terraform Data Block

- Data sources are used in Terraform to load or query data from APIs or other Terraform workspaces.
- You can use this data to make your project's configuration more flexible, and to connect workspaces that manage different parts of your infrastructure.
- You can also use data sources to connect and share data between workspaces in Terraform Cloud and Terraform Enterprise.
- Data Blocks within Terraform HCL are comprised of the following components:
  - **Data Block**: "resource" is a top-level keyword like "for" and "while" in other programming languages.
  - **Data Type**: The next value is the type of the resource. Resources types are always prefixed with their provider (aws in this case). There can be multiple resources of the same type in a Terraform configuration.
  - **Data Local Name**: The next value is the name of the resource. The resource type and name together form the resource identifier, or ID. In this lab, one of the resource IDs is aws_instance.web. The resource ID must be unique for a given configuration, even if multiple files are used.
  - **Data Arguments**: Most of the arguments within the body of a resource block are specific to the selected resource type. The resource type's documentation lists which arguments are available and how their values should be formatted.

#### Data Block Template

```hcl
data “<DATA TYPE>” “<DATA LOCAL NAME>”   {
  # Block body
  <IDENTIFIER> = <EXPRESSION> # Argument
}
```

#### Task: Add A New Data Source To Query The Current AWS Region Being Used

```hcl
# Retrieve the list of AZs in the current AWS region
data "aws_availability_zones" "available" {}

# === Access the data ===
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
```

#### Syntax For Accessing Data In A Data Block

- `data.<type>.<name>.<attribute>`. e.g. `data.aws_availability_zones.available.names`

#### Task: Add A New Data Source For Querying A Different Ubuntu Image

```hcl
# Terraform Data Block - Lookup Ubuntu 22.04
data "aws_ami" "ubuntu_22_04" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  owners = ["099720109477"]
}

# Modify the aws_instance so it uses the returned AMI
resource "aws_instance" "web_server" {
  ami                         = data.aws_ami.ubuntu_22_04.id
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public_subnets["public_subnet_1"].id
  security_groups             = [aws_security_group.vpc-ping.id]
  associate_public_ip_address = true
  tags = {
    Name = "Web EC2 Server"
  }
}
```

### Terraform Import

- Terraform import is a functionality that allows you to bring existing infrastructure resources under Terraform's management.
- It essentially imports the configuration of these pre-existing resources into your Terraform state file.

#### Import An AWS EC2 Instance

- Assuming an AWS EC2 instance has manually been created (using AWS Console), you need to copy the resource id of the EC2 instance. e.g. id = `1-03db5c21e61154d36`
- Add the resource to the `main.tf` file.

```hcl
# Add manually created resource
resource "aws_instance" "your_instance_name" {}
```

- On the CLI, enter the command:

```sh
# Get help
terraform import -help

terraform import aws_instance.your_instance_name <instance_id>

# e.g.
terraform import aws_instance.demo_server i-0c0505eacad53de2c

```

- Running this throws **`an expected error`** because the resource block is missing required arguments.

```sh
terraform plan

# Get the resource properties
terraform state show aws_instance.demo_server
```

- Update the config file.

```hcl
# Add manually created resource
resource "aws_instance" "your_instance_name" {
  ami             = "ami-080e1f13689e07408" # new!
  instance_type   = "t2.micro"              # new!
}
```

### Terraform Workspaces - OSS

- Terraform workspaces are a mechanism to manage different environments or deployments of your infrastructure using the same Terraform configuration.
- They achieve this by isolating the state files associated with each environment.

#### Terraform Workspaces Use Cases

- Managing separate deployments for `development`, `staging`, and `production` environments.
- Testing infrastructure changes in a dedicated environment before applying them to production.
- Providing different infrastructure configurations for different teams or projects.

#### Show All The Terraform Workspaces

- You can show all the Terraform workspaces with the command:

```sh
terraform workspace list

# Get help
terraform workspace -help
```

#### Check The Current Terraform Workspace

- You can check the current Terraform workspace you are in with the terraform workspace command:

```sh
terraform workspace show
```

#### Create New Workspace

```sh
terraform workspace new <workspace_name>

# e.g.
terraform workspace new development
```

#### Select Workspace

```sh
terraform workspace select <workspace_name>

# e.g.
terraform workspace select default
```

### Terraform Modules

- A `Terraform module` is a way to package and reuse a set of Terraform configuration files.
- It groups resources that perform a specific function or manage a particular infrastructure component together.
- Modules promote code `organization`, `maintainability`, and `sharing` of infrastructure building blocks.

#### Terraform Modules Example

```hcl
# Filename: modules/servers/servers.tf
# ==========================================================
# Input Variable Blocks
# ==========================================================
# Required variables
variable "ami" {}
variable "subnet_id" {}
variable "security_groups" {
  type = list(any)
}
# Optional variable (coz it has default=...)
variable "size" {
  default = "t2.micro"
}


# ==========================================================
# Resource Block(s)
# ==========================================================
# It expects 4 arguments (1 is optional)
resource "aws_instance" "web" {
  ami                    = var.ami
  instance_type          = var.size
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_groups

  tags = {
    "Name"        = "Server from Module"
    "Environment" = "Training"
  }
}

# ==========================================================
# Output Blocks
# ==========================================================
output "public_ip" {
  value = aws_instance.web.public_ip
  description = "Public IP address of the instance"
}

output "public_dns" {
  value = aws_instance.web.public_dns
  description = "Public DNS of the instance"
}
```

#### Access Local Modules

- In your root configuration (also called your root module) `/workspace/terraform/main.tf`, we can call our new server module with a Terraform module block.
- Remember that terraform only works with the configuration files that are in it's current working directory.
- Modules allow us to reference Terraform configuration that lives outside of our working directory.
- In this case we'll incorporate all configuration that is both inside our working directory (root module) and inside the server directory (child module).

```hcl
# It takes 4 arguments but 3 are required
module "server" {
  source          = "./modules/server"
  ami             = data.aws_ami.ubuntu.id
  subnet_id       = aws_subnet.public_subnets["public_subnet_3"].id
  security_groups = [
    aws_security_group.vpc-ping.id,
    aws_security_group.ingress-ssh.id,
    aws_security_group.vpc-web.id
  ]
}
```

#### Install and Apply Module

- Terraform configuration files located within modules are pulled down by Terraform during initialization, so any time you add or update a module version you must run a `terraform init`.

```sh
terraform init
```

### Terraform Module Sources

- Modules can be sourced from a number of different locations, including both local and remote sources.
- The `Terraform Module Registry`, `HTTP urls` and `S3 buckets` are examples of remote sources, while folders and subfolders are examples of local sources.
- Support for various module sources allow you to include Terraform configuration from a variety of locations while still providing proper organization of code.

#### 1. Public Module Registry

- [Auto Scaling Docs](https://registry.terraform.io/modules/terraform-aws-modules/autoscaling/aws/latest)
- Terraform Public Registry is an index of modules shared publicly. This public registry is the easiest way to get started with Terraform and find modules created by others in the community.
- You can also use a private registry as a feature of Terraform Cloud/Terraform Enterprise.
- Modules on the public Terraform Registry can be sourced using a registry source address of the form `//`, with each module's information page on the registry site including the exact address to use.
- Example:
  - We will use the `AWS Autoscaling module` to deploy an AWS Autoscaling group to our environment.
  - Update the `main.tf` to include this module from the Terraform Module Registry.

```hcl
module "autoscaling" {
  source  = "terraform-aws-modules/autoscaling/aws"
  version = "4.9.0"

  # Autoscaling group
  name = "myasg"

  vpc_zone_identifier = [aws_subnet.private_subnets["private_subnet_1"].id,
  aws_subnet.private_subnets["private_subnet_2"].id,
  aws_subnet.private_subnets["private_subnet_3"].id]
  min_size            = 0
  max_size            = 1
  desired_capacity    = 1

  # Launch template
  use_lt    = true
  create_lt = true

  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags_as_map = {
    Name = "Web EC2 Server 2"
  }
}
```

- Any time that the source of a module is updated or added to our configuration, the working directory needs to be reintilized.

```sh
terraform init
```

- We can follow that by issuing a terraform plan to see that additional resources that will be added by using the module.

```sh
terraform plan -out tfplan
```

- Once we are happy with how the module is behaving we can issue a terraform apply.

```sh
terraform apply tfplan
```

#### 2. Source A Module From GitHub

- Another source of modules that we can use are those that are published directly on `GitHub`.
- Terraform will recognize unprefixed github.com URLs and interpret them automatically as Git repository sources.
- Let's update the source of our autoscaling group module from the Public Module registry to use github.com instead.
- This will require us to remove the `version` argument from our module block.

```hcl
module "autoscaling" {
  source = "github.com/terraform-aws-modules/terraform-aws-autoscaling?ref=v4.9.0"

  # Autoscaling group
  name = "myasg"

  vpc_zone_identifier = [aws_subnet.private_subnets["private_subnet_1"].id,
  aws_subnet.private_subnets["private_subnet_2"].id,
  aws_subnet.private_subnets["private_subnet_3"].id]
  min_size            = 0
  max_size            = 1
  desired_capacity    = 1

  # Launch template
  use_lt    = true
  create_lt = true

  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  tags_as_map = {
    Name = "Web EC2 Server 2"
  }
}
```

- Re-intilize the providers.

```sh
terraform init
```

- We can follow that by issuing a terraform plan to see that additional resources that will be added by using the module.

```sh
terraform plan -out tfplan
```

- Once we are happy with how the module is behaving we can issue a terraform apply.

```sh
terraform apply tfplan
```

## Generate Private Key

- Instead of using this:

```hcl
resource "aws_key_pair" "generated" {
  key_name   = "MyAWSKey"
  public_key = tls_private_key.generated.public_key_openssh
}
```

- Use this!

```sh
ssh-keygen -t rsa -b 4096 -m PEM -f path/to/your/key>/your_key_name.pem

# e.g.
ssh-keygen -t rsa -b 4096 -m PEM -f ${PWD}/MyAWSKey.pem
```

- Update the config code.

```hcl
resource "aws_key_pair" "imported_key" {
  key_name   = "MyAWSKey"
  public_key = file("path/to/your/public_key.pem.pub")
}

```
