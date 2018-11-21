#!/usr/bin/python3

import boto3, argparse, datetime

parser = argparse.ArgumentParser(description='AWS Amazon EC2 Container Registry cleaner')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using "default" for your profile if not set')
parser.add_argument('-d', '--delete', action="store", dest="days_ago", type=int, help='Delete images that are older then "days_ago')
parser.add_argument('repository_name',  action="store", help='ECR repository name')


delta = datetime.timedelta(days=args.days_ago)
until_datetime = datetime.datetime.now() - delta


if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()
ecr = session.client('ecr', region_name=args.aws_region)

images = client.describe_images(repositoryName=args.repository_name, maxResults=1000)['imageDetails']
todelete = []

for i in images:
    if untildate > i['imagePushedAt'].replace(tzinfo=None):
        todelete.append(i['imageDigest'])

print(str(len(todelete)) + ' images will be deleted.')