class IRequired:
    def __init__(self, date=dict, error_message=dict):
        self.date = date
        self.error_message = error_message

    def required(self):
        raise Exception
