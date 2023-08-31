from querystar.client import ClientConnection

_client_connection: ClientConnection = ClientConnection()


class Counter:
    def __init__(self):
        self.count = 0
        self.status = 'only outside'

    def increment(self):
        self.count += 1
        print(f'a count of {self.count} with status {self.status}')

    def update_status(self, status):
        self.status = status


_counter = Counter()
