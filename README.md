# aws-tools

Shell utilities for AWS operations written on Python.


----------


ec2runner.py - starting/stopping instances.

Example:

    newuser@vbox:~$ ec2runner stop -p default -r us-east-1 i-007f29708864cc40b
    Response code: 200
    Instance:i-007f29708864cc40b stopped => stopped


----------


amilist.py - AMI listing

Example:

    newuser@vbox:~$ amilist.py|head -10|sort -k2
    ami-00e60416: Centos-6 2017-01-13 12-10-07
    ami-040ddc7e: devops-infra-amazonlinux-1.22.0-SNAPSHOT-hvm-20171017094118032
    ami-02af3c78: devops-infra-amazonlinux-1.22.0-SNAPSHOT-hvm-20171127115712474
    ami-0192c27b: devops-infra-amazonlinux-1.22.0-SNAPSHOT-hvm-20180105113209206
    ami-0403107f: devops-infra-centos-1.0.0-SNAPSHOT-hvm-20170906110115204
    ami-0216bb78: devops-infra-cis-centos-1.0.0-SNAPSHOT-hvm-20171030085909632
    ami-034c7e14: devops-infra-sles-11.4.9-hvm
    ami-08ae9460: emr 3.7.0-ami-roller-20 paravirtual is


----------


ec2top.py - listing of your EC2 machines

    newuser@vbox:~$ ec2top --sort Type
    i-9262c07c          stopped    c3.large  54.84.57.91     10.155.4.105    vpc-8e9861e2   db2012-compute-01
    i-0f4e12fe047c8968b running    c3.large  54.165.160.131  10.155.4.98     vpc-8e9861e2   dev-auto-s3-compute101
    i-0b545c4b945aa6183 running    c3.large  54.236.202.212  10.155.2.199    vpc-8e9861e2   dev-compute-01
    i-0ce03d96ac577bba0 running    c3.large  34.192.41.156   10.155.2.241    vpc-8e9861e2   dev-compute-01-phx
    i-0401332de32993d1e running    c3.large  54.172.49.236   10.155.4.238    vpc-8e9861e2   dev-compute-02
    i-c8d6b639          stopped    c3.large  54.88.208.204   10.155.4.4      vpc-8e9861e2   dev-compute-03

