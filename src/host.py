class Host:
    def __init__(self, ip):
        self.ip = ip
        self.total_bytes_received = 0
        self.bytes_sent = 0
        self.hosts = []
        self.protocols = []

    def find_host(self, ip):
        list = [x for x in self.hosts if x.ip == ip]
        if list:
            return list[0]
        else:
            return None

    def find_protocol(self, name):
        list = [x for x in self.protocols if x.name == name]
        if list:
            return list[0]
        else:
            return None
