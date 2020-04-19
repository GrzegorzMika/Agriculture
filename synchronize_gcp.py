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


def list_files_gcp(client: storage.client.Client, bucket_name: str) -> List[str]:
    """
    List all files in a bucket specified by argument bucket.
    :param bucket_name:
    :param client: connection instance to GCP service
    :param bucket: bucket name in which to list files
    :return: list of file names (without extension)
    """
    blobs = client.list_blobs(bucket_name)
    files = [blob.name.split('.')[0] for blob in blobs]
    return files


def list_files_local(path: str) -> List[str]:
    """
    List files in local directory specified by path and saved in parquet format.
    :param path: path to the local directory containing files
    :return: list of file names (without extension)
    """
    files = os.listdir(path)
    files = [f.split('.')[0] for f in files if 'pkl' in f]
    return files


def compare_lists(local_list: List[str], remote_list: List[str]) -> List[str]:
    """
    Comapre local and remote list of files and return the list of local files not stored in remote database.
    :param local_list: list of names of local files
    :param remote_list: list of names of remote files
    :return: list of names of files not stored in remote database
    """
    return list(set(local_list) - set(remote_list))


def upload(client: storage.client.Client, file_names: List[str], bucket_name: str, path: str):
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
            data = pd.read_pickle(os.path.join(path, file + '.pkl.gz'), compression="gzip")
            f = StringIO()
            data.to_csv(f, index_label=False)
            f.seek(0)
            blob = bucket.blob(file + '.csv')
            blob.upload_from_file(f, content_type='text/csv')
        except Exception as e:
            logging.error(e)


def main():
    logging.basicConfig(filename='/home/database/log.log', level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    local_storage: str = '/home/database'
    bucket_name: str = 'lilia'

    client: storage.client.Client = establish_connection()

    local_list: List[str] = list_files_local(local_storage)
    remote_list: List[str] = list_files_gcp(client, bucket_name=bucket_name)
    files_to_upload: List[str] = compare_lists(local_list, remote_list)

    upload(client, files_to_upload, bucket_name, local_storage)


if __name__ == '__main__':
    main()
