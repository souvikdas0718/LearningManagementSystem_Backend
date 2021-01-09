import boto3
import re
import json


def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client("s3")
    s3_bucket = boto3.resource('s3')
    comprehend = boto3.client("comprehend")
    if event:
        print("Event ", event)
        file_obj = event["Records"][0]
        filename = str(file_obj['s3']['object']['key'])
        print("Filename: ", filename)
        try:
            fileObj = s3.get_object(Bucket="lmsanalysis2", Key=filename)
            file_content = fileObj["Body"].read().decode('utf-8')
            file_content_list = re.split('Message', file_content)
            jsonData = []
            jsonData_new = {}
            for messages in file_content_list[1:]:
                line = messages.split("\n")
                for l in line:
                    l = l.strip()
                    temp_message = l
                    if l.startswith("data: b"):
                        l = l[7:].replace("'", "").strip()
                        temp_message = l
                        if len(l) != 0:
                            sentiment = comprehend.detect_sentiment(Text=l, LanguageCode="en")
                            print(sentiment)
                            root = {}
                            root["message"] = temp_message
                            root["sentiment"] = sentiment
                            jsonData.append(root)
                            print(jsonData)

                string = json.dumps(jsonData)
            s3_bucket.Bucket('lmssentiments').put_object(Key=filename, Body=string)


        except Exception as e:
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps(jsonData)
    }