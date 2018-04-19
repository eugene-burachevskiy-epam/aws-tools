#!/usr/bin/python3

#
#       Starting/Stoping EC2 isntance by its instance_id. 
#
# Usage example:
# ~$ ./ec2runner.py stop i-007f29708864cc40b
# ~$ Response code: 200
# ~$ Instance:i-007f29708864cc40b running => stopping
#

import boto3, argparse, pprint
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser(description='EC2 instances stopping.')
parser.add_argument('action', action="store", help='start|stop')
parser.add_argument('instance_id', action="store", help='EC2 instance_id to stop')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/config profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using "default" for your profile if not set')
parser.add_argument('-t', '--test', action="store_true", help='Perform a DryRun')
args = parser.parse_args()


if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()

if args.aws_region:
    ec2 = session.client('ec2', region_name=args.aws_region)
else:
    ec2 = session.client('ec2')


if args.action == 'stop':
    if args.test:
        try:
            response = ec2.stop_instances(InstanceIds=[args.instance_id], DryRun=True)
            print(response)           
        except ClientError as e:
            print(e)
    else:
        try:
            response = ec2.stop_instances(InstanceIds=[args.instance_id], DryRun=False)
            print('Response code: ' + str(response['ResponseMetadata']['HTTPStatusCode']))
            print('Instance:' + response['StoppingInstances'][0]['InstanceId'] + ' ' + response['StoppingInstances'][0]['PreviousState']['Name'] + ' => ' + response['StoppingInstances'][0]['CurrentState']['Name'])
        except ClientError as e:
            print(e)  
elif args.action == 'start':
    if args.test:
        try:
            response = ec2.start_instances(InstanceIds=[args.instance_id], DryRun=True)
            print(response)
        except ClientError as e:
            print(e)
    else:
        try:
            response = ec2.start_instances(InstanceIds=[args.instance_id], DryRun=False)
            print('Response code: ' + str(response['ResponseMetadata']['HTTPStatusCode']))
            print('Instance:' + response['StartingInstances'][0]['InstanceId'] + ' ' + response['StartingInstances'][0]['PreviousState']['Name'] + ' => ' + response['StartingInstances'][0]['CurrentState']['Name'])
        except ClientError as e:
            print(e)
elif args.action == 'terminate':
    if args.test:
        try:
            response = ec2.terminate_instances(InstanceIds=[args.instance_id], DryRun=True)
            print(response)
        except ClientError as e:
            print(e)
    else:
        try:
            response = ec2.terminate_instances(InstanceIds=[args.instance_id], DryRun=False)
            print('Response code: ' + str(response['ResponseMetadata']['HTTPStatusCode']))
            #print('Instance:' + response['StartingInstances'][0]['InstanceId'] + ' ' + response['StartingInstances'][0]['PreviousState']['Name'] + ' => ' + response['StartingInstances'][0]['CurrentState']['Name'])
        except ClientError as e:
            print(e)
else:
    print('Action ' + str(args.action) + ' not definied! Use "ec2run.py --help" for details!')
    exit(1)

