'''
Challenge Catuxa Seoane Botana - Magine Pro interview
12/04/2023


Bonus Assignment 1:
Extend the Python script to process a folder of video files instead of a single video file.
The script should iterate through all files in the folder and process and upload each file
to the specified S3 bucket

'''

import os
from os import path
import argparse
import moviepy.editor as moviepy

import boto3
from botocore.exceptions import ClientError


# Arguments
parser = argparse.ArgumentParser(description='Magine Pro challenge')

parser.add_argument("-i", "--input",
                    required=False,
                    type=str,
                    help='INPUT file path')

parser.add_argument("-o", "--output",
                    required=False,
                    type=str,
                    help='OUTPUT file path')

parser.add_argument("-b", "--bucket",
                    required=False,
                    type=str,
                    help='S3 bucket')

parser.add_argument("-ok", "--objectkey",
                    required=False,
                    type=str,
                    help='S3 Object key')


args = parser.parse_args()

#INPUT FILE PATH
in_file_path = args.input
# Check if input file path is correct
while path.exists(in_file_path) == False:
    print("The directory "+str(in_file_path)+' is incorrect. Please check the directory path and try again.: ')
    in_file_path = input()

#OUTPUT FILE PATH
out_file_path = args.output
while path.exists(out_file_path) == False:
    print("The directory "+str(out_file_path)+' is incorrect. Please check the directory path and try again.: ')
    in_file_path = input()
#S3 bucket
s3_bucket = args.bucket
#S3 object key
s3_object_key = args.objectkey





def video_format(in_file_path, out_file_path):
    """Change the format of the video and resized it

    :param in_file_path: Input file name
    :param out_file_path: Output file name
    :return: Clip ready to upload
    """
    count=0
    print('Changing format and resizing...')
    for file in os.scandir(in_file_path):
        count=count+1
        filename=os.fsdecode(file)
        
        print('Processing the file'+str(filename))
        
        clip=moviepy.VideoFileClip(filename)
        #resizing
        clip.resize((300,300))
        print((str(out_file_path)+'/'+str(filename)+".mov"))
        clip.write_videofile(str(out_file_path)+'/'+'newvideo'+str(count)+".mov",codec='libx264')
    


def upload_file(out_file_path, s3_bucket, s3_object_key=None):
    """Upload a file to an S3 bucket

    :param out_file_path: File to upload
    :param s3_bucket: Bucket to upload to
    :param s3_object_key: S3 object name. If not specified then clip name is used
    :return: True if file was uploaded, else False
    """
        #Ask for credentials
    print("Please write your AWS ACCESS KEY ID: ")
    aws_access_key_id = input()
    print("Please write your AWS SECRET ACCESS KEY: ")
    aws_secret_access_key=input()


    count=0
    for file in os.scandir(out_file_path):
        count=count+1
        print(count)
        filename=os.fsdecode(file)
        print('Uploading the file'+str(filename))
        # If S3 object_name was not specified, use file_name
        if s3_object_key is None:
            s3_object_key = os.path.basename(filename)
    
        # Upload the file
        s3_client = boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        try:
            response = s3_client.upload_file(filename, s3_bucket, s3_object_key+"_"+str(count)+".mov")
        except ClientError as e:
            print('Client error : ')
            print(e)
            logging.error(e)
            
        print('The video has been uploaded to the platform successfully!')
        


#Calling the functions

video_format(in_file_path, out_file_path)
upload_file(out_file_path, s3_bucket, s3_object_key)