import boto3
import os
import time
import subprocess
import paramiko



"""
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

#arg = ['sudo', 'apt-get', 'install', '-y', 'ansible',]
#subprocess.Popen(arg, 
#		stdin=subprocess.PIPE,
#		).wait(timeout=60)
#proc = subprocess.Popen('apt-get install -y ansible', shell=True, executable="/bin/bash")
#proc.wait()
#proc.stdin.write('a\n')
#proc.stdin.flush()

#stdout, stderr = proc.communicate()
#print(stdout)
#print(stderr)

ec2 = boto3.resource('ec2', region_name='us-east-1')

instances = ec2.create_instances(
     ImageId='ami-09e67e426f25ce0d7',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='ec2-keypair'
 )

#time.sleep(40)
#running_instances = ec2.instances.filter(Filters=[{
#    'Name': 'instance-state-name',
#    'Values': ['running']}])

#print(instances.public_ip_address)
#print(list(running_instances))
#print(list(running_instances))

#for instance in running_instances:
#    print(instance.public_hostname)

instance = instances[0]

instance.wait_until_running()

# Associate Security Group to the instance to allow access to instance VPC 
instance.modify_attribute(Groups=['sg-0c56f0fa147e09cc1'])

# Reload to get the DNS name after EC2 is up and running
instance.load()
hostname = instance.public_dns_name

key = paramiko.RSAKey.from_private_key_file('ec2-keypair.pem')

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect/ssh to an instance

try:

    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2

    client.connect(hostname=hostname, username="ubuntu", pkey=key)

    # Execute a command(cmd) after connecting/ssh to an instance

#    cmds = ["sudo snap install docker", 
#            #"sudo chmod 666 /var/run/docker.sock", 
#	    "sudo chown ${USER}:${USER} /var/run/docker.sock"
#	    "sudo docker run -d -p 8000:8000 danielcchen/django_ec2"]  

#    cmds = "sudo apt update;  sudo apt install apt-transport-https ca-certificates curl software-properties-common;  curl -fsSL https:\/\/download.docker.com\/linux/ubuntu/gpg \| sudo apt-key add -;  sudo add-apt-repository \"deb \[arch=amd64\] https:\/\/download.docker.com\/linux\/ubuntu focal stable\" ; sudo apt update;  apt-cache policy docker-ce;  sudo apt install -y docker-ce;  sudo docker run -d -p 8000:8000 danielcchen\/django_ec2"

#    cmds = "sudo apt update;  sudo apt install apt-transport-https ca-certificates curl software-properties-common;  curl -fsSL https:\/\/download.docker.com\/linux/ubuntu/gpg \| sudo apt-key add -;  sudo add-apt-repository \"deb \[arch=amd64\] https:\/\/download.docker.com\/linux\/ubuntu focal stable\" ; sudo apt update;  apt-cache policy docker-ce;  sudo apt install -y docker-ce;  sudo docker run -d -p 8000:8000 danielcchen\/django_ec2"

    cmds = ["sudo apt update",  
            "sudo apt install -y apt-transport-https ca-certificates curl software-properties-common",
            "curl -fsSL https:\/\/download.docker.com\/linux/ubuntu/gpg | sudo apt-key add -",  
            "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable\"",  
            "sudo apt update",  
            "apt-cache policy docker-ce",  
            "sudo apt install -y docker-ce", 
            "sudo docker run -d -p 8000:8000 danielcchen\/django_ec2"]

#    channel = client.get_transport().open_session()
#    channel.invoke_shell()  

#    while channel.recv_ready():
#       channel.recv(1024) 

    
    for cmd in cmds:
        print(cmd) 
        stdin,stdout,stderr=client.exec_command(cmd)
        outlines=stdout.readlines()
        result=''.join(outlines)
        print (result)        

#       print(cmd)
#       channel.sendall(cmd)
#       print(channel.recv(1024))

#    channel = client.invoke_shell()
#    stdin = channel.makefile('wb')
#    stdout = channel.makefile('rb') 

#    stdin.write('''
#    sudo apt update 
#    sudo apt install apt-transport-https ca-certificates curl software-properties-common 
#    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#    sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable\"  
#    sudo apt update && apt-cache policy docker-ce 
#    sudo apt install docker-ce 
#    sudo docker run -d -p 8000:8000 danielcchen\/django_ec2
#    ''')

    #stdin, stdout, stderr = client.exec_command(cmds)

    #print(stdout.read())

    # close the client connection once the job is done
    #stdout.close()
    #stdin.close()
    client.close()


except Exception as e:

    print(e)

print(hostname)
print("ssh -i ec2-keypair.pem ubuntu@{}".format(hostname))
print("Please use this address to access the website http://{}:8000".format(hostname))


