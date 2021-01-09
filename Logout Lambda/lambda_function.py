import json
import pymysql



def lambda_handler(event, context):
    email = event['email']
    print(email)
    body={}
    try:
        headers = {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }
        connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                             user='serverless', password='serverless', db='serverless', charset='utf8mb4')
        try:
            with connection.cursor() as cursor:
                sql = 'UPDATE `userStatus` SET  `status`=%s WHERE `email`=%s'
                cursor.execute(sql, ("offline", email))
                connection.commit()
                body['message']= 'User Logout success'
            connection.close()
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps(body)}
        except Exception as e:
            body['error'] = "RDS: "+str(e)
            return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps(body)}
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':"SQL Connection Error"})}

  