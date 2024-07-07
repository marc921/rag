from hashlib import sha256

def hash_array(array):
    # Convert the list to a tuple because tuples are immutable and hashable
    array_tuple = tuple(array)

    # Initialize a hash object
    hash_object = sha256(str(array_tuple).encode())

    # Get the hexadecimal digest of the hash
    hex_dig = hash_object.hexdigest()

    return hex_dig