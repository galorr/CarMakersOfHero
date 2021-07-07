class Command:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def toString(self):
        return "{" + f"command: {self.type}, value: {self.value}" + "}"