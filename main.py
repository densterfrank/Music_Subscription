# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_render_template]
# [START gae_python3_render_template]

#References:
#1.)https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
#2.)https://docs.amplify.aws/guides/functions/dynamodb-from-python-lambda/q/platform/js/#scanning-a-table
#3.)https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
#4.)https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_table_span
#5.)https://www.w3schools.com/howto/howto_css_two_columns.asp
#6.)Class material
import datetime

from flask import Flask, render_template, redirect, url_for, make_response
from flask import request


from botocore.exceptions import ClientError

import database as datacall
import json

app = Flask(__name__)


@app.route('/', methods =["GET", "POST"] )
#login fuction to deal with login html
def login():
    
    message = None
    if request.method == "POST":
        email=request.form['email']
        password=request.form['password']
        
        try:
            #To get details from login table
            json_response=datacall.get_details(email,password)
            
            if((email==json_response['Item']['email'])&(password==json_response['Item']['password'])):
                #message = json_response['Item']['user_name']
                #return render_template('main.html',json_response)
                response_object = make_response(redirect('main'))
                response_object.set_cookie('name', json_response['Item']['user_name'])
                response_object.set_cookie('email', json_response['Item']['email'])
                response_object.set_cookie('password', json_response['Item']['password'])
                return response_object
            else:
                message = 'email or password is invalid'
                return render_template('login.html',Message=message)
        except KeyError as e:
            
            message = 'email or password is invalid'
            return render_template('login.html',Message=message)
    return render_template('login.html',Message=message)

@app.route('/main', methods =["GET", "POST"])
#function to deal with main.html
def main():
    sub_result=None
    message = None
    result=None
    sub_result=None
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    email = request.cookies.get('email')
    username = request.cookies.get('name')
    if datacall.check_condition(email,username):

        sub_result=datacall.subscribtion_query(email,username)
        sub_result1=datacall.subscribtion_query(email,username)
        
        for each in sub_result:
            x=datacall.get_img(each['artist'])
            new={'link':x}
            each.update(new)
        
        response_object = render_template('main.html',valuesub=sub_result)
        #return response_object
    else:
        response_object = render_template('main.html')
    if request.method == "POST":
        
        button_ids = request.form.get('removebutton')
        if button_ids is not None:
            check=datacall.subscribtion_query(email,username)
            
            for resu in check:
                if button_ids in resu['title']:
                    datacall.remove_subscription(email,username,[resu])
                    sub_result=datacall.subscribtion_query(email,username)
                   
                    for each in sub_result:
                        x=datacall.get_img(each['artist'])
                        new={'link':x}
                        each.update(new)
                    response_object = render_template('main.html',value=result,valuesub=sub_result)
                    return response_object
        title=request.form['Title']
        artist=request.form['Artist']
        year=request.form['Year']
        if( (title=="") &( artist=="") &( year=="")):
            message="No result is retrieved"
            response_object = render_template('main.html',Error=message,value=result,valuesub=sub_result)
            return response_object
        result=datacall.scan_query(title,artist,year)
        result1=datacall.scan_query(title,artist,year)
        if result==[]:
           
            message="No result is retrieved"
            response_object = render_template('main.html',Error=message,value=result,valuesub=sub_result)
            return response_object
        for each in result:
            x=datacall.get_img(each['artist'])
            new={'link':x}
            each.update(new)
        
        button_id = request.form.get('button')
        if button_id is not None:
            for res in result1:
                if button_id in res['title']:
                    
                    datacall.add_subcription(email,username,res)
                    sub_result=datacall.subscribtion_query(email,username)
                    for each in sub_result:
                        x=datacall.get_img(each['artist'])
                        new={'link':x}
                        each.update(new)
                    response_object = render_template('main.html',value=result,valuesub=sub_result)
                    return response_object
        #for eachyear in result:
         #   eachyear["year"] = float(eachyear["year"])
        response_object = render_template('main.html',value=result,valuesub=sub_result)
        
       # response_object.set_cookie('send', value=json.dumps(result))
        #return response_object

    return response_object
@app.route('/signup', methods =["GET", "POST"])
#function to deal with signup page
def signup():
    message = None
    if request.method == "POST": 
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
          
        
            
        if (datacall.check_mail(email)):
                
                    
            message = 'The email already exists'
            return render_template('sign_up.html',Message=message)
        else:
            datacall.add_details(email,password,username) 
            message = 'Account Created,Plaese login with your Details'
            response_object = make_response(redirect('/'))
            response_object.set_cookie('Message', message)
        return response_object
    return render_template('sign_up.html',Message=message)
            

    


@app.route('/logout')
#function to deal with loutout
def logout():
    response_object = make_response(redirect('/'))
    response_object.set_cookie('admin', '', expires = 0)
    return response_object


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_render_template]
# [END gae_python38_render_template]
