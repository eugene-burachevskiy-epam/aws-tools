#!/usr/bin/python3

#
# Usage:
#   ./ec2_to_confluence.py [PROFILE] [REGION]
#
# where [PROFILE] and [REGION] are your ~/.aws/credentials information. 
# Script requires ec2top.py in the same directory and atlassian-cli.
#
# Please update confl dictionary with your proper Confluence details.
# 'pass' is base64 encoded password.
# 'pagetitle' is generating dynamically
#

import subprocess, datetime, sys, base64, pytz

confl = {
    'url':'URLSTRING',
    'user':'USERSTRING',
    'pass':'PASSTRING',
    'space':'OPS',
    'parent':'Assets Inventory',
    'pagetitle':'',
    'cli-path':'./atlassian-cli-3.1.0/lib/confluence-cli-3.1.0.jar'
}

if len(sys.argv) == 1:
    #for testing purposes
    aws_profile = 'fed'
    aws_region = 'us-gov-west-1'
else:
    aws_profile = sys.argv[1]
    aws_region = sys.argv[2]

fmt = '%Y-%m-%d %H:%M:%S'
curdate = datetime.datetime.now(pytz.timezone("America/Los_Angeles")).strftime(fmt)

print('Pulling EC2 data...')
out = subprocess.check_output(['./ec2top.py', '-p', aws_profile, '-r', aws_region, '-s', 'VPC'])
out = out.decode("utf-8")
outlist = out.split('\n')
outlist = list(filter(None, outlist))

file = open('page.xml', 'w')
file.write("<i>Status updated: %s </i>\n\n<h2>EC2 inventory</h2>\n<table>\n<tr>\n<th>ID</th><th>Status</th><th>Type</th><th>Public IP</th><th>Private IP</th><th>VPC</th><th>VPC name</th><th>Name</th></tr>"\
 % (curdate))
file.close()

for rownum in range(len(outlist)):
    outitem = outlist[rownum].split()
    outitem[0], outitem[-1] =  outitem[-1], outitem[0]
    outitem.insert(0, '<tr>')
    for i in range(1, len(outitem)):
        if i == 4 and not outitem[i].startswith('None'):
            outitem[i] = '<b>' + outitem[i] + '</b>'
        outitem[i] = '<td>' + outitem[i] + '</td>'
    outitem.append('</tr>')
    file = open('page.xml', 'a')
    file.write(' '.join(outitem))
    file.write('\n')
    file.close()
    
file = open('page.xml', 'a')
file.write('\n</table>\n\n')
file.write('<h2>RDS inventory</h2>\n<table>\n<tr>\n<th>DBName</th><th>DBInstanceIdentifier</th><th>DBInstanceClass</th><th>Status</th><th>Engine</th><th>EngineVersion</th><th>AvailabilityZone</th><th>VPC ID</th><th>VPC Name</th></tr>')
file.close()

print('Pulling RDS data...')
out = subprocess.check_output(['./ec2top.py', '-p', aws_profile, '-r', aws_region, '--rds'])
out = out.decode("utf-8")
outlist = out.split('\n')
for rownum in range(len(outlist)):
    outitem = outlist[rownum].split()
    outitem.insert(0, '<tr>')
    for i in range(1, len(outitem)):
        outitem[i] = '<td>' + outitem[i] + '</td>'
    outitem.append('</tr>')
    file = open('page.xml', 'a')
    file.write(' '.join(outitem))
    file.write('\n')
    file.close()

file = open('page.xml', 'a')
file.write('\n</table>\n\n')
file.write('<h2>Elasticache inventory</h2>\n<table>\n<tr>\n<th>CacheClusterId</th><th>Node Type</th><th>Cluster Status</th><th>Engine</th><th>Engine Version</th><th>Num Nodes</th><th>Preffered AZ</th></tr>')
file.close()

print('Pulling Elasticache data...')
out = subprocess.check_output(['./ec2top.py', '-p', aws_profile, '-r', aws_region, '--ech'])
out = out.decode("utf-8")
outlist = out.split('\n')
for rownum in range(len(outlist)):
    outitem = outlist[rownum].split()
    outitem.insert(0, '<tr>')
    for i in range(1, len(outitem)):
        outitem[i] = '<td>' + outitem[i] + '</td>'
    outitem.append('</tr>')
    file = open('page.xml', 'a')
    file.write(' '.join(outitem))
    file.write('\n')
    file.close()

file = open('page.xml', 'a')
file.write('\n</table>\n\n')
file.close()
print('page.xml written with %s data.' % (aws_profile.upper()))


print('\nUpdating Confluence page...')
confl['pass'] = base64.b64decode(bytes(confl['pass'], 'UTF-8'), altchars=None).decode("utf-8")
confl['pagetitle'] = 'AWS resources list - %s, %s' % (aws_profile.upper(), aws_region)

p = subprocess.check_output('java -jar %(cli-path)s --server %(url)s --user "%(user)s" --password "%(pass)s" --action storePage --space "%(space)s" --parent "%(parent)s" --title "%(pagetitle)s" --file page.xml --noConvert' % confl, shell=True)
print(p.decode("utf-8"))
