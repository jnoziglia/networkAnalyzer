import subprocess as sub
import re

class Event(object):
    def __init__(self, timestamp, src, src_port, dst, dst_port, protocol):
        self.timestamp = timestamp
        self.src = src
        self.src_port = src_port
        self.dst = dst
        self.dst_port = dst_port
        self.protocol = protocol
