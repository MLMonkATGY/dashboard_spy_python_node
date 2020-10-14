from socketIO_client_nexus import SocketIO, BaseNamespace
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode, b64encode
from Crypto.Random import get_random_bytes


def decryption(data):
    print('welcome received', data)
    payloadSlice = data.split("*")
    decrypted = str(
        decrypt(payloadSlice[2], payloadSlice[1], payloadSlice[0]), "utf8")
    socketIO.emit("status_update", decrypted)


def keep_alive(data):
    socketIO.emit("gateway_status", "alive")


def decrypt(data_element, iv, api_key):

    api_key = bytes(api_key, "utf-8")
    encoded = data_element

    hash = MD5.new()
    hash.update(api_key)
    key = hash.digest()

    cipher = AES.new(key, AES.MODE_CBC, iv=b64decode(iv))
    ciphertext = b64decode(encoded)
    padded = cipher.decrypt(ciphertext)
    plaintext = unpad(padded, AES.block_size)

    return plaintext


socketIO = SocketIO('http://localhost:7878', verify=True,
                    wait_for_connection=True)

socketIO.on('decrypt', decryption)
socketIO.on('alive', keep_alive)

socketIO.wait()
