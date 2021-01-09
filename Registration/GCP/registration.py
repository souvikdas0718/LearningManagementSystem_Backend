from google.cloud import storage, datastore
import requests
import time
import json
import logging
import re

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Users\deepd\Downloads\serverless-project-283717-2ff5adc71c65.json'
email_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
password_re = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})'

def email_check(email):
    if len(email) == 0:
        print("Email is requried")
        return True
    elif(re.search(email_re,email)):  
        print("Valid Email")  
        return False
    else:  
        print("Invalid Email")
        return True

def password_check(password):
    if len(password) == 0:
        print("Password is requried")
        return True 
    elif re.search(password_re, password) == None:  
        print("Invalid Password")  
        return True  
    else:  
        print("Valid Password")
        return False

def check_valid(name, question, answer, instituteName,role):
    if len(name) == 0 or len(question) == 0 or len(answer) == 0 or len(instituteName) == 0 or len(role) == 0:
        print("Field is requried")
        return True
    else:  
        print("Valid Data")
        return False

def hello_world(request): 
    body = {}
    response={"Error":"Fail"}
    try:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)
        # "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        headers = {
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*', 
            'Access-Control-Max-Age': '1296000', 
            'Content-Type': 'application/json'
        }
        # request_json=True
        request_json = request.get_json()
        if request_json:
            temp = request_json.keys()
            print(temp)
            if ('name' not in temp): 
                return json.dumps({'error': 'enter valid name'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if ('email' not in temp):
                return json.dumps({'error': 'enter valid email'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if ('question' not in temp):
                return json.dumps({'error': 'enter valid question'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if ('answer' not in temp):
                return json.dumps({'error': 'enter valid answer'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if ('password' not in temp):
                return json.dumps({'error': 'enter valid password'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if ('instituteName' not in temp):
                return json.dumps({'error': 'enter valid instituteName'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if ('role' not in temp):
                return json.dumps({'error': 'enter valid role'}), 400, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            
            email = request_json['email'] 
            question = request_json['question']
            answer = request_json['answer']
            name = request_json['name']
            instituteName = request_json['instituteName']
            password = request_json['password']
            role = request_json['role']
            response = {}
            # response.headers.set('Access-Control-Allow-Origin', '*')
            # response.headers.set('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS, POST')
            # response.headers.set('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
            # print(request_json)
            flag = 0
            print('flag', flag)
            if email_check(email):
                response['email_error'] = 'Invalid Email'
                print('check email called...')
                flag = 1
            if password_check(password):
                response['password_error'] = 'Invalid Password'
                print('check password called...')
                flag = 1
            if check_valid(name, question, answer, instituteName, role):
                response['other_error'] = 'Invalid Other'
                print('check valid called...')
                flag = 1
            print('flag', flag)
            if flag == 1:
                return json.dumps(response), 400 , { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            data1 = { "email": email, "name": name, "password": password, "instituteName": instituteName, 'role': role, 'question':question }
            # print(email,password, answer, question, name, instituteName)
            response1 =  requests.post("https://do3vuuv41l.execute-api.us-east-1.amazonaws.com/login/register" ,data=json.dumps(data1), headers = {'Content-Type': 'application/json', 'Accept':'text/plain'})
            # time.sleep(5)
            print(response1)
            logging.info(response1.text)
            print(response1.text)
            response = eval(response1.text)
            STATUS_CODE = response1.status_code
            if STATUS_CODE == 409:
                return json.dumps(body),409, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            if STATUS_CODE == 200:
                try:
                    client = datastore.Client()
                    entity = datastore.Entity(key=client.key('user'))
                    entity.update({ 'email': email, 'question': question, 'answer': answer})
                    client.put(entity)
                    body['message'] = 'Success'
                    return json.dumps(body), 200, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
                except Exception as e:
                    print("ERR", str(e))
                    body['message'] = str(e)
                    return json.dumps(response), 500, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            else:
                body['message'] = response['error']
                return json.dumps(response), 500, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
            # except Exception as e:  
            #     body['message'] = str(e)
            #     return {'statusCode': 200,  'headers': , 'body': json.dumps(response)}
        else: 
            body['error'] = "One or more of Required data is missing from (name, email, password, institutename,role,question, answer)"
            return json.dumps(body), 500, { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
    except Exception as e: 
        # body['message'] = str("e")
        print("ERROR:",str(e))
        return json.dumps(response), 500,  { "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS, POST","Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept","Access-Control-Allow-Origin": "*","Access-Control-Max-Age": "1296000", 'Content-Type': 'application/json'}
    
