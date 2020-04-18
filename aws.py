import boto3
from botocore.exceptions import NoCredentialsError


ACCESS_KEY = ''
SECRET_KEY = ''


def get_AWS_client():
	s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_key=SECRET_KEY)
	return s3


def upload_to_AWS(s3, local_file, bucket, s3_file):
	try:
		s3.upload_file(local_file, bucket, s3_file)
		print("Upload Successful")
		return True
	except FileNotFoundError:
		print("That file was not file")
		return False
	except NoCredentialsError:
		print("Credentials not available")
		return False

	