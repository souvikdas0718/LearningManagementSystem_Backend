import os
import json
from google.cloud import pubsub_v1, storage

project_id = "serverless-project-283717";
count = 1


def appendToCloudStorageFile(message):
    client = storage.Client()
    bucket = client.get_bucket('lms_bucket')
    print("Unique File: ", uniqueFileName)
    blob = bucket.get_blob(uniqueFileName)
    blob.download_to_filename(uniqueFileName)
    with open(uniqueFileName, 'a') as file_object:
        file_object.write(message)
    blob = bucket.blob(uniqueFileName)
    blob.upload_from_filename(uniqueFileName)
    print("inside storage")


def callback(message):
    payLoad = {}
    payLoad['data'] = message.data.decode('utf-8')
    payLoad['user'] = message.attributes.get("username")
    chats.append(payLoad)
    print("Received message: {}".format(message.data))
    message.ack()
    appendToCloudStorageFile(str(message))
    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print("{}: {}".format(key, value))


def subscriber(request):
    global chats
    global uniqueFileName
    chats = []
    uniqueFileName = ""
    data = request.get_json()
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
        subscription_id = data.get("sub_id")
        uniqueFileName = data.get("uniqueFileName")
        uniqueFileName = "/tmp/" + uniqueFileName
        subscriber_client = pubsub_v1.SubscriberClient()
        subscription_path = subscriber_client.subscription_path(project_id, subscription_id)
        streaming_pull_future = subscriber_client.subscribe(
            subscription_path, callback=callback
        )
        print("Listening for messages on \n".format(subscription_path))

        try:
            streaming_pull_future.result(timeout=5.0)
        except:
            streaming_pull_future.cancel()

        subscriber_client.close()
        print("Message to be sent", chats)
        temp = chats
        chats = []
        uniqueFileName = ""
        return json.dumps(temp), 200, {
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Max-Age': '3600'
        }
    except Exception as e:
        return json.dumps({'Error': str(e)}), 500, {
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Max-Age': '3600'
        }
