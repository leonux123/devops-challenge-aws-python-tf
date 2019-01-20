# Devops POC - Infra as code using TF and Python.

## Description

The script will create an EC2 instance (using Terraform) in the specified AWS Region with the selected EC2 Instance Type.


## Requirements

- [x] Script should use Boto3 library.
- [x] Terraform templates format will be **json**.
- [x] The script will receive 2 parameters: EC2 Instance Type (required), AWS Region (optional)
- [x] Instance will be created within the AWS Region provided in the script parameter. Default to **us-east-1**.
- [x] The EC2 Instance Type will be the one provided in the script parameter. Make sure this parameter is constraint to be a valid EC2 Instance Type. Default to **t2.micro**.
- [x] The script will pass the parameters received from the CLI to the Terraform template.
- [x] The EC2 instance will have a cloud-init script that installs **cowsay** command when the instance gets created.
- [x] Grant access to the EC2 instance via SSH (port 22).
- [x] Select the default VPC for the EC2 instance.

## Pre-requisites

- Create security group in AWS to allow SSH access (port 22) for all regions.
- Import your [public key](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#how-to-generate-your-own-key-and-import-it-to-aws) for all AWS regions. Use this script: `AWS CLI scripts/aws_import_keys.sh`


## System dependencies

> python, Boto3 library, AWS CLI, Linux environment, Terraform.

## Script config

An initial script configuration is required in order to set your AWS account credentials+EC2 info. Please edit the following files accordingly:

### Update `tfvariables.template` file
```
      "sec_group": {
        "default": "YOUR-SSH-SEC-GROUP"
      },
      "key_name": {
        "default": "YOUR-KEY-NAME"
      },
```

### Update `terraform/terraform.tfvars.json` file
```
{
  "access_key": "YOUR-ACCESS-KEY",
  "secret_key": "YOUR-SECRET-KEY"
}
```
Once the above files are updated with your AWS account credentials+EC2 info, you're ready to run the script.

## Installation

```bash
$ git clone git@github.com:leonux123/devops-challenge-aws-python-tf.git
$ cd devops-challenge-aws-python-tf/
$ chmod +x provision_EC2_infra.py
$ ./provision_EC2_infra.py -h
```

## Usage

### Commands:
```
-h, --help   | Displays help information and the list of valid arguments.
-r, --region | AWS Region. Examples: us-west-1, us-west-2, etc...
```

### Basic usage

The script expects 2 arguments: EC2 Instance Type (required), AWS Region (optional).

Valid scenarios:

```bash
$ ./provision_EC2_infra.py t2.micro
```
Note: If AWS Region is missing, it will be defaulted to: **us-east-1**.

```bash
$ ./provision_EC2_infra.py t2.micro -r us-west-2
```

Note: Only Free tier instance types are allowed: **t1.micro**, **t2.micro**.

## Notes

- I'm using Boto3 library to retrieve all EC2 running instances and displaying that to the terminal. That way you can make sure that the new instance was actually created, by comparing Terraform output vs AWS CLI information.

- The script will also display to the terminal the public IP address of the new created EC2 instance via Terraform output. You can SSH to that IP address and validate that "cowsay" was installed during launch process.
```
$ ssh -i "YOUR-KEY-NAME.pem" ec2-user@PUBLIC-IP-ADDRESS
$ cowsay HELLO!
```

- In order to be able to create an EC2 instance across AWS regions, a valid AMI id should be passed to the script. This could be easily achieved by using a [Data Source Configuration](https://www.terraform.io/docs/configuration/data-sources.html) in HCL format, which will search and filter for a specific pattern in the AMI name that can match across regions. Hashicorp has multiple known issues when working with Data Sources in json format. Example: [#13037](https://github.com/hashicorp/terraform/issues/13037). This is expected to be fixed until [version 0.12](https://www.hashicorp.com/blog/terraform-0-12-reliable-json-syntax) is released. Because of that, I decided to get a list of valid AMI ids via AWS CLI for all regions (see: `AWS CLI scripts/aws_valid_amis.sh`) and create a map variable in Terraform that will be passed to the TF template depending on the selected AWS region.

- The script only allows to select between Free Tier EC2 instance types now but this can be easily modified by updating the choices for the given argument.
