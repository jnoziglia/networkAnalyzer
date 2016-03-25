import subprocess as sub
import re
import sys

sys.path.append('./')
from event import *


class Analyzer:
    regex_ip_1 = r'IP (?:\(tos \w*, ttl \d*, id (?P<id>\d*), offset (?P<offset>\d*), flags \[\w*\], proto (?P<transport_protocol>\w*) (?:\(\d*\))?, length (?P<length>\d*)\))'
    # regex_ip_2 = r'(?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<Port1>\d+)? > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<Port2>\d+)?: (?P<transport_protocol>TCP|UDP|ICMP)'
    regex_timestamp = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>IP|ARP)'
    reg_ip_1 = re.compile(regex_ip_1)
    reg_timestamp = re.compile(regex_timestamp)
    events = []

    # sub.call("./create_capture.sh")

    # regex_string = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) IP (?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port1>\d+) > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.(?P<Port2>\d+): (?P<protocol>(?:TCP|UDP|ICMP))'

    # with open('outputtxt') as output:
    #     for line in output:
    #         m = reg.match(line)
    #         print line
    #         print m.group()

    def main(self):
        events_empty = 1
        p = sub.Popen(('sudo', 'tcpdump', '-l', '-nnv', '-r', '../output'), stdout=sub.PIPE)
        for line in iter(p.stdout.readline, b''):
            m = Analyzer.reg_timestamp.match(line)
            if m:
                if events_empty == 0:
                    Analyzer.events.append(event)
                events_empty = 0
                event = Event(m.group('timestamp'))
                m = Analyzer.reg_ip_1.match(line)
                if m:
                    event.id = m.group('id')
                    event.protocol = m.group('protocol')
                    event.length = m.group('length')

        for event in self.events:
            print(event.src)
            print(event.timestamp)

    if __name__ == "__main__":
        main()
