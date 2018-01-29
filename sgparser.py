#!/usr/bin/python3

#
#       AWS Security groups rules parser.
# App uses aws-cli "describe-security-groups" request or JSON file as an input and gives CSV-compatible output for each rule.
# Output format is 'GroupId', 'GroupName', 'Description', 'CidrIp', 'IpProtocol', 'FromPort', 'ToPort'
#
# Use "sgparser.py --help" for options.
#

import subprocess, yaml, copy, argparse
from argparse import RawDescriptionHelpFormatter

parser = argparse.ArgumentParser(description="AWS Security groups rules parser. App uses aws-cli or JSON file as an input and gives CSV-compatible output for each rule.\nOutput format is 'GroupId', 'GroupName', 'Description', 'CidrIp', 'IpProtocol', 'FromPort', 'ToPort'", formatter_class=RawDescriptionHelpFormatter)
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", default="default", help='AWS credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using default for your profile if not set')
parser.add_argument('--file', action="store", dest="filename", help='By default app uses aws-cli request for your profile/region to parse Security groups JSON input. Use "--file FILENAME" argument to parse input from local file')
args = parser.parse_args()


if args.filename:
    fileobj = open(args.filename, 'r')
    file = fileobj.read()
    fileobj.close()
else:
    if args.aws_region:
        file = subprocess.check_output("aws ec2 describe-security-groups --profile %s --region %s" % (args.aws_profile, args.aws_region), shell=True)
    else:
        file = subprocess.check_output("aws ec2 describe-security-groups --profile %s" % (args.aws_profile), shell=True)

try:
    input = yaml.load(file)
except yaml.YAMLError as e:
    print(e)
    exit(1)

for i in range(len(input['SecurityGroups'])):
    item = []
    item.append(input['SecurityGroups'][i]['GroupId'])
    item.append(input['SecurityGroups'][i]['GroupName'])
    item.append(input['SecurityGroups'][i]['Description'].replace(',', ' and '))
    for f in input['SecurityGroups'][i]['IpPermissions']:
        if len(f['UserIdGroupPairs']) == 0:
            for r in f['IpRanges']:
                rule = copy.copy(item)
                rule.append(r['CidrIp'])
                rule.append(f['IpProtocol'])
                if 'FromPort' in f.keys():
                    rule.append(str(f['FromPort']))
                else:
                    rule.append('no_fromport')
                if 'ToPort' in f.keys():
                    rule.append(str(f['ToPort']))
                else:
                    rule.append('no_toport')
                formatted_rule = ', '.join(rule)
                print(formatted_rule)
        else:
            for r in f['UserIdGroupPairs']:
                rule = copy.copy(item)
                rule.append(r['GroupId'])
                rule.append(f['IpProtocol'])
                if 'FromPort' in f.keys():
                    rule.append(str(f['FromPort']))
                else:
                    rule.append('no_fromport')
                if 'ToPort' in f.keys():
                    rule.append(str(f['ToPort']))
                else:
                    rule.append('no_toport')
                formatted_rule = ', '.join(rule)
                print(formatted_rule)
