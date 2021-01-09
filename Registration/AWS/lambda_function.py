import json
import pymysql
import pymysql.cursors
import requests
import sys
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64

USER_POOL_ID = 'us-east-1_DUJ1OFR0U'
CLIENT_ID = '75q99f08ahuqof4eqbh98rt61v'
CLIENT_SECRET = '1g364uimbpa0im65u7dds1rocldtq6447iior2barrohgf05rcau'


def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode(
        'utf-8'), msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def lambda_handler(event, context):
    body = {}
    try:
        connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                                 user='serverless', password='serverless', db='serverless', charset='utf8mb4')
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':"SQL Connection Error"})}
    # print(event)
    try:
        data = eval(event['body'])
        email = data['email']
        name = data['name']
        password = data['password']
        role = data['role']
        instituteName = data['instituteName']
        question = data['question']
    except Exception as e:
        body['error'] = "Request-error"+str(e)
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps(body)}
    try:
        client = boto3.client('cognito-idp')
        resp = client.sign_up(ClientId=CLIENT_ID, SecretHash=get_secret_hash(email), Username=email, Password=password,  UserAttributes=[
                              {'Name': "email", 'Value': email}, {'Name': "custom:question", 'Value': question}], ValidationData=[{'Name': "email", 'Value': email}])
    except client.exceptions.UsernameExistsException as e:
        body['error'] = "Cognito-Error: "+"This username already exists"
        return {'statusCode': 409, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps(body)}
    except Exception as e:
        body['error'] = "Cognito-Error: "+str(e)
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps(body)}
    else:
        try:
            print('inside try')
            with connection.cursor() as cursor:
                sql = "INSERT INTO `user` (`name`, `email`, `password`, `instituteName`, `role`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, password, instituteName, role))
                connection.commit()
                sql1 = "INSERT INTO `userStatus` (`email`, `name`) VALUES (%s, %s)"
                cursor.execute(sql, (email, name))
                connection.commit()
                body["message"] = "Success"
            connection.close()
            print(body)
            return { 'statusCode': 200, 'body': json.dumps(body), 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}}
        except Exception as e:
            body['error'] = "RDS: "+str(e)
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps(body)}
