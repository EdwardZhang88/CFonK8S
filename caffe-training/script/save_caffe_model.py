import os
import boto
import boto.s3.connection
import glob
from boto.s3.key import Key

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
    k = Key(myBucket)
    print("Succeeded to access bucket "+bucketName+".\n")     

    # As a rule, trained models are supposed to be under s3://{bucket}/models on Ceph OSS
    for file in glob.glob("/workdir/model/*.caffemodel"):
        print("Found local model file : "+file+"\n")
        name = file.split('/')[-1]
        k.key = jobID+"/model/"+name
        k.set_contents_from_filename(file)
        print("Succeeded to upload model "+name+".\n")
                            
    # As a rule, training logs are supposed to be under s3://{bucket}/logs on Ceph OSS
    for file in glob.glob("/workdir/log/*.log"):
        print("Found local log file : "+file+"\n")
        name = file.split('/')[-1]
        k.key = jobID+"/log/"+name
        k.set_contents_from_filename(file)
        print("Succeeded to upload log "+name+".\n")
                            
except Exception as e:      
        print("Failed to upload model or log.\n" + e.message)
        raise e 
