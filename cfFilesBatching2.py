import json
import pandas as pd
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
import concurrent.futures


prompts_list = []
def add_prompts():
    prompts_list.append("Create a CloudFormation template to create PrivateLink infrastructure.")
    prompts_list.append("Creat a AWS CloudFormation Sample Template AppRunnerService: This template demonstrates the creation of a App Runner Service from existing ECR Repository.")
    prompts_list.append("Create a AWS CloudFormation template for a multi-az, load balanced and Auto Scaled sample web site running on an Apache Web Server. The application is configured to span all Availability Zones in the region and is Auto-Scaled based on the CPU utilization of the web servers. Notifications will be sent to the operator email address on scaling events. The instances are load balanced with a simple health check against the default web page.")
    prompts_list.append("Create a AWS CloudFormation Sample Template ELBGuidedAutoScalingRollingUpdates: This tempplate creates an auto scaling group behind a load balancer with a simple health check. The Auto Scaling launch configuration includes an update policy that will keep 2 instances running while doing an autoscaling rolling update. The update will roll forward only when the ELB health check detects an updated instance in-service.")
    prompts_list.append("Create a AWS CloudFormation template for a load balanced, Auto Scaled sample website. This example creates an Auto Scaling group with time-based scheduled actions behind a load balancer with a simple health check.")
    prompts_list.append("Create a template for date macro for Cloudformation. Provides functions for date manipulation in your CloudFormation templates including getting the current date, and doing date math. Written in Python.")
    prompts_list.append("Create a ARN for the Permission Boundary Policy")
    prompts_list.append("Create a AWS Cloudformation that uses the Fn::ForEach function to create mutiple tables.")
    prompts_list.append("Create a AWS CloudFormation template for an Aurora RDS instance and DMS instance in a VPC, and an S3 bucket. The Aurora RDS instance is configured as the DMS Source Endpoint and the S3 bucket is configured as the DMS Target Endpoint. A DMS task is created and configured to migrate existing data and replicate ongoing changes from the source endpoint to the target endpoint.")
    prompts_list.append("Create a CloudFormation template which shows how to provide multiple values to one StringValue when creating a DataPipeline definition.")
    prompts_list.append("Create a AWS CloudFormation template for a DynamoDB table with local and global secondary indexes.")
    prompts_list.append("Create a AWS CloudFormation template for an Amazon EC2 instance running the Amazon Linux AMI. The AMI is chosen based on the region in which the stack is run. This example creates an EC2 security group for the instance to give you SSH access.")
    prompts_list.append("Create a AWS CloudFormation template for an Amazon EC2 instance with cfn-init and cfn-signal.")
    prompts_list.append("Createa AWS CloudFormation template for a single EC2 instance with a single ENI which has multiple private and public IPs.")
    prompts_list.append("Create a AWS CloudFormation template for a Multi-AZ EFS with automount EFS.")
    prompts_list.append("Create a AWS CloudFormation Sample Template EKS Cluster on EC2.")
    prompts_list.append("Create a AWS CloudFormation template for a VPC containing two subnets and an auto scaling group containing instances with Internet access.")
    prompts_list.append("Create a AWS CloudFormation template for an auto scaling group behind a load balancer with a simple health check. The Auto Scaling launch configuration includes an update policy that will keep 2 instances running while doing an autoscaling rolling update. The update will roll forward only when the ELB health check detects an updated instance in-service.")
    prompts_list.append("Create a AWS CloudFormation template for two EC2 instances behind a load balancer with a simple health check. The ec2 instances are untargeted and may be deployed in one or more availaiblity zones. The web site is available on port 80, however, the instances can be configured to listen on any port (8888 by default).")
    prompts_list.append("Create a AWS CloudFormation template for a load balanced, Auto Scaled sample website where the instances are locked down to only accept traffic from the load balancer. This example creates an Auto Scaling group behind a load balancer with a simple health check. The web site is available on port 80, however, the instances can be configured to listen on any port (8888 by default).")
    prompts_list.append("Create a AWS CloudFormation template for a load balanced, scalable sample website using Elastic Load Balancer attached to an Auto Scaling group. The ELB has connection draining enabled and also puts access logs into an S3 bucket.")
    prompts_list.append("Create a AWS CloudFormation template for a Network Load Balancer in 2 AZs with EIPs listening on TCP port 80. There are no registered targets these would either be EC2 instance IDs added to the targets property of the target group  or defined under the autoscaling group resources.")
    prompts_list.append("Create a AWS CloudFormation template for Greengrass resources and group, with supporting AWS services.")
    prompts_list.append("Create a AWS CloudFormation template for a Channel, Datastore, Pipeline and Dataset with SQL action.")
    prompts_list.append("Create a AWS CloudFormation template to automatically provision AWS Neptune Graph Database through optimized CI/CD method with AWS CloudWatch and AWS SNS.")
    prompts_list.append("Create a AWS CloudFormation template for a highly-available, RDS DBInstance with a read replica.")
    prompts_list.append("Create a AWS CloudFormation template for an RDS DBInstance that is snapshotted on stack deletion.")
    prompts_list.append("Create an Amazon RDS Database Instance with a DBParameterGroup.")
    prompts_list.append("Creat a AWS CloudFormation template for a secure bucket that passes default security scanning checks.  Includes a bucket to store replicas and an access log bucket. Server side encryption is enabled. Public access is disabled. The bucket policy requires secure transport.")
    prompts_list.append("Create a AWS CloudFormation template for a static website using S3 and CloudFront that passes typical compliance checks.")
    prompts_list.append("Create a AWS CloudFormation template for an AD Connector to connect to an on-premises directory. Tasks to accomplish: (1) create AD Connector (2) option to create seamless domain join resources for Windows & Linux EC2 instances (3) option to create a domain members security group that allows all PrivateIP communications inbound (4) option to create DHCPOptionSet pointing to Domain DNS servers.")
    prompts_list.append("Create a AWS CloudFormation template that deploys a VPC with a pair of private subnets spread across two Availabilty Zones. It deploys a VPC Endpoint for CloudFormation so an instance in the private subnet can use cfn-signal for its CreationPolicy.")
    prompts_list.append("Create a AWS CloudFormation template for one Linux and three Windows EC2 instances and joins them to Active Directory using the 'AWS-JoinDirectoryServiceDomain' SSM document via AD Connector or AWS Managed AD directory. By default, it relies on the DNS servers being used by the EC2 instances knowing how to resolve the AD domain (i.e., Route 53 Resolvers, DHCP OptionsSet), with an option to set the DNS servers manually on the EC2 instances, as necessary. Several methods used to initiate the domain join (1) Windows EC2 instance with inline SSM association (2) Windows and Linux EC2 instance with SSM association targeting EC2 instance IDs (3) Windows EC2 instance with SSM association targeting EC2 instance tags")

    print("Number of prompts: ", len(prompts_list))

