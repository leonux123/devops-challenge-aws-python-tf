# Devops POC - Infra as code using TF and Python.

## Description

The script will create an EC2 instance (using Terraform) in the specified AWS Region with the selected AWS Instance Type.


## Requirements

- TBD.

## Pre-requisites

- TBD.

## System dependencies

> python, boto3 library, AWS CLI, Linux environment, Terraform.

## Installation

```bash
$ git clone git@github.com:leonux123/devops-challenge-aws-python-tf.git
$ cd devops-challenge-aws-python-tf/
$ chmod +x provision_EC2_infra.py
$ ./provision_EC2_infra.py -h
```

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

## Usage

### Commands:
```
-h, --help   | Displays help information and the list of valid arguments.
-r, --region | AWS Region. Examples: us-west-1, us-west-2, etc...
```

### Basic usage

The script expects 2 arguments: AWS Instance Type (required), AWS Region (optional).

Valid scenarios:

```bash
$ ./provision_EC2_infra.py t2.micro
```
Note: If AWS Region is missing, it will be defaulted to: **us-east-1**.

```bash
$ ./provision_EC2_infra.py t2.micro -r us-west-2
```

Note: Only Free tier instance types are allowed: **t1.micro**, **t2.micro**.
