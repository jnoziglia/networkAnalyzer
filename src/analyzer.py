import subprocess as sub
import re
import sys
import textwrap
sys.path.append('./')
from event import *
from yattag import Doc
from yattag import indent


class Analyzer(object):
    regex_ip_1 = r'IP (?:\(tos \w*, ttl \d*, id (?P<id>\d*), offset (?P<offset>\d*), flags \[\w*\], proto (?P<transport_protocol>\w*) (?:\(\d*\))?, length (?P<length>\d*)\))'
    regex_ip_2 = r'(?P<src>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<src_port>\d*) > (?P<dst>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<dst_port>\d*): (?P<protocol>\w+)'
    regex_timestamp = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>IP|ARP)'
    regex_port_error = r'port \w+ unreachable'
    reg_ip_1 = re.compile(regex_ip_1)
    reg_ip_2 = re.compile(regex_ip_2)
    reg_timestamp = re.compile(regex_timestamp)
    reg_port_error = re.compile(regex_port_error)
    events = []

    # sub.call("./create_capture.sh")
    doc, tag, text = Doc().tagtext()
    add_event = 0
    p = sub.Popen(('sudo', 'tcpdump', 'ip', '-l', '-nnv', '-r', '../output'), stdout=sub.PIPE)
    for line in iter(p.stdout.readline, b''):
        m = reg_timestamp.match(line.decode())
        if m:
            if add_event == 1:
                events.append(event)
            add_event = 1
            event = Event(m.group('timestamp'), m.group('protocol'))
            m = reg_ip_1.search(line.decode())
            if m:
                event.id = m.group('id')
                event.t_protocol = m.group('transport_protocol')
                event.length = m.group('length')
        else:
            m = reg_ip_2.search(line.decode())
            if m:
                event.src = m.group('src')
                event.src_port = m.group('src_port')
                event.dst = m.group('dst')
                event.dst_port = m.group('dst_port')
            m = reg_port_error.search(line.decode())
            if m:
                add_event = 0

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
    code = indent(doc.getvalue())
    with open('../report.html') as f:
        file_str = f.read()
    new_file_str = file_str.format(code=code)
    with open('report.html', 'w') as f:
        f.write(new_file_str)

# if __name__ == "__main__":
#     Analyzer().main()
