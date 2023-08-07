
import aws_details
import boto3
from boto3 import resource
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import numpy as np
import json
import requests
import logging
import os


resources = boto3.resource(
   'dynamodb',
   aws_access_key_id     = aws_details.AWS_ACCESS_KEY_ID,
   aws_secret_access_key = aws_details.AWS_SECRET_ACCESS_KEY,
   region_name           = aws_details.REGION_NAME,
   aws_session_token=aws_details.SESSION_ID
)
s3_client = boto3.client(
   's3',
   aws_access_key_id     = aws_details.AWS_ACCESS_KEY_ID,
   aws_secret_access_key = aws_details.AWS_SECRET_ACCESS_KEY,
   region_name           = aws_details.REGION_NAME,
   aws_session_token=aws_details.SESSION_ID
)


def create_table_music():   
   table = resources.create_table(
       TableName = 'music', 
       KeySchema = [
           {
               'AttributeName': 'title',
               'KeyType'      : 'HASH'
           },
           {
               'AttributeName': 'artist',
               'KeyType'      : 'RANGE'
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'title', 
               'AttributeType': 'S'   
           },
           {
               'AttributeName': 'artist', 
               'AttributeType': 'S'   
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 30,
           'WriteCapacityUnits': 30
       }
   )
   return table
def add_details_music():
    
    
    
    Table = resources.Table('music')
    with open ("a1.json") as pic_file:
        data=json.load(pic_file)
        inner_list=data['songs']
        for item in inner_list:
            
            response = Table.put_item(
            Item={
            'title':item ['title'],
            'artist':item ['artist'],
            'img_url':item ['img_url'],
            'web_url':item ['web_url'],
            'year':item ['year'],
            }   )
        return response

def create_table_subscription():   
   table = resources.create_table(
       TableName = 'Subscribtion', 
       KeySchema = [
           {
               'AttributeName': 'email',
               'KeyType'      : 'HASH'
           },
           {
               'AttributeName': 'username',
               'KeyType'      : 'RANGE'
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'email', 
               'AttributeType': 'S'   
           },
           {
               'AttributeName': 'username', 
               'AttributeType': 'S'   
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table
def create_bucket():
   
    try:
            
            
            
            s3_client.create_bucket(Bucket='s3894695-ass1'
            )
            
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_img():
    with open ("a1.json") as pic_file:
        data=json.load(pic_file)
        inner_list=data['songs']
        for item in inner_list:
            img_data = requests.get(item['img_url'])
            print(img_data)
            
            with open(item['artist']+".jpg", "wb") as file:
                file.write(img_data.content)
                
                
def upload_img():
    
    with open ("a1.json") as pic_file:
        data=json.load(pic_file)
        inner_list=data['songs']
        for item in inner_list:
    
            with open("C:/RMIT/Sem_3/Cloud_Computing/Assignment_1/flask_demo/flask_demo/"+item['artist']+".jpg", 'rb') as f:
                s3_client.upload_fileobj(f, 's3894695-ass1', item['artist']+".jpg")
        
        
if __name__ == '__main__':
  # create_table_subscription()
   #create_table_music()
   #create_bucket()
   #add_details_music()
   #get_img()
   upload_img()
   