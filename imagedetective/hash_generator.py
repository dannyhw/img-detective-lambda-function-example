import imagehash
from PIL import Image

HASH_FUNCTIONS = {
    'ahash': lambda img: imagehash.average_hash(img, hash_size=8),
    'phash': lambda img: imagehash.phash(img, hash_size=8),
    'dhash': lambda img: imagehash.dhash(img, hash_size=8),
    'whash': lambda img: imagehash.whash(img, hash_size=8),
    'whashDb4': lambda img: imagehash.whash(img, mode='db4')
}


def get_image_hashes(path_to_file, hash_types):
    image_hashes = {}
    with Image.open(path_to_file) as img:
        for hash_type in hash_types:
            image_hashes[hash_type] = []
            this_hash = HASH_FUNCTIONS[hash_type](img).hash.tolist()
            for hashrow in this_hash:
                image_hashes[hash_type].extend(hashrow)

    return image_hashes
