class Packet:
    def __init__(self, src_port, dst_port, size):
        self.src_port = src_port
        self.dst_port = dst_port
        self.size = size