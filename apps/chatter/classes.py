class Message(object):
    def __init__(self, command, **kwargs):
        self.command = command
        self.entry = kwargs.get('entry', None)
        self.entries = kwargs.get('entries', None)
        self.error = kwargs.get('error', None)
        self.success = kwargs.get('success', None)