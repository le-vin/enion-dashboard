import boto3
import pandas as pd
import json

f = open("./credentials.json")
credentials = json.load(f)
access_key  = credentials["aws_access_key_id"]
secret_access_key = credentials["aws_secret_access_key"]

#Creating Session With Boto3.
session = boto3.Session(
aws_access_key_id= access_key, 
aws_secret_access_key= secret_access_key
)

# Download previous final_list.csv file from S3
s3_client = boto3.client('s3', 
                    aws_access_key_id= access_key,
                    aws_secret_access_key= secret_access_key,
                    region_name='eu-west-3'
                    )

obj = s3_client.get_object(Bucket= 'capstoneenion', Key= 'test.csv') 
df = pd.read_csv(obj['Body'])
json_file = df.to_json(orient="split")

print(json_file)