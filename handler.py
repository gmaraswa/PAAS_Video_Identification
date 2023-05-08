import os

from boto3 import client as boto3_client
from boto3.dynamodb.conditions import Key
import boto3
import face_recognition
import pickle
import csv

from boto3.dynamodb.conditions import Key

input_bucket = "himaliainputbucket"
output_bucket = "himaliaoutputbucket"
table_name = "student_data"
s3 = boto3_client('s3')
dynamodb = boto3.resource('dynamodb')


# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def download_from_s3(key):
	with open('/tmp/'+key, 'wb') as f:
		s3.download_fileobj(input_bucket, key, f)
	
def generate_encoding(key):
	os.system(f"ffmpeg -i /tmp/{key} -r 1 /tmp/image-%3d.jpg")
	
	# video_frame_list = os.listdir("/tmp/")
	# print(f"video_frame_list: {video_frame_list}")
	
	image_from_video = face_recognition.load_image_file(f"/tmp/image-001.jpg")
	image_from_video_encoding = face_recognition.face_encodings(image_from_video)[0]

	return image_from_video_encoding

def recognise_face(image_from_video_encoding, input_encoding):
	
	names = input_encoding['name']
	known = input_encoding['encoding']

	results = face_recognition.compare_faces(known, image_from_video_encoding)
	i = 0
	while i < len(results):
		if results[i]:
			break
		i += 1
	index_of_match = i
	name_of_match = names[index_of_match]

	return name_of_match

def fetch_data_from_dynamodb(name_of_match):

	table = dynamodb.Table(table_name)
	response = table.query(KeyConditionExpression=Key('name').eq(name_of_match))
	return response['Items'][0]

def write_to_csv(result_dictionary, name):
	print(f"Item response: {result_dictionary}")
	header = ["Name", "Major", "Year"]
	data = [result_dictionary['name'], result_dictionary['major'], result_dictionary['year']]

	with open(f'/tmp/{name}.csv', 'w', encoding='UTF8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerow(data)


def face_recognition_handler(event, context):
	print("Lambda event is triggered.")
	input_encoding = open_encoding('encoding')
	key = event['Records'][0]['s3']['object']['key']
	print(f"Input bucket: {input_bucket}, key:{key}")

	name, extension = key.split(".")
	download_from_s3(key)
	image_from_video_encoding = generate_encoding(key)
	name_of_match = recognise_face(image_from_video_encoding,input_encoding)
	result_dictionary = fetch_data_from_dynamodb(name_of_match) 
	write_to_csv(result_dictionary, name)

	s3.upload_file(f"/tmp/{name}.csv", output_bucket, f"{name}.csv")


