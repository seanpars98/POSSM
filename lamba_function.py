import json
import boto3
import logging
from botocore.exceptions import ClientError
import csv
from csv import writer

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    message = event["Records"]
    result = json.dumps(message)
    more = result.replace("[","")
    more = more.replace("]","")
    #edits event data to be properly readable
    
    dict = json.loads(more)
    
    values = dict["s3"]["object"]["key"]
    print('##EVENT')
    print(event)
    print('##VALUE')
    print(values)
    #sends event data to logs for debugging
    
    s3.download_file('soil-monitoring-bucket', values, '/tmp/tempfile.csv')
    
    s3.download_file('soil-monitoring-bucket', 'master/masterfile.csv', '/tmp/masterfile.csv')
    
    text1 = ""
    text2 = ""
    
    with open('/tmp/tempfile.csv', 'rt') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            text1 = row[0]
            text2 = row[1]
    #collects last two entries in the data csv file
    
    row_contents = [text1, text2]
    
    print('##DATA')
    print(text1)
    print(text2)
    #sends information to logs for debugging
    
    append_list_as_row('/tmp/masterfile.csv', row_contents)
    #appends master csv file
    
    upload_file('/tmp/masterfile.csv', 'soil-monitoring-bucket')
    
    return {
        'statusCode': 200,
        'body': json.dumps(event),
        'message': message,
        'words': dict,
        'values': values
    }
    
def upload_file(file_name, bucket, object_name= 'master/masterfile.csv'):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)