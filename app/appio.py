
import Crypto
from Crypto.Hash import MD5
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode, b64encode
from Crypto.Random import get_random_bytes
import json
import asyncio
import websockets
from aiozeroconf import ServiceBrowser, Zeroconf
import time
import click
import ast

from websockets import WebSocketServer
from singletonInfoCache import SingletonInfoCache
tasks = []


def format_encryption_msg(payload, api_key, data):

    payload["selfApikey"] = "123"
    # see https://github.com/itead/Sonoff_Devices_DIY_Tools/issues/5)
    iv = generate_iv()
    payload["iv"] = b64encode(iv).decode("utf-8")
    payload["encrypt"] = True
    payload["data"] = encrypt(
        json.dumps(data, separators=(",", ":")), iv, api_key
    )


def format_encryption_txt(properties, data, api_key):

    properties["encrypt"] = True

    iv = generate_iv()
    properties["iv"] = b64encode(iv).decode("utf-8")

    return encrypt(data, iv, api_key)


def encrypt(data_element, iv, api_key):

    api_key = bytes(api_key, "utf-8")
    plaintext = bytes(data_element, "utf-8")

    hash = MD5.new()
    hash.update(api_key)
    key = hash.digest()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    padded = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded)
    encoded = b64encode(ciphertext)

    return encoded.decode("utf-8")


def decrypt(data_element, iv, api_key):

    api_key = bytes(api_key, "utf-8")
    encoded = data_element

    hash = MD5.new()
    hash.update(api_key)
    key = hash.digest()
    cipher = AES.new(key, AES.MODE_CBC,b64decode(iv))
    ciphertext = b64decode(encoded)
    padded = cipher.decrypt(ciphertext)
    plaintext = unpad(padded, AES.block_size)

    return plaintext




def socket_router(infoSingleton : SingletonInfoCache ,payload :str, start_server):
    intit:str = payload[1:3]
    if intit == "--":
        device_info :str= payload.replace("--","").replace("'","")
        infoSingleton.parse_device_info_string(device_info)
        


async def controller():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("connected")

        payload : str = await websocket.recv()
        data = payload.split("*")
        data_element:str = data[0]
        iv:str = data[1]
        api_key:str = data[2]
        plaintext = decrypt(data_element, iv, api_key)
        await websocket.send(plaintext)
        


if __name__ == "__main__":
    asyncio.get_event_loop().run_forever()
    
