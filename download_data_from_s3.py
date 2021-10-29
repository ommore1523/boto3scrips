import os
import datetime
import boto3

begin_time = datetime.datetime.now()

BUCKET_NAME = 'xsfc-libraries'
TMPDIR = "/home/omkar/Desktop/aws_deployment/xsightalgo/demo/lib/"



if not os.path.exists(TMPDIR):
    os.makedirs(TMPDIR)


# initiate the s3 resource 
s3 = boto3.resource('s3')

# Access the bucket
my_bucket = s3.Bucket(BUCKET_NAME)

"""
 for all paths in s3 bucket :
    split path to two parts path=[folderpath,file_name]

    if len(dir) greater than 1:
        try:
            check if folderpath exists:
                if not exists:
                    create path
                download data = TMPDIR+ folderpath+"/"+filename
    else:
         download data = TMPDIR+filename
                
"""


for s3_object in my_bucket.objects.all():
    
    dir=(s3_object.key).rsplit("/",1)
    # print("s3_object.key",s3_object.key)

    try:
        if len(dir) > 1:
            print(dir)
            if  os.path.exists(TMPDIR+dir[0]):
                my_bucket.download_file(s3_object.key, TMPDIR+dir[0]+"/"+dir[1])
            else:
                os.makedirs(TMPDIR+dir[0])
            # print(os.listdir())
        else:
            my_bucket.download_file(s3_object.key, TMPDIR+dir[0])
    except Exception as e:
        raise e

print("EXECUTION-TIME: hour:minute:second:microsecond",datetime.datetime.now() - begin_time)


# Note in Aws side lambda cannot access the s3 directly .. create vpc endpoint to vpc and s3