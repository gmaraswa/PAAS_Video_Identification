# Cloud_project_2 - PaaS
This project is a part of course work CSE 546: Cloud Computing.
Professor - Yuli Deng.


## Team Members
- Sai Vikhyath Kudhroli 
- Gautham Maraswami
- Abhilash Subhash Sanap 



## Project Requirements


### Software Requirements
    Python3
    Boto3 - AWS SDK for python
    face-recoginiton
    ffmpeg
    awslambdaric


    
### AWS CLI
    Install aws-cli from 
    https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### AWS Configuration.
    Use command: aws configure
    ACCESS_KEY_ID = ####
    SECRET_ACCESS_KEY_ID = ####
    REGION = us-east-1
    OUTPUT = JSON

    PEM key file for SSH Access: cc.pem

### AWS components
    S3 buckets:
    himaliainputbucket
    himaliaoutputbucket
    Dynamo DB:
    student_data

### Installing requirements

Download Python from ``https://www.python.org/downloads/``

#### Installing packages:
    boto3         : pip install boto3


### Running the application
    Make sure to install all the requirements before running the application.

    - Create S3 Bucket for input and output using AWS Console
    - Set Bucket permissions to public
    - Use the handler file provide and create a docker image using the file.
    - Create a Docker image and push it to AWS ECR. Use the following commands:
      - Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:
      - aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 630075306220.dkr.ecr.us-east-1.amazonaws.com
    - Build your Docker image using the following command:  docker build -t face_recoginition_sample .
    - After the build completes, tag your image so you can push the image to this repository:
        - docker tag face_recoginition_sample:latest 630075306220.dkr.ecr.us-east-1.amazonaws.com/face_recoginition_sample:latest
    - Run the following command to push this image to your newly created AWS repository:
        - docker push 630075306220.dkr.ecr.us-east-1.amazonaws.com/face_recoginition_sample:latest
    - Create a Lambda function from the AWS Console and define a trigger so that it is invocated when a new object is added to S3.
    - Create role for which has the following permissions
        - AmazonS3FullAccess
        - AmazonDynamoDBFullAccess
        - AWSXRayDaemonWriteAccess
        - AWSLambdaBasicExecutionRole
    - Assign the role to the AWS Lambda function
    - Update input bucket name in  Workload generator and run the to input bucket.

### Member tasks
#### Sai Vikhyath Kudhroli
- Created the face recognition handler that is executed when the lambda is triggered.
- Loaded the encoding data which is used to recognize the faces in the video.
- Extract the key of the video file which is uploaded to S3 and download the video from the input bucket.
- Use the downloaded video to extract all the frames in the video.
- Extract the first frame that contains a person and generate encoding for it.
- Developed the face recognition logic to extract the name of the person in the video.
- Use this name to extract academic information about the person from DynamoDB.
- Create a CSV file with all the academic information extracted from DynamoDB.
- Push this CSV file into the output S3 bucket.


#### Gautham Maraswami (1225222063)
- Set up S3 Buckets programmatically using boto3 libraries.
Configured buckets, so that the workload generator and lambda functions are able to upload and download files to the bucket seamlessly.
- Set up DynamoDb using Boto 3 libraries.
- Defined Schema, keys, attribute definitions, and Throughput so as enable correct configurations of DynamoDb.
- Set up user roles for lambda functions for correct access to Log files, S3 Buckets, and DynamoDb.
- Developed a testing mechanism to check if the generated outputs are correct.
- Manually and programmatically compared the generated outputs in the S3 Bucket and the mapping files provided in the bootstrap file. 
- Loaded the data provided in the JSON file into DynamoDB.


#### Abhilash Subhash Sanap (1225222362)
- Read and understood the DockerFile and entry.sh file.
- Created an AWS Elastic Container Registry (ECR) repository.
- Built the docker image from the given Docker File.
- Configured the programmatic access to the ECR and pushed the image to it.
- Configured an AWS Lambda function through the console using the “latest” image.
- When the lambda function failed to run, I debugged the issue and set the memory requirement and timeout to an appropriate value. 
- Understood the triggers Defined a trigger on the lambda function such that it is invocated every time an object is added to the input bucket.


