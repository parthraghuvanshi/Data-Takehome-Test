import psycopg2
import boto3
import hashlib

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5433'
)
cursor = conn.cursor()

# Connect to LocalStack SQS
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')

queue_url = 'http://localhost:4566/000000000000/login-queue'

def mask_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

while True:
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
    
    if 'Messages' in response:
        for message in response['Messages']:
            body = json.loads(message['Body'])
            user_id = body['user_id']
            device_type = body['device_type']
            masked_ip = mask_data(body['ip'])
            masked_device_id = mask_data(body['device_id'])
            locale = body['locale']
            app_version = int(body['app_version'])
            create_date = body['create_date']

            cursor.execute("""
                INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))
            conn.commit()

            # Delete message from the queue
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
    else:
        break

cursor.close()
conn.close()
