'''
Challenge Catuxa Seoane Botana - Magine Pro interview
12/04/2023


Build a simple Python script that processes a video file and uploads it to an S3 bucket.

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
while path.isfile(in_file_path) == False:
    print("I did not find the file at "+str(in_file_path)+'. Please check the directory path and try again.: ')
    in_file_path = input()

#OUTPUT FILE PATH
out_file_path = args.output

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
    print('Changing format and resizing...')
    clip=moviepy.VideoFileClip(in_file_path)
    #resizing
    clip.resize((300,300))
    clip.write_videofile(out_file_path,codec='libx264')
    


def upload_file(out_file_path, s3_bucket, s3_object_key=None):
    """Upload a file to an S3 bucket

    :param out_file_path: File to upload
    :param s3_bucket: Bucket to upload to
    :param s3_object_key: S3 object name. If not specified then clip name is used
    :return: True if file was uploaded, else False
    """
    

    # If S3 object_name was not specified, use file_name
    if s3_object_key is None:
        s3_object_key = os.path.basename(out_file_path)
    
    
    #Ask for credentials
    print("Please write your AWS ACCESS KEY ID: ")
    aws_access_key_id = input()
    print("Please write your AWS SECRET ACCESS KEY: ")
    aws_secret_access_key=input()
    
    aws_access_key_id='AKIAZTTGMAALBZLWR3US'
    aws_secret_access_key='+G6hY+B2jAAAcHAf3gvggLww6OUvM6n1X/8MlI/c'

    # Upload the file
    s3_client = boto3.client('s3',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        response = s3_client.upload_file(out_file_path, s3_bucket, s3_object_key)
    except ClientError as e:
        print('Client error : ')
        print(e)
        logging.error(e)
        return False
    print('The video has been uploaded to the platform successfully!')
    return True


#Calling the functions

video_format(in_file_path, out_file_path)
while path.isfile(out_file_path) == False:
    print("The video could not be saved to the directory "+str(out_file_path)+'.Check the parameters and run again. ')
    break

upload_file(out_file_path, s3_bucket, s3_object_key)