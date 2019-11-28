import boto3


class AWSService:
    def __init__(self):
        self.sqs = boto3.client('sqs')
        self.s3 = boto3.client('s3')

    def receive_and_delete_message(self, queue_url):
        data = []
        response = self.sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        if 'Messages' in response:
            for message in response['Messages']:
                data.append(message['Body'])
                self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
        return data

    def send(self, queue_url, data, msg_group_id):
        self.sqs.send_message(QueueUrl=queue_url, MessageBody=str(data),
                              MessageGroupId=msg_group_id)

