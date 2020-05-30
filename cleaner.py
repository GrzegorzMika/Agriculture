import json
import logging
import os

import pandas as pd

from utils import find


def find_txt(path):
    """
    List all txt files in a given directory.
    :param path: path to the directory
    :return: list of txt files
    """
    files = os.listdir(path)
    files = [f for f in files if f.endswith('.txt')]
    return files


def pop_files(local_list, drop_files):
    """
    Drop from a list of files, files specified by drop_files.
    :param local_list: list of files
    :param drop_files: list of files to be omitted
    :return: list of files without specified files
    """
    files = [f for f in local_list if f not in drop_files]
    return files


def compress_file(filename, path):
    """
    Compress a given file to to pickle format.
    :param filename: name of the file
    :param path: path to the file
    """
    df = pd.read_csv(os.path.join(path, filename))
    new_name = filename.split('.')[0]
    df.to_pickle(os.path.join(path, new_name + '.pkl'), compression='gzip')


def run_cleanup(files, path):
    """
    Remove all files specified by files.
    :param files: list of files to remove
    :param path: path to the directory containing the files
    """
    files = [os.path.join(path, file) for file in files]
    for file in files:
        os.remove(file)


def cleaner(setup: dict):
    log_storage = setup.get('log_storage')
    local_storage = setup.get('local_storage')
    drop_files = setup.get('drop_files')

    logging.basicConfig(filename=os.path.join(log_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    files = find_txt(local_storage)
    files = pop_files(files, drop_files)
    for file in files:
        try:
            compress_file(file, local_storage)
        except Exception as e:
            logger.error(e, exc_info=True)
    try:
        run_cleanup(files, local_storage)
    except Exception as e:
        logger.error(e, exc_info=True)
