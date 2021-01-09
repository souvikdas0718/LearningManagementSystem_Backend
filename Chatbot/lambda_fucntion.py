import json
import pymysql
import pymysql.cursors

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print("-----------------------------------------")
    print(event['currentIntent']['slots']['OrganizationNames'])
    org = event['currentIntent']['slots']['OrganizationNames']
    try:
        connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                                 user='serverless', password='serverless', db='serverless', charset='utf8mb4')
        with connection.cursor() as cursor:
            sql = "SELECT name FROM `userStatus` where `instituteName`=%s and `status`= 'online' "
            cursor.execute(sql, (org))
            result = cursor.fetchall()
            user = ""
            for i in result:
                user = user + ', ' + '\n'.join(i)
            print(user)
            return {     
                   "sessionAttributes": {
                      "key1": "value1",
                      "key2": "value2"
                    },   
                    "dialogAction": {     
                        "type": "Close",
                        "fulfillmentState": "Fulfilled",
                        "message": {       
                           "contentType": "PlainText",
                           "content": "Online useres are: \n"+user[1:]
                        },    
                     } 
                };
    except Exception as e:
        print(e)
        return {     
   "sessionAttributes": {
      "key1": "value1",
      "key2": "value2"
    },   
    "dialogAction": {     
        "type": "Close",
        "fulfillmentState": "Failed",
        "message": {       
           "contentType": "PlainText",
           "content": "Error"
        },    
     } 
};
    


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
