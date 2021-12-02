import json
from nacl import encoding
import nacl.utils
from nacl.public import Box
from NaClDSEncoder import NaClDSEncoder

def show(message):
    print(message)
    input("Continue...")


dsenc = NaClDSEncoder()
dsenc.generate()

PrvKey = dsenc.encode_private_key(dsenc.private_key)
PubKey = dsenc.encode_public_key(dsenc.public_key)

boxed_keys = Box(PrvKey, PubKey)

message = "I am plain text"

show(message)

encoded_message = message.encode(encoding='UTF-8')

show(encoded_message)

encrypted_message = boxed_keys.encrypt(encoded_message, encoder=encoding.Base64Encoder)

show(encrypted_message)
show(encrypted_message.decode('UTF-8'))

decrypted_message = boxed_keys.decrypt(encrypted_message, encoder=encoding.Base64Encoder)

show(decrypted_message)

decoded_message = decrypted_message.decode(encoding='UTF-8')

show(decoded_message)
