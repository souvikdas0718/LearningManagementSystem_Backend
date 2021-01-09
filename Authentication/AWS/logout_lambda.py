import json
import requests
import boto3
import botocore.exceptions
import pymysql

# USER_POOL_ID = 'us-east-1_DUJ1OFR0U'
# CLIENT_ID = '75q99f08ahuqof4eqbh98rt61v'
# CLIENT_SECRET = '1g364uimbpa0im65u7dds1rocldtq6447iior2barrohgf05rcau'


def lambda_handler(event, context):
    # print(event)
    # data = eval(event['body'])
    # print(data)
    try:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)
        headers = {
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*', 
            'Access-Control-Max-Age': '1296000', 
            'Content-Type': 'application/json'
        }
        token = 'ayJraWQiOiJNVUdWVFVZa09ORE1UNWRXcHhwVWdWNjhBa0pnRmpnMCs0Z2pPdUk1QlF3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjNWVkNWE5Yy1hYmJjLTQ3OGMtODdiNi0zYTNkZjE4ZGE4N2QiLCJldmVudF9pZCI6IjY1ODJiYTFiLTk0NzItNDU1Ny1hYmIwLThjMTAxZjMxODQyMyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1OTU0NjIxMzYsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RVSjFPRlIwVSIsImV4cCI6MTU5NTQ2NTczNiwiaWF0IjoxNTk1NDYyMTM2LCJqdGkiOiIwM2Q3ZDYxNi1mMTAxLTQ1OTctOGU2ZC00YWE1YTEwNmM4ZGUiLCJjbGllbnRfaWQiOiI3NXE5OWYwOGFodXFvZjRlcWJoOThydDYxdiIsInVzZXJuYW1lIjoiYzVlZDVhOWMtYWJiYy00NzhjLTg3YjYtM2EzZGYxOGRhODdkIn0.a39EGqFj5oA6YIAHBTsIYk3uGIXcUMc9P80Vsh9fIz8D2y3SdRr0qpUf_ojSv3MyoiZc961jeIMbSEZsabs4blPdFsPYvyONJW6_P4f7Uu-RHk4J5jib4ZSbOBm4ibSEbOIfKKqQPVTW4bsRTRQpt8qoDdNn6X3h5_ip2l5dEOXgkkNUhnuZZ16z6Hg_xbFwaO1b49i3kb4jQm9CryeXVYQN0stD-24zlRY9KK_BgpoL7cYuWVFqI6pMO-DvQagVILNgFqc2UcEbsnB8urI9PZkeSgeVm38bVDpcyodoj5qD-bdxB5Lw_thsvhyc2CcaIBZNzTLnmo5KgansegOQ6Q'
        client = boto3.client('cognito-idp')
        response = client.get_user(AccessToken=token)
        email = response['UserAttributes'][2]['Value']
        print(email)
        try:
            connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                                 user='serverless', password='serverless', db='serverless', charset='utf8mb4')
            try:
                with connection.cursor() as cursor:
                    sql = 'UPDATE `userStatus` SET  `status`= %s WHERE `email`=%s'
                    cursor.execute(sql, ("offline", email))
                    connection.commit()
                    body['message']= 'User Logout success'
                connection.close()
                return json.dumps(body), 200, headers
            except Exception as e:
                body['error'] = "RDS: "+str(e)
                return json.dumps(body), 500, headers
        except Exception as e:
            print(e)
            return json.dumps({'Error':"SQL Connection Error"}), 500, headers
        # return {
        #     "statusCode": 200,
        #     "msg": 'ok'
        # }
    except client.exceptions.ResourceNotFoundException as e:
        print("1: ",str(e))
    except client.exceptions.InvalidParameterException as e:
        print("2: ",str(e))
    except client.exceptions.NotAuthorizedException as e:
        print("3: ",str(e))
    except client.exceptions.UserNotFoundException as e:
        print("4: ",str(e))
    except Exception as e:
        print("5: ",str(e))
  