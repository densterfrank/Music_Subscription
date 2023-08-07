
import aws_details
import boto3
from boto3 import resource
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import json
import requests

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

#To get data from login table
def get_details(email,password):
        url_get_details=' https://0i0mrly5l0.execute-api.us-east-1.amazonaws.com/dev/login'
        response_get_details=requests.post(url_get_details,json={"email"     : email,"password" :password })
    
        response_get_details=json.loads(response_get_details.text)
        response_get_details=json.loads(response_get_details['body'])
        
        
        return response_get_details
#To add data to login table
def add_details(email, password, user_name):
    url_add_details="https://hrchj0wrte.execute-api.us-east-1.amazonaws.com/dev/signup"
    requests.post(url_add_details,json={"email"     : email,"password" :password ,"user_name":user_name})
    
    
 #To scan all required information from sunscription table   
def scan_query(title,artist,year):
    url_scan="https://s83b0skukj.execute-api.us-east-1.amazonaws.com/dev/query"
    response_scan=requests.post(url_scan,json={"title":title,"artist":artist,"year":year})
    response_scan=json.loads(response_scan.text)
    response_scan=json.loads(response_scan['body'])
    return response_scan['Items']
#To check is mail already present in database for signup
def check_mail(email):
    url_check_mail="https://8rh40u8zqi.execute-api.us-east-1.amazonaws.com/dev/check_mail"
    response_check=requests.post(url_check_mail,json={"email":email})
    response_check=json.loads(response_check.text)
    response_check=response_check['body']
    return response_check


#To get image from s3
def get_img(artist):
    url_image="https://37vcs06tt9.execute-api.us-east-1.amazonaws.com/dev/image"
    response_image=requests.post(url_image,json={"artist":artist})
    response_image=json.loads(response_image.text)
    response_image=response_image['body']
    return response_image
    
    
#To get deatils from sucription table for particular email
def subscribtion_query(email,username):
    url_sub_query=" https://6zkhidyjbi.execute-api.us-east-1.amazonaws.com/dev/scan_subscib"
    response_sub_query=requests.post(url_sub_query,json={"email":email,"username":username})
    response_sub_query=json.loads(response_sub_query.text)
    response_sub_query=json.loads(response_sub_query['body'])
    return response_sub_query['Items'][0]['subscribed_songs']
#To check is songs is attached to email
def check_condition(email,username):
    url_check_condition="https://3jlw198xfg.execute-api.us-east-1.amazonaws.com/dev/check_condition"
    response_condition=requests.post(url_check_condition,json={"email":email,"username":username})
    response_condition=json.loads(response_condition.text)
    response_condition=response_condition['body']
    return response_condition
    


 #To add email and songs to subscription table   
def add_subcription(email,username,List):
    url_add="https://40nfyilbfa.execute-api.us-east-1.amazonaws.com/dev/add_subscrib"
    requests.post(url_add,json={"email":email,"username":username,"List":List})

 #To remove song from subscription table   
def remove_subscription(email,username,List):
    url_remove=" https://y8el9g2uv1.execute-api.us-east-1.amazonaws.com/dev/remove_subscribe"
    requests.post(url_remove,json={"email":email,"username":username,"List":List})




                               

    