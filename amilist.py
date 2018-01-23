#!/usr/bin/python3

#
#       Pretty listing of your account Amazon Machine Images (--executable-users self)
# App requires aws-cli installed on your machine. Default output is YAML compatible which can be easily redirected to some config file.
# You can change output to pprinted dictionary. Use --help for details.
#   

import yaml, subprocess, pprint, argparse


parser = argparse.ArgumentParser(description='Listing of your account Amazon Machine Images')
parser.add_argument('-p', '--profile', action="store", dest="aws_profile", default="default", help='.aws/config profile name. Using "default" if not set')
parser.add_argument('-o', '--output', action="store", dest="output_type", help='By default app output is YAML compatible multiline string. Use "--output dict" to get key:value dictionary output')
args = parser.parse_args()


aws_cli_output = subprocess.check_output("aws ec2 describe-images --executable-users self --profile %s" % (args.aws_profile), shell=True)
amidict = yaml.load(aws_cli_output)
amilist = amidict['Images']


if args.output_type == 'dict':
    output = {}
    for i in range(len(amilist)):
        output.setdefault(amilist[i].get('ImageId'), amilist[i].get('Name'))
    pprint.pprint(output)
else:
    for i in range(len(amilist)):
        print(amilist[i].get('ImageId') + ': ' + amilist[i].get('Name'))
