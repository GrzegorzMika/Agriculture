import json
import logging
from typing import List

import pandas as pd
import os

from utils import find


def find_txt(path: str) -> List[str]:
    """
    List all txt files in a given directory.
    :param path: path to the directory
    :return: list of txt files
    """
    files = os.listdir(path)
    files = [f for f in files if f.endswith('.txt')]
    return files


def pop_files(local_list: List[str], drop_files: List[str]) -> List[str]:
    """
    Drop from a list of files, files specified by drop_files.
    :param local_list: list of files
    :param drop_files: list of files to be omitted
    :return: list of files without specified files
    """
    files: List[str] = [f for f in local_list if f not in drop_files]
    return files


def compress_file(filename: str, path: str) -> None:
    """
    Compress a given file to to pickle format.
    :param filename: name of the file
    :param path: path to the file
    """
    df = pd.read_csv(os.path.join(path, filename))
    new_name = filename.split('.')[0]
    df.to_pickle(os.path.join(path, new_name + '.pkl'), compression='gzip')


def run_cleanup(files: List[str], path: str) -> None:
    """
    Remove all files specified by files.
    :param files: list of files to remove
    :param path: path to the directory containing the files
    """
    files = [os.path.join(path, file) for file in files]
    for file in files:
        os.remove(file)


def main():
    with open(find('setup_agriculture.json', '/')) as f:
        setup = json.load(f)

    local_storage: str = setup.get('local_storage')
    drop_files: List[str] = setup.get('drop_files')

    logging.basicConfig(filename=os.path.join(local_storage, 'log.log'), level=logging.WARNING,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    files: List[str] = find_txt(local_storage)
    files = pop_files(files, drop_files)
    for file in files:
        try:
            compress_file(file, local_storage)
        except Exception as e:
            logging.error(e)
    try:
        run_cleanup(files, local_storage)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()
