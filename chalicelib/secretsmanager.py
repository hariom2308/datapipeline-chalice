import os
import json
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name=None):
    secret_name = secret_name or os.environ.get('SECRETNAME')
    try:
        #logger.debug(f'Get Secret from AWS, secret name: {secret_name}')

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager')

        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        #logger.exception('Error retrieving secrets from AWS')
        raise e
    else:
        # Depending on whether the secret was a string or binary
        # one of these fields will be populated
        #logger.debug(f'Retrieved Secret from AWS, secret name: {secret_name}')
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            return json.loads(get_secret_value_response['SecretBinary'])
