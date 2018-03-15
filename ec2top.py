#!/usr/bin/python3

#
#     Listing of your AWS EC2 instances, RDS, Elasticache
# App require boto3 AWS-API module, make sure it is installed by running 'sudo pip3 install boto3'
# If no args specified app lists your EC2 instances using .aws/config "Default" profile and region. Use ./ec2top.py --help for possible options
#

import boto3, argparse
from operator import itemgetter

parser = argparse.ArgumentParser(description='AWS EC2 instances listing.')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using "default" for your profile if not set')
parser.add_argument('-s', '--sort', action="store", dest="sort_key", help='Sort your output by column name. Default sorting is "Name". Other options are Status|Type|VPC|pubIP|privIP ')
group = parser.add_mutually_exclusive_group()
group.add_argument('--rds', action="store_true", default=False, help='RDS data')
group.add_argument('--ech', action="store_true", default=False, help='Elastic cache data')
group.add_argument('--ec2', action="store_true", default=True, help='EC2 data (Default).')
args = parser.parse_args()

if args.ech or args.rds:
    args.ec2 = False
#print(args)


if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()

#list of Tags dictionaries as input
def instance_name(tags):
    for i in tags:
        if i['Key'] == 'Name':
            return i['Value'].replace(' ', '_')

#VPC ID string as input
def vpc_name(id):
    if args.aws_profile:
        session = boto3.Session(profile_name=args.aws_profile)
    else:
        session = boto3.Session()
    if args.aws_region:
        ec2 = session.client('ec2', region_name=args.aws_region)
    else:
        ec2 = session.client('ec2')
    vpcdata = ec2.describe_vpcs()
    for vpci in vpcdata['Vpcs']:
        if vpci['VpcId'] == id:
            vpcname = instance_name(vpci['Tags']).replace(' ', '_')
    return vpcname


if args.ec2:
    if args.aws_region:
        ec2 = session.client('ec2', region_name=args.aws_region)
    else:
        ec2 = session.client('ec2')
    response = ec2.describe_instances()

    top_list = []

    for i in range(len(response['Reservations'])):
        for r in range(len(response['Reservations'][i]['Instances'])):
            instance = response['Reservations'][i]['Instances'][r]
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
                vpcname = vpc_name(instance['VpcId'])
                top_instance.setdefault('VPCname', vpcname)
            else:
                top_instance.setdefault('VPC', 'None')
                top_instance.setdefault('VPCname', 'None')
            
            if top_instance['Name'] is None:
                top_instance['Name'] = 'None'
            top_list.append(top_instance)

    sorted_list = sorted(top_list, key=itemgetter('Name'))

    if args.sort_key:
        sorted_list = sorted(sorted_list, key=itemgetter(args.sort_key))

    for i in range(len(sorted_list)):
        print(sorted_list[i]['Id'].ljust(20) + sorted_list[i]['Status'].ljust(11) + sorted_list[i]['Type'].ljust(12)\
        + sorted_list[i]['pubIP'].ljust(16) + sorted_list[i]['privIP'].ljust(16) + sorted_list[i]['VPC'].ljust(13) + sorted_list[i]['VPCname'][:16].ljust(17) + sorted_list[i]['Name'] )


if args.rds:
    if args.aws_region:
        rds = session.client('rds', region_name=args.aws_region)
    else:
        rds = session.client('rds')
    response = rds.describe_db_instances()

    top_list = []

    for i in response['DBInstances']:
        top_instance = {}
        top_instance.setdefault('DBInstanceIdentifier', i['DBInstanceIdentifier'])
        top_instance.setdefault('DBInstanceClass', i['DBInstanceClass'])
        top_instance.setdefault('DBInstanceStatus', i['DBInstanceStatus'])
        top_instance.setdefault('DBName', i['DBName'])
        top_instance.setdefault('AvailabilityZone', i['AvailabilityZone'])
        top_instance.setdefault('Engine', i['Engine'])
        top_instance.setdefault('EngineVersion', i['EngineVersion'])
        top_instance.setdefault('VpcId', i['DBSubnetGroup']['VpcId'])
        vpcname = vpc_name(i['DBSubnetGroup']['VpcId'])
        top_instance.setdefault('VPCname', vpcname)

        top_list.append(top_instance)

    sorted_list = sorted(top_list, key=itemgetter('DBName'))

    for i in sorted_list:
        print(i['DBName'].ljust(20) + i['DBInstanceIdentifier'][:18].ljust(20) + i['DBInstanceClass'].ljust(16) \
        + i['DBInstanceStatus'].ljust(12) + i['Engine'].ljust(12) + i['EngineVersion'].ljust(12) \
        + i['AvailabilityZone'].ljust(16) + i['VpcId'].ljust(16) + i['VPCname'][:15].ljust(16))

if args.ech:
    if args.aws_region:
        ech = session.client('elasticache', region_name=args.aws_region)
    else:
        ech = session.client('elasticache')
    response = ech.describe_cache_clusters()

    top_list = []

    for i in response['CacheClusters']:
        top_instance = {}
        top_instance.setdefault('CacheClusterId', i['CacheClusterId'])
        top_instance.setdefault('CacheNodeType', i['CacheNodeType'])
        top_instance.setdefault('CacheClusterStatus', i['CacheClusterStatus'])
        top_instance.setdefault('Engine', i['Engine'])
        top_instance.setdefault('EngineVersion', i['EngineVersion'])
        top_instance.setdefault('NumCacheNodes', i['NumCacheNodes'])
        top_instance.setdefault('PreferredAvailabilityZone', i['PreferredAvailabilityZone'])

        top_list.append(top_instance)
    
    sorted_list = sorted(top_list, key=itemgetter('CacheClusterId'))

    for i in sorted_list:
        print(i['CacheClusterId'].ljust(32) + i['CacheNodeType'].ljust(20) + i['CacheClusterStatus'].ljust(12) \
        + i['Engine'].ljust(12) + i['EngineVersion'].ljust(12) + str(i['NumCacheNodes']).ljust(5) + i['PreferredAvailabilityZone'].ljust(16))

