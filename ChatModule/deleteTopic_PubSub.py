import os
import json
from google.cloud import pubsub_v1

project_id = "serverless-project-283717"


def removeTopic(topic_id):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    if publisher.delete_topic(topic_path):
        return True
    else:
        return False

def unsubscribe(user_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, user_id)
    with subscriber:
        subscriber.delete_subscription(subscription_path)
        print("Subscriber deleted: ", user_id)


def deleteTopic(request):
    data = request.get_json()
    print(data)
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

        topic_id = data.get('topic_name')
        subscriber_ids = data.get('subscribers')
        for subscriber in subscriber_ids:
            print(subscriber)
            unsubscribe(subscriber)
        if removeTopic(topic_id):
            print("Topic deleted ", topic_id);
        return ("pub/sub deleted",200 , {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            })
    except Exception as e:
        return json.dumps({'Error': str(e)}), 500, {
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Max-Age': '3600'
        }