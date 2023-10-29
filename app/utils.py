import os
import yaml

import bz2
import _pickle as cPickle

from directories import DATA_DIR


def load_yaml_file(filepath):
    with open(filepath, encoding="utf8") as file:
        obj = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return obj


# Pickle a file and then compress it into a file with extension 
def compressed_pickle(data, filename, directory=DATA_DIR):
    """
    Saves a python object as a compressed pickled object. 
    File location and extension are controlled so user only needs to specify
    a short hand name, like "test_graph".
    """
    # This enforces save location and extension
    filename = os.path.basename(filename)
    filename, extension = os.path.splittext(filename)
    filepath = DATA_DIR / f"{filename}.pbz2"

    with bz2.BZ2File(filepath, "w") as write_file: 
        cPickle.dump(data, write_file)
    print("Saved object to: ", filepath)


# Load any compressed pickle file
def decompress_pickle(filename):
    """
    Loas a python object as a compressed pickled object. 
    File location and extension are controlled so user only needs to specify
    a short hand name, like "test_graph".
    """
    # This enforces save location and extension
    filename = os.path.basename(filename)
    filename, extension = os.path.splittext(filename)
    filepath = DATA_DIR / f"{filename}.pbz2"

    data = bz2.BZ2File(filepath, "rb")
    data = cPickle.load(data)
    return data


def chunk_it_up(arr, chunk_size):
    """
    Split an array into chunks of size `chunk_size`
    """
    for i in range(0, len(arr), chunk_size): 
        yield arr[i:i + chunk_size]