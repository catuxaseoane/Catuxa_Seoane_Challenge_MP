# Interview challenge - Catuxa Seoane

This repository shows the challenge carried out by Catuxa Seoane for the company MaginePro. The challenge consists of two python scripts containing the main assignment and one of the bonus assignments.

# -----------------------------------------------------------------------------

## Basic assignment

The python script for this part is----. To execute the corresponding code you have to write the following in the console:
```
python challenge_Catuxa.py -i input_file_path -o output_file_path -b s3_bucket_name -ok s3_object_key
```
An example can be:
```
python challenge_Catuxa.py -i ./User/video.mp4 -o ./output/newvideo.mov -b bucketmagine -ok videomagine
```
The script then executes a function called ```video_format``` which processes the corresponding video. This video is resized (300x300 size, for example) and format changed (according to the parameters indicated in the output file path). 

A function called ```upload_file``` is then executed which will prompt you to enter your AWS credentials via console, read the modified video and upload it to the specified S3 bucket with the specified name.

# -----------------------------------------------------------------------------

## Bonus assignment 1
