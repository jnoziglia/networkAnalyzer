import subprocess as sub
import re
import sys
sys.path.append('./')
from event import *
from yattag import Doc


class Analyzer(object):
    regex_ip_1 = r'IP (?:\(tos \w*, ttl \d*, id (?P<id>\d*), offset (?P<offset>\d*), flags \[\w*\], proto (?P<transport_protocol>\w*) (?:\(\d*\))?, length (?P<length>\d*)\))'
    # regex_ip_2 = r'(?P<IP1>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<Port1>\d+)? > (?P<IP2>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<Port2>\d+)?: (?P<transport_protocol>TCP|UDP|ICMP)'
    regex_timestamp = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>IP|ARP)'
    reg_ip_1 = re.compile(regex_ip_1)
    reg_timestamp = re.compile(regex_timestamp)
    events = []

    # sub.call("./create_capture.sh")
    doc, tag, text = Doc().tagtext()
    events_empty = 1
    p = sub.Popen(('sudo', 'tcpdump', 'ip', '-l', '-nnv', '-r', '../output'), stdout=sub.PIPE)
    for line in iter(p.stdout.readline, b''):
        m = reg_timestamp.match(line.decode())
        if m:
            if events_empty == 0:
                events.append(event)
            events_empty = 0
            event = Event(m.group('timestamp'), m.group('protocol'))
            m = reg_ip_1.search(line.decode())
            if m:
                event.id = m.group('id')
                event.t_protocol = m.group('transport_protocol')
                event.length = m.group('length')

    for event in events:
        with tag ('tr'):
            with tag('td'):
                text(event.timestamp)
            with tag('td'):
                text(event.dst)
            with tag('td'):
                text(event.dst_port)
            with tag('td'):
                text(event.src)
            with tag('td'):
                text(event.src_port)
            with tag('td'):
                text(event.t_protocol)
            with tag('td'):
                text(event.length)
            with tag('td'):
                text(event.id)
    code = doc.getvalue()
    with open('report.html') as f:
        file_str = f.read()
    new_file_str = file_str.format(code=code)
    with open('report.html', 'w') as f:
        f.write(file_str)

# if __name__ == "__main__":
#     Analyzer().main()
