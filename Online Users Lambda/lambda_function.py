import json
import pymysql
import pymysql.cursors

def lambda_handler(event, context):
    # TODO implement
    print(event)
    try:
        connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                                 user='serverless', password='serverless', db='serverless', charset='utf8mb4')
        with connection.cursor() as cursor:
            sql = "SELECT email FROM `userStatus` where `status`= 'online'"
            cursor.execute(sql)
            result = cursor.fetchall()
            user = []
            for i in result:
                user.append(''.join(i))
            print(user)
            return {
                "statusCode": 200,
                'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({'online':user})
            }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':"Some internal error!"})}
    


# exports.handler = async (event) => {
#     console.log(event)
#     console.log("-----------------------------------------")
#     console.log(event.currentIntent.slots.OrganizationNames)
#     const org = event.currentIntent.slots.OrganizationNames;
#     // TODO implement
#     const response = {     
#   "sessionAttributes": {
#       "key1": "value1",
#       "key2": "value2"
#     },   
#     "dialogAction": {     
#         "type": "Close",
#         "fulfillmentState": "Fulfilled",
#         "message": {       
#           "contentType": "PlainText",
#           "content": org
#         },    
#      } 
# };
#     // const response = {
#     //     statusCode: 200,
#     //     body: JSON.stringify('Hello from Lambda!'),
#     // };
#     return response;
# };
import json
import pymysql
import pymysql.cursors

def lambda_handler(event, context):
    # TODO implement
    print(event)
    try:
        connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                                 user='serverless', password='serverless', db='serverless', charset='utf8mb4')
        with connection.cursor() as cursor:
            sql = "SELECT email FROM `userStatus` where `status`= 'online'"
            cursor.execute(sql)
            result = cursor.fetchall()
            user = []
            for i in result:
                user.append(''.join(i))
            print(user)
            return {
                "statusCode": 200,
                'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"},
                "body": json.dumps({'online':user})
            }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}, "body": json.dumps({'Error':"Some internal error!"})}
    


# exports.handler = async (event) => {
#     console.log(event)
#     console.log("-----------------------------------------")
#     console.log(event.currentIntent.slots.OrganizationNames)
#     const org = event.currentIntent.slots.OrganizationNames;
#     // TODO implement
#     const response = {     
#   "sessionAttributes": {
#       "key1": "value1",
#       "key2": "value2"
#     },   
#     "dialogAction": {     
#         "type": "Close",
#         "fulfillmentState": "Fulfilled",
#         "message": {       
#           "contentType": "PlainText",
#           "content": org
#         },    
#      } 
# };
#     // const response = {
#     //     statusCode: 200,
#     //     body: JSON.stringify('Hello from Lambda!'),
#     // };
#     return response;
# };
                  