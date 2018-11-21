#!/usr/bin/python3

import boto3, argparse, datetime, sys

parser = argparse.ArgumentParser(description='AWS Amazon EC2 Container Registry cleaner')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='EC2 region name. Using "default" for your profile if not set')
parser.add_argument('-d', '--delete', action="store", dest="days_ago", type=int, help='Delete images that are older then "days_ago" integer')
parser.add_argument('repository_name',  action="store", help='ECR repository name')
args = parser.parse_args()

delta = datetime.timedelta(days=args.days_ago)
until_datetime = datetime.datetime.now() - delta


if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()
client = session.client('ecr', region_name=args.aws_region)

images = client.describe_images(repositoryName=args.repository_name, maxResults=1000)['imageDetails']
todelete = []

for i in images:
    if until_datetime > i['imagePushedAt'].replace(tzinfo=None):
        todelete.append( {'imageDigest':i['imageDigest']} )

print(str(len(todelete)) + ' images will be deleted.')
print('[Yes/No] ?')
gg = input()

if gg.lower() in ('yes', 'y'):
    response = client.batch_delete_image(repositoryName='string', imageIds=todelete)
    print('Deleted: ' + str( len(response['imageIds']) ) + ' images')
    print('Failures:' + str( len(response['failures']) ))
else:
    sys.exit(1)