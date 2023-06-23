from required.IRequired import IRequired


class Required(IRequired):
    def required(self):
        dict_required = {}
        for key, value in self.date.items():
            if not value:
                dict_required[key] = self.error_message[key]

        return dict_required
