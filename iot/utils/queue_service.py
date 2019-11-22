import boto3


class QueueService:
    AWS_ACCESS_KEY = 'AKIAVUCMWN63SXDTHQBM'
    AWS_SECRET_KEY = '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'
    AWS_REGION= "eu-west-1"
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=QueueService.AWS_ACCESS_KEY,
            aws_secret_access_key=QueueService.AWS_SECRET_KEY,
            region_name=QueueService.AWS_REGION
        )
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=QueueService.AWS_ACCESS_KEY,
            aws_secret_access_key=QueueService.AWS_SECRET_KEY,
            region_name=QueueService.AWS_REGION
        )

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

