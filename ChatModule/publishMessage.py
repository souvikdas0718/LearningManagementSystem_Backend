import os
from google.cloud import pubsub_v1


project_id = "serverless-project-283717";


def publish_message(userName, message, topic_id):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = message
    data = data.encode("utf-8")
    future = publisher.publish(
        topic_path, data, origin="python-sample", username=userName
    )
    print(future.result())
    print("Published messages with custom attributes.")


def publishMessage(request):
    try:
        if request.method == 'OPTIONS':
                headers = {
                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Max-Age': '3600'
                }
                return ('', 204, {
                    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Max-Age': '3600'
                })
        data = request.get_json()
        uName = data.get('username')
        message = data.get('message')
        topic = data.get('topic_name')
        print("useraneme ", uName)
        print("message ", message)
        publish_message(uName, message, topic)
        return ("success"), 200, {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }
    except Exception as e:
        return json.dumps({'Error':str(e)}), 500, {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }