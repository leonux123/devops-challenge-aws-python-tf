#!/usr/bin/python
import boto3, os, sys, argparse, json
from collections import OrderedDict

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("awsInstanceType", help="AWS Instace type. Free Tier only.", choices=['t1.micro', 't2.micro'])

    # Optional arguments
    parser.add_argument("-r", "--region", help="AWS Region. Examples: us-west-1, us-west-2, etc...", default='us-east-1')

    # Parse arguments
    args = parser.parse_args()

    return args

# A function to map argument values into json templates.
def updateJsonTemplates(awsInstanceType, region):

    with open('tfvariables.template', 'r') as file:
         json_data = json.load(file, object_pairs_hook=OrderedDict)
         for item in json_data:
               if item['variable']['instance_type']['default'] in ["t2.micro"]:
                  item['variable']['instance_type']['default'] = awsInstanceType
               if item['variable']['region']['default'] in ["us-east-1"]:
                  item['variable']['region']['default'] = region
    with open('out_tfvariables.json', 'w') as file:
        json.dump(json_data, file, sort_keys=False, indent=2)

    with open('terraform.template', 'r') as file:
         json_data = json.load(file, object_pairs_hook=OrderedDict)
         for item in json_data:
               if item['resource']['aws_instance']['myNode']['ami'] in ["${var.ami_id[\"us-east-1\"]}"]:
                  item['resource']['aws_instance']['myNode']['ami'] = '${var.ami_id[\"'+region+'\"]}'
    with open('out_tftemplate.json', 'w') as file:
        json.dump(json_data, file, sort_keys=False, indent=2)

    return

# A function to retrieve EC2 running instances.
def getAWSRunningInstances(region):

    session = boto3.Session()
    ec2 = session.resource('ec2', region)

    instances = []
    result = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in result:
        instances.append(instance.id)

    print "Current Running Instances in AWS: ",instances

    return

if __name__ == '__main__':
    args = parseArguments()
    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))

    # Run functions and script logic:
    updateJsonTemplates(args.awsInstanceType, args.region)

    # Remove unwanted characters from templates.
    os.system("head -c -1 < out_tfvariables.json | tail -c +2 > ./terraform/variables.tf.json")
    os.system("head -c -1 < out_tftemplate.json | tail -c +2 > ./terraform/template.tf.json")

    # Delete temp files.
    os.remove("out_tfvariables.json")
    os.remove("out_tftemplate.json")

    tf_init = 'cd terraform/ && terraform init -input=false && terraform plan -out=tfplan -input=false && terraform apply -input=false tfplan'
    os.system(tf_init)

    getAWSRunningInstances(args.region)
