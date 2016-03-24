import subprocess as sub
import re
import sys

sys.path.append('./')
from event import *

regex_layer_3 = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<proto>(?:IP|ARP))'
regex_ip_1 = r'IP (?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>IP|ARP)'
# regex_ip_2 = r'(?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<Port1>\d+)? > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<Port2>\d+)?: (?P<transport_protocol>TCP|UDP|ICMP)'
regex_timestamp = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>IP|ARP)'
events = []


class Analyzer:
    def process_ip(self, line):
        reg = re.compile(regex_ip)
        m = reg.match(line)
        event = Event(m.group('timestamp'), m.group('IP1'), m.group('IP2'), m.group('protocol'))
        events.append(event)

    # sub.call("./create_capture.sh")
    p = sub.Popen(('sudo', 'tcpdump', '-l', '-nnv', '-r', '../output'), stdout=sub.PIPE)

    # regex_string = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?P<protocol>(?:TCP|UDP|ICMP))'

    reg = re.compile(regex_layer_3)

    # with open('outputtxt') as output:
    #     for line in output:
    #         m = reg.match(line)
    #         print line
    #         print m.group()

    for line in iter(p.stdout.readline, b''):
        m = reg.match(line)
        if m.group('proto') == 'IP':
            process_ip(line)

    for event in events:
        print(event.src)
        print(event.timestamp)
