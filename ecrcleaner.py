#!/usr/bin/python3

import boto3, argparse, datetime, yaml, sys

parser = argparse.ArgumentParser(description='AWS Amazon EC2 Container Registry cleaner')
parser.add_argument('-l', '--list', action="store_true", dest="list_repo", default=False, help='Show repository info')
parser.add_argument('-d', '--delete', action="store", dest="days_ago", type=int, help='Delete images that are older then "days_ago" integer')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='AWS region name. Using "default" for your profile if not set')
parser.add_argument('repository_name',  action="store", help='ECR repository name')
args = parser.parse_args()

if args.days_ago:
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
    if len(todelete) == 0:
        sys.exit(0)
    print('[Yes/No] ?')
    gg = input()

    if gg.lower() in ('yes', 'y'):
        chunks = [todelete[x:x+100] for x in range(0, len(todelete), 100)]
        for part in chunks:
            response = client.batch_delete_image(repositoryName=args.repository_name, imageIds=part)
            print('Deleted: ' + str(len(response['imageIds'])) + ' Failures: ' + str(len(response['failures'])) )
        sys.exit(0)

    else:
        sys.exit(0)


if args.list_repo:
    amount = len(client.describe_images(repositoryName=args.repository_name, maxResults=1000)['imageDetails'])
    uri = client.describe_repositories(repositoryNames=[args.repository_name])['repositories'][0]['repositoryUri']
    print(uri)
    print(str(amount) + ' / 1000 images')

print(parser.parse_args(['-h']))
