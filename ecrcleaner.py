#!/usr/bin/python3

import boto3, argparse, datetime, yaml, sys
from operator import itemgetter

parser = argparse.ArgumentParser(description='AWS Amazon EC2 Container Registry cleaner')

group = parser.add_mutually_exclusive_group()
group.add_argument('-l', '--list', action="store_true", dest="list_repo", default=False, help='Show repository info')
group.add_argument('--list-all', action="store_true", dest="list_allrepo", default=False, help='Show all repositories stats')
group.add_argument('-d', '--delete', action="store", dest="days_ago", type=int, help='Delete images that are older then "DAYS_AGO"')

parser.add_argument('--only', action="store", dest="del_tag", help='Delete only with such tag. Use with -d')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", help='.aws/credentials profile name. Using "default" if not set')
parser.add_argument('-r', '--region', action="store", dest="aws_region", help='AWS region name. Using "default" for your profile if not set')
parser.add_argument('repository_name',  action="store", nargs='?', help='ECR repository name')
args = parser.parse_args()

fmt = '%Y-%m-%d %H:%M:%S'

if args.aws_profile:
    session = boto3.Session(profile_name=args.aws_profile)
else:
    session = boto3.Session()
client = session.client('ecr', region_name=args.aws_region)


if args.days_ago:
    delta = datetime.timedelta(days=args.days_ago)
    until_datetime = datetime.datetime.now() - delta

    images = client.describe_images(repositoryName=args.repository_name, maxResults=1000)['imageDetails']
    todelete = []

    for i in images:
        if until_datetime > i['imagePushedAt'].replace(tzinfo=None):
            if args.del_tag:
                for tag in i['imageTags']:
                    if args.del_tag in tag:
                        todelete.append( {'imageDigest':i['imageDigest']} )
            else:
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
    images = client.describe_images(repositoryName=args.repository_name, maxResults=1000)['imageDetails']
    amount = len(images)
    uri = client.describe_repositories(repositoryNames=[args.repository_name])['repositories'][0]['repositoryUri']
    last10 = sorted(images, key=itemgetter('imagePushedAt'), reverse=True)[0:9]
    print(uri + '\n')
    print(str(amount) + ' / 1000 images \n')
    print('Last pushed images:')
    for i in last10:
        print(i['imagePushedAt'].replace(tzinfo=None).strftime(fmt).ljust(20) + str(i['imageTags']))
    sys.exit(0)

if args.list_allrepo:
    allrepos = sorted(client.describe_repositories(maxResults=1000)['repositories'], key=itemgetter('repositoryName') )
    for i in allrepos:
        amount = len(client.describe_images(repositoryName=i['repositoryName'], maxResults=1000)['imageDetails'])
        print(str (str(amount) + ' / 1000 ').ljust(14) + i['repositoryName'])
    sys.exit(0)

print(parser.parse_args(['-h']))
