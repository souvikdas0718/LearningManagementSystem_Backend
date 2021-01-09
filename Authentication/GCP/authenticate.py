from google.cloud import datastore
import json
import pymysql

def hello_world(request):
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
        try:
            connection = pymysql.connect(host='serverless-project.cwatpkmdgenk.us-east-1.rds.amazonaws.com',
                                 user='serverless', password='serverless', db='serverless', charset='utf8mb4')
        except Exception as e:
            print(e)
            return json.dumps({'Error':"SQL Connection Error"}), 500, headers
       
        request_json = request.get_json()
        if request.args:
            return ('Add data in request body', 400 , headers)
        elif request_json:
            temp = request_json.keys()
            print(temp)
            if ('email' not in temp):
                return json.dumps({'error': 'enter valid email'}), 400, headers
            if ('question' not in temp):
                return json.dumps({'error': 'enter valid question'}), 400, headers
            if ('answer' not in temp):
                return json.dumps({'error': 'enter valid answer'}), 400, headers
            body={}  
            print(type(request_json))
            email = request_json['email'] 
            question = request_json['question']
            answer = request_json['answer']
            print(email, question, answer)
            client = datastore.Client()
            query = client.query(kind='user')
            result = query.add_filter('email', '=', email).fetch(1)
            user = [dict(e) for i,e in enumerate(result)]
            if user:
                if user[0]['question'] == question and user[0]['answer'] == answer:
                    try:
                        with connection.cursor() as cursor:
                            sql = 'UPDATE `userStatus` SET  `status`= %s WHERE `email`=%s'
                            cursor.execute(sql, ("online", email))
                            connection.commit()
                            body['message']= 'User authenticate success'
                            body['statusCode']= 200
                        connection.close()
                        return json.dumps(body), headers
                    except Exception as e:
                        body['error'] = "RDS: "+str(e)
                        return json.dumps(body), 500, headers
                else:
                    body['message']='Verification failed'
                    body['statusCode']= 401 
                    print('Verification failed')
            else:
                body['error']= 'User does not exist'
                body['statusCode']= '404'  
                print('User does not exist')
            return json.dumps(body), headers     
        else:
            return ('Add data in request body', 400 , headers)
    except Exception as e:
        return ("One or more of Required data is missing from (email, question, answer)", 500, headers)
       