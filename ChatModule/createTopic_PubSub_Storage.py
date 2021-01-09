import os
import json
from google.cloud import pubsub_v1, storage

project_id = "serverless-project-283717";


def checkTopic():
    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(project_id)
    print(type(publisher.list_topics(project_path)))
    v = 0
    for topic in publisher.list_topics(project_path):
        v = 1
    if v == 1:
        return 1
    else:
        return 0


def subscribeUser(topic_id, user_id):
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, user_id)
    with subscriber:
        subscription = subscriber.create_subscription(subscription_path, topic_path)

    print("A subscription has been created created: ".format(subscription))


def cloudStorage(fileName):
    gcs_client = storage.Client(project=project_id)
    bucket = gcs_client.get_bucket('lms_bucket')
    fileName = "/tmp/"+fileName + ".txt"
    f = open(fileName, 'w')
    blob = bucket.blob(f.name)
    blob.upload_from_filename(f.name)
    os.remove(fileName)
    print("bucket created: " + fileName)


def createTopic(request):
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
        headers = {
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Max-Age': '1296000',
            'Content-Type': 'application/json'
        }
        if checkTopic() == 1:
            print("Topic exists");
            return json.dumps("Already an active topic exists"), 500 , {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }
        else:
            project_id = "serverless-project-283717";
            topic_id = data.get('topic_name')
            user_ids = data.get('userID')
            uniqueFileName = data.get('uniqueFileName')

            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_id)

            topic = publisher.create_topic(topic_path)
            print("Topic created: {}".format(topic))
            i=0
            for user in user_ids:
                u_arr = user.split("@")
                user = u_arr[0]
                subscribeUser(topic_id, user)
                print("subscriber: ", user)

        cloudStorage(uniqueFileName)
        return ("success"), 200, {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }
    except Exception as e:
            # print(e)
        return json.dumps({'Error':str(e)}), 500, {
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Max-Age': '3600'
            }