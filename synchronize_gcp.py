import logging
import os
from typing import List

import pandas as pd
from utils import find
# noinspection PyPackageRequirements
from google.cloud import storage
from io import StringIO


def establish_connection() -> storage.client.Client:
    """
    Establish a connection to Google Cloud Storage storing agriculture data.
    :return: client connection
    """
    storage_client = storage.Client.from_service_account_json(find('Agriculture.json', '/home'))
    return storage_client


def list_files_gcp(client: storage.client.Client, bucket) -> List[str]:
    """
    List all files in a bucket specified by argument bucket.
    :param client: connection instance to GCP service
    :param bucket: bucket name in which to list files
    :return: list of file names
    """
    blobs = client.list_blobs(bucket)
    files = [blob.name for blob in blobs]
    return files


def compare_lists(local_list: List[str], remote_list: List[str]) -> List[str]:
    """
    Comapre local and remote list of files and return the list of local files not stored in remote database.
    :param local_list: list of names of local files
    :param remote_list: list of names of remote files
    :return: list of names of files not stored in remote database
    """
    return list(set(local_list) - set(remote_list))


def upload(client: storage.client.Client, file_names: List[str], bucket_name, path):
    """
    Upload a specified files to a given bucket in Google Cloud Storage instance.
    :param client: connection instance to GCP service
    :param file_names: list of file names to upload
    :param bucket_name: bucket in which to store data
    :param path: loacl path where the files are stored
    """
    bucket = client.bucket(bucket_name)
    for file in file_names:
        try:
            data = pd.read_csv(os.path.join(path, file))
            f = StringIO()
            data.to_csv(f, index_label=False)
            f.seek(0)
            blob = bucket.blob(file)
            blob.upload_from_file(f, content_type='text/csv')
        except Exception as e:
            logging.error(e)


def main():
    logging.basicConfig(filename='/home/database/log.log', level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    local_storage: str = '.'
    bucket_name: str = 'lilia'

    client: storage.client.Client = establish_connection()

    local_list: List[str] = os.listdir(local_storage)
    local_list = [f for f in local_list if 'txt' in f]
    remote_list: List[str] = list_files_gcp(client, bucket=bucket_name)
    files_to_upload: List[str] = compare_lists(local_list, remote_list)

    upload(client, files_to_upload, bucket_name, local_storage)


if __name__ == '__main__':
    main()
