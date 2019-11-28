from datetime import date
from botocore.exceptions import ClientError
from iot.utils.queue_service import AWSService

import logging


def download_file(file_name, bucket, object_name=None):
    awsService = AWSService()

    try:
        s3 = awsService.s3
        with open(file_name, 'wb') as f:
            s3.download_fileobj(bucket, object_name, f)
    except ClientError as e:
        logging.error(e)
        return False
    return True


obj_name = str(date.today()) + 'data.json'
download_file('data_downloaded.json', 'scalable-iot-devices', obj_name)
