class SingletonInfoCache(object):
    """
    docstring
    """
    __instance = None
    @staticmethod
    def getInstance():
        if SingletonInfoCache.__instance == None:
            SingletonInfoCache()
        return SingletonInfoCache.__instance
    
    def parse_device_info_string(self ,payload :str):
        data = payload[:len(payload)- 1]
        args_list = data.split("*")
        for info in args_list:
            deviceId_apiKey = info.split(":")
            device_id = deviceId_apiKey[0]
            api_key = deviceId_apiKey[1]
            self.info_dict[device_id] = api_key

    def __init__(self):
        if SingletonInfoCache.__instance != None:
            raise Exception("Singleton class has been init")
        else:
            SingletonInfoCache.__instance = self
            self.info_dict = {}
    def getInfoDict(self)->dict:
        return self.info_dict;
            
