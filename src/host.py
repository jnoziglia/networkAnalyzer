class Host:
    def __init__(self, ip):
        self.ip = ip
        self.total_bytes_received = 0
        self.bytes_sent = 0
        self.hosts = []
        self.protocols = []
        self.color = ''

    def find_host(self, ip):
        host_list = [x for x in self.hosts if x.ip == ip]
        if host_list:
            return host_list[0]
        else:
            return None

    def find_protocol(self, name):
        protocol_list = [x for x in self.protocols if x.name == name]
        if protocol_list:
            return protocol_list[0]
        else:
            return None
