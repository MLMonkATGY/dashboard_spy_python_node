from socketIO_client_nexus import SocketIO, BaseNamespace
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode, b64encode
from Crypto.Random import get_random_bytes


def decryption(data):
    # print('welcome received', data)
    # payloadSlice = data.split("*")
    decrypted = str(
        decrypt(data["data1"], data["iv"], data["apiKey"]), "utf8")
    socketIO.emit("generic_event", {
        "event": "decryption_done",
        "payload": decrypted
    })
    print(decrypted)


def keep_alive(data):
    socketIO.emit("generic_event", alive_payload)


def debug(data):
    print(data)
    socketIO.emit("debug_receive", data)


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
alive_payload = {"event": "gateway_status", "payload": {
    "client": "asdfas",
    "status": "alive",
    "broadcastFunction": "decrypt"
}
}
socketIO.on('decrypt', decryption)
socketIO.on('alive', keep_alive)
socketIO.on('debug', debug)
socketIO.wait()
