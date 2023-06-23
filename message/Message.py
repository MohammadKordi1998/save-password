from message.IMessage import IMessage


class Message(IMessage):
    def message(self):
        result = {
            'response': self.response,
            'status_code': self.status_code,
            'message': self.return_message,
        }
        return result


