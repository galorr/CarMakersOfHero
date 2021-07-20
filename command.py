import json

class Command:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def initFromJson(self, message):
        self.__dict__ = json.dumps(message)
        #self.__dict__ = json.loads(message)

    def equal(self, command):
        if command == None:
            return self == None
        else:
            return self.type == command.type and self.value == command.value
