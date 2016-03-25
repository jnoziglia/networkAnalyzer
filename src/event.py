import subprocess as sub
import re



class Event(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.src = ''
        self.src_port = 0
        self.dst = ''
        self.dst_port = 0
        self.protocol = ''
        self.length = 0
        self.id = 0