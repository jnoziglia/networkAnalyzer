import subprocess as sub
import re

class Event(object):
    def __init__(self, timestamp, src, dst, protocol):
        self.timestamp = timestamp
        self.src = src
        self.dst = dst
        self.protocol = protocol
