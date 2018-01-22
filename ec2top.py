#!/usr/bin/python3

#
#     Listing of your AWS EC2 instances.
# App require boto3 AWS-API module, make sure it is installed by running 'sudo pip3 install boto3'
# If no args specified app lists your EC2 instances using .aws/config "Default" profile and region. Use ./ec2top.py --help for possible options
#

import boto3, argparse
from operator import itemgetter

parser = argparse.ArgumentParser(description='AWS EC2 instances listing.')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/config profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using "default" for your profile if not set')
parser.add_argument('-s', '--sort', action="store", dest="sort_key", help='Sort your output by column name. Default sorting is "Name". Other options are Status|Type|VPC|pubIP|privIP ')
args = parser.parse_args()


if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()

if args.aws_region:
    ec2 = session.client('ec2', region_name=args.aws_region)
else:
    ec2 = session.client('ec2')

response = ec2.describe_instances()


#list of Tags dictionaries as input
def instance_name(tags):
    for i in tags:
        if i['Key'] == 'Name':
            return i['Value']


top_list = []

for i in range(len(response['Reservations'])):
    instance = response['Reservations'][i]['Instances'][0]
    top_instance = {}

    top_instance.setdefault('Status', instance['State']['Name'])
    top_instance.setdefault('Type', instance['InstanceType'])
    top_instance.setdefault('Id', instance['InstanceId'])
    if 'Tags' in instance.keys():
        top_instance.setdefault('Name', instance_name(instance['Tags']))
    else:
        top_instance.setdefault('Name', 'None')
        
    if 'PrivateIpAddress' in instance.keys():
        top_instance.setdefault('privIP', instance['PrivateIpAddress'])
    else:
        top_instance.setdefault('privIP', 'None')
    
    if 'PublicIpAddress' in instance.keys():
        top_instance.setdefault('pubIP', instance['PublicIpAddress'])
    else:
        top_instance.setdefault('pubIP', 'None')
    
    if 'VpcId' in instance.keys():
        top_instance.setdefault('VPC', instance['VpcId'])
    else:
        top_instance.setdefault('VPC', 'None')

    top_list.append(top_instance)
    

sorted_list = sorted(top_list, key=itemgetter('Name'))

if args.sort_key:
    sorted_list = sorted(sorted_list, key=itemgetter(args.sort_key))

for i in range(len(sorted_list)):
    print(sorted_list[i]['Id'].ljust(20) + sorted_list[i]['Status'].ljust(11) + sorted_list[i]['Type'].ljust(10)\
     + sorted_list[i]['pubIP'].ljust(16) + sorted_list[i]['privIP'].ljust(16) + sorted_list[i]['VPC'].ljust(15) + sorted_list[i]['Name'] )

