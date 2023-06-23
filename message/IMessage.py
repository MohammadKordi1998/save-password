class IMessage:
    def __init__(self, response, status_code, return_message):
        self.response = response
        self.status_code = status_code
        self.return_message = return_message

    def message(self):
        raise Exception
