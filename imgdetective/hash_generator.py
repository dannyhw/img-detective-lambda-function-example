"""
Module containing hash generating functions for images.
"""
from __future__ import absolute_import, division, print_function

import imagehash
from PIL import Image


def generate_hashes_for_image(img_path):
    """
    This function is used to generate various hashes for an image and return a
    dictionary which contains each of these hashes.

    args:
        img_path - path to the image which we will generate the hashes for.
    returns:
        hashes - Dict containing boolean arrarys representing hashes of the
        supplied image.
    """
    print ("Generating hash for: " + img_path)
    img = Image.open(img_path)

    hashes = {}
    hashes['ahash'] = imagehash.average_hash(img, hash_size=8)
    hashes['phash'] = imagehash.phash(img, hash_size=8)
    hashes['dhash'] = imagehash.dhash(img, hash_size=8)
    hashes['whash'] = imagehash.whash(img, hash_size=8)
    hashes['whashDb4'] = imagehash.whash(img, mode='db4')

    return hashes