add_prompts()

error_list = [None]*165
# Function to process each item in prompts_list
def process_prompt(x, criteria):
    print(x)
    for y in range(5):
        client = OpenAI(api_key='')
        model = "gpt-4o"
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output only AWS CloudFormation JSON based on the given criteria."},
                {"role": "user", "content": f"Here is the criteria: {criteria}"}
            ],
        )
        output = response.choices[0].message.content

        try:
            my_json = json.loads(output)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            my_json = None

        file_path = f'/Users/map/Documents/JSON_run_v2/JSONwork_batching6/json_set_1/JSONtemplate{x*5 + y+1}.json'
        with open(file_path, 'w') as f:
            json.dump(my_json, f)
    
        s = subprocess.getstatusoutput(f'cfn-lint {file_path}')
        error_list[x*5 + y] = s[1]

    return s[1]

# List to hold all errors
all_errors = []

# Run the loop in parallel using ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_prompt, x, prompts_list[x]) for x in range(len(prompts_list))]
    for future in concurrent.futures.as_completed(futures):
        all_errors.extend(future.result())

# Save the errors to a CSV
df = pd.DataFrame(error_list, columns=["Errors"])
df.to_csv('/Users/map/Documents/JSON_run_v2/JSONwork_batching6/errorCSVs/errorsCSV1.csv', index=False)



# Load the errors CSV
errorsDF = pd.read_csv('/Users/map/Documents/JSON_run_v2/JSONwork_batching6/errorCSVs/errorsCSV4.csv')
error_list = errorsDF.values.tolist()
Error_list = error_list

# Function to process each JSON file and fix errors
def process_json(z, x, Error_list):
    if x == 0:
        error = Error_list[z][0]
    else:
        error = Error_list[z]
    
    file_path = f'/Users/map/Documents/JSON_run_v2/JSONwork_batching6/json_set_{x+1}/JSONtemplate{z+1}.json'

    with open(file_path) as f:
        my_json = json.dumps(json.load(f))

    if type(error) != float:
        client = OpenAI(api_key='')
        model = "gpt-4o"
        response = client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to take in input JSON and output only JSON."},
                {"role": "user", "content": f"Generate a new CloudFormation JSON object that fixes the error in the old JSON object. Here is the old JSON object: {my_json}. Here is the error: {error}."}
            ],
        )
        output = response.choices[0].message.content
    else:
        output = my_json

    try:
        new_json = json.loads(output)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        new_json = None

    new_file_path = f'/Users/map/Documents/JSON_run_v2/JSONwork_batching6/json_set_{x+2}/JSONtemplate{z+1}.json'
    with open(new_file_path, 'w') as f:
        json.dump(new_json, f)

    s = subprocess.getstatusoutput('cfn-lint ' + new_file_path)
    return s[1]

# Iterate over the error lists
for x in range(9):
    print(x)
    new_error_list = [None]*165
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        future_to_z = {executor.submit(process_json, z, x, Error_list): z for z in range(165)}
        for future in as_completed(future_to_z):
            z = future_to_z[future]
            try:
                result = future.result()
            except Exception as exc:
                print(f'JSON template {z+1} generated an exception: {exc}')
                result = None
            new_error_list[z] = result

    # Save new errors to CSV
    csv_name = f'/Users/map/Documents/JSON_run_v2/JSONwork_batching6/errorCSVs/errorsCSV{x+2}.csv'
    df = pd.DataFrame(new_error_list)
    df.to_csv(csv_name, index=False)
    Error_list = new_error_list
