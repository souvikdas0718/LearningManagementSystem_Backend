import json
import requests
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
    print(event)
    data = eval(event['body'])
    print(data)
    try:
        client = boto3.client('cognito-idp')
        auth_data = { 'USERNAME':data['email'], 'PASSWORD':data['password'], "SECRET_HASH": get_secret_hash(data['email']) }
        resp = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', AuthParameters=auth_data, ClientId=CLIENT_ID)
        token = resp['AuthenticationResult']['AccessToken']
        try:
            client = boto3.client('cognito-idp')
            response = client.get_user(AccessToken=token)
            question = response['UserAttributes'][2]['Value']
            email = response['UserAttributes'][3]['Value']
            return {
                "statusCode": 200,
                'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({'question':question,"email":email, 'token': token})
            }
        except client.exceptions.ResourceNotFoundException as e:
            print("1: ",str(e))
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':"Missing required parameter email."})}
        except client.exceptions.InvalidParameterException as e:
            print("2: ",str(e))
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':str(e)})}
        except client.exceptions.NotAuthorizedException as e:
            print("3: ",str(e))
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':str(e)})}
        except client.exceptions.UserNotFoundException as e:
            print("4: ",str(e))
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':str(e)})}
        except Exception as e:
            print("5: ",str(e))
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':str(e)})}
    except client.exceptions.NotAuthorizedException as e:
        print("err", str(e))
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':"Incorrect username or password"})}
    except Exception as e:
        print("err1", str(e))
        temp = str(e).split(':')[1]
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':temp})}
    # else:                        
    #     try:
    #         data1 = json.dumps({'email': data['email'], 'question': data['question'], 'answer': data['answer']})
    #         response = requests.post('https://us-central1-serverless-project-283717.cloudfunctions.net/userAuthentication', data=data1, headers={'Content-Type': 'application/json'})
    #         print(response.text)
    #         return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'msg': str(response.text)}) }
    #     except Exception as e:
    #         print("err2", str(e))
    #         return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':str(e)})}

    
#--------------------------------------------------------------
# CODE FOR DELETE COGNITO DATA
#--------------------------------------------------------------
    # client = boto3.client('cognito-idp')
    # response = client.list_users(UserPoolId=USER_POOL_ID, AttributesToGet=[])
    # print(response)
    # for i in response['Users']:
    #     print(i['Username'])
    #     response1 = client.admin_delete_user(UserPoolId=USER_POOL_ID,Username=str(i['Username'])            )
    # response = client.list_users(UserPoolId=USER_POOL_ID, AttributesToGet=[])
    # print(len(response['Users']))
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    
#--------------------------------------------------------------
# CODE TO GET EMAILID FROM TOKEN
#--------------------------------------------------------------
# try:
#         token = 'ayJraWQiOiJNVUdWVFVZa09ORE1UNWRXcHhwVWdWNjhBa0pnRmpnMCs0Z2pPdUk1QlF3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjNWVkNWE5Yy1hYmJjLTQ3OGMtODdiNi0zYTNkZjE4ZGE4N2QiLCJldmVudF9pZCI6IjY1ODJiYTFiLTk0NzItNDU1Ny1hYmIwLThjMTAxZjMxODQyMyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTU0NjIxMzYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RVSjFPRlIwVSIsImV4cCI6MTU5NTQ2NTczNiwiaWF0IjoxNTk1NDYyMTM2LCJqdGkiOiIwM2Q3ZDYxNi1mMTAxLTQ1OTctOGU2ZC00YWE1YTEwNmM4ZGUiLCJjbGllbnRfaWQiOiI3NXE5OWYwOGFodXFvZjRlcWJoOThydDYxdiIsInVzZXJuYW1lIjoiYzVlZDVhOWMtYWJiYy00NzhjLTg3YjYtM2EzZGYxOGRhODdkIn0.a39EGqFj5oA6YIAHBTsIYk3uGIXcUMc9P80Vsh9fIz8D2y3SdRr0qpUf_ojSv3MyoiZc961jeIMbSEZsabs4blPdFsPYvyONJW6_P4f7Uu-RHk4J5jib4ZSbOBm4ibSEbOIfKKqQPVTW4bsRTRQpt8qoDdNn6X3h5_ip2l5dEOXgkkNUhnuZZ16z6Hg_xbFwaO1b49i3kb4jQm9CryeXVYQN0stD-24zlRY9KK_BgpoL7cYuWVFqI6pMO-DvQagVILNgFqc2UcEbsnB8urI9PZkeSgeVm38bVDpcyodoj5qD-bdxB5Lw_thsvhyc2CcaIBZNzTLnmo5KgansegOQ6Q'
#         client = boto3.client('cognito-idp')
#         response = client.get_user(AccessToken=token)
#         print(response['UserAttributes'][2]['Value'])
#         return {
#             "statusCode": 200,
#             "msg": 'ok'
#         }
#     except client.exceptions.ResourceNotFoundException as e:
#         print("1: ",str(e))
#     except client.exceptions.InvalidParameterException as e:
#         print("2: ",str(e))
#     except client.exceptions.NotAuthorizedException as e:
#         print("3: ",str(e))
#     except client.exceptions.UserNotFoundException as e:
#         print("4: ",str(e))
#     except Exception as e:
#         print("5: ",str(e))