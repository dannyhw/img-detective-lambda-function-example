from __future__ import absolute_import, division, print_function

# import six
import imagehash
from PIL import Image


# def get_hash_method(hashmethod):
#     hash_methods = {
#         'ahash': imagehash.average_hash,
#         'phash': imagehash.phash,
#         'dhash': imagehash.dhash,
#         'whash-haar': imagehash.whash,
#         'whash-db4': lambda img: imagehash.whash(img, mode='db4')
#     }
#     return hash_methods[hashmethod]


def generate_hashes_for_image(imgPath):

    print ("Generating hash for: " + imgPath)
    img = Image.open(imgPath)

    data = {}
    data['ahash'] = imagehash.average_hash(img, hash_size=8)
    data['phash'] = imagehash.phash(img, hash_size=8)
    data['dhash'] = imagehash.dhash(img, hash_size=8)
    data['whash'] = imagehash.whash(img, hash_size=8)
    data['whashDb4'] = imagehash.whash(img, mode='db4')
    print(data)
    return data
