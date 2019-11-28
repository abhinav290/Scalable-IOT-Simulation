from datetime import date
from botocore.exceptions import ClientError
from iot.utils.queue_service import AWSService

import logging


def upload_file(file_name, bucket, object_name=None):
    queueService = AWSService()

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = str(date.today()) + file_name
    try:
        response = queueService.s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
upload_file('data.json', 'scalable-iot-devices')