import boto3
import io

s3 = boto3.resource('s3')

google_access_key_id="GOOG1EAJR4ZVDKM7K5KLOCWWIR7H76AQG6LDSAIWR5GMIJLL5WMZKDQ2CEJXA"
google_access_key_secret="yyXtRBgIKTsMVFxFeRB+IFL/aWM3CL1RzLMMf0j+"

gc_bucket_name="lms_bucket"


def get_gcs_objects(google_access_key_id, google_access_key_secret,
                     gc_bucket_name):
    """Gets GCS objects using boto3 SDK"""
    client = boto3.client("s3", region_name="auto",
                          endpoint_url="https://storage.googleapis.com",
                          aws_access_key_id=google_access_key_id,
                          aws_secret_access_key=google_access_key_secret)

    # Call GCS to list objects in gc_bucket_name
    response = client.list_objects(Bucket=gc_bucket_name)

    # Print object names
    print("Objects:")
    for blob in response["Contents"]:
        print(blob)
        file_name = blob['Key']
        farr = file_name.split("/")
        object = s3.Object('lmsanalysis2', farr[2])
        f = io.BytesIO()
        client.download_fileobj(gc_bucket_name,file_name,f)
        object.put(Body=f.getvalue())

def lambda_handler(event, context):
    get_gcs_objects(google_access_key_id,google_access_key_secret,gc_bucket_name)
    return "sucess"