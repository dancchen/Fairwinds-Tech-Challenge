import boto3
import os
import subprocess


"""
    ec2 = boto3.resource('ec2')

    # create a file to store the key locally
    outfile = open('ec2-keypair.pem','w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)
    outfile.close()

    os.chmod("ec2-keypair.pem", 0o400)
"""

arg = ['sudo', 'apt-get', 'install', '-y', 'ansible',]
subprocess.Popen(arg, 
		stdin=subprocess.PIPE,
		).wait(timeout=60)
#proc = subprocess.Popen('apt-get install -y ansible', shell=True, executable="/bin/bash")
#proc.wait()
#proc.stdin.write('a\n')
#proc.stdin.flush()

#stdout, stderr = proc.communicate()
#print(stdout)
#print(stderr)
