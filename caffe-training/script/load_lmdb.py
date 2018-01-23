import time
import os
import boto
import boto.s3.connection
from boto.s3.key import Key
from boto.s3.bucketlistresultset import *

aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
host = os.environ.get("S3_ENDPOINT")
port = os.environ.get("PORT")
bucketName = os.environ.get("BUCKET_NAME")
jobID = os.environ.get("UID")

#aws_access_key_id = 'ewogICAgIlJHV19UT0tFTiI6IHsKICAgICAgICAidmVyc2lvbiI6IDEsCiAgICAgICAgInR5cGUiOiAibGRhcCIsCiAgICAgICAgImlkIjogImhhZG9vcCIsCiAgICAgICAgImtleSI6ICJoYWRvb3AiCiAgICB9Cn0K'
#aws_secret_access_key = ''
#host = '10.1.86.14'
#port = 8080
#bucketName = 'junzhang22'
#jobID = 'MNIST'

# As a rule, training/validation data/labels are supposed to be under /workdir/data in started container
os.chdir("/workdir/data")

try:
    # Get S3 connection to Ceph OSS
    connection = boto.connect_s3(
        aws_access_key_id= aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        host=host, 
        port=int(port),
        is_secure=False, 
        calling_format=boto.s3.connection.OrdinaryCallingFormat()
       )
    # Access to the specified bucket
    myBucket = connection.get_bucket(bucketName)
    #k = Key(myBucket)
    print("Succeeded to access bucket "+bucketName+".\n")    

    # As a rule, training/validation data/labels are supposed to be under s3://{bucket}/data on Ceph OSS
    # Also, trainign data/lables are supposed to be under train directoy and test under test directoy.
    for key in bucket_lister(myBucket, prefix=jobID+"/data/"):
        file = key.name.split('/')[-1]
        path = '/'.join(key.name.split('/')[2:-1])
        
        # Create sub folder if any on Ceph OSS and not existed locally
        if path != '' and not os.path.exists(path):
            os.makedirs(path)

        key.get_contents_to_filename(path+'/'+file)
        print("Succeeded to download data "+path+'/'+file+".\n")
                            
except Exception as e:      
        print("Failed to download data.\n" + e.message)
        raise e  
