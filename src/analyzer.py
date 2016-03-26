import subprocess as sub
import re
import sys
import random
import textwrap
sys.path.append('./')
from event import *
from host import *
from protocol import *
from yattag import Doc
from yattag import indent

regex_ip_1 = r'IP (?:\(tos \w*, ttl \d*, id (?P<id>\d*), offset (?P<offset>\d*), flags \[\w*\], proto (?P<transport_protocol>\w*) (?:\(\d*\))?, length (?P<length>\d*)\))'
regex_ip_2 = r'(?P<src>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<src_port>\d*) > (?P<dst>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<dst_port>\d*): (?P<transport_protocol>\w+)'
regex_timestamp = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>\w+)'
regex_port_error = r'port \w+ unreachable'
regex_length = r'length (?P<length>\d+)'
reg_ip_1 = re.compile(regex_ip_1)
reg_ip_2 = re.compile(regex_ip_2)
reg_length = re.compile(regex_length)
reg_timestamp = re.compile(regex_timestamp)
reg_port_error = re.compile(regex_port_error)
events = []
hosts = []
add_event = 0


class Analyzer(object):
    def generate_html(self):
        doc, tag, text = Doc().tagtext()
        for event in events:
            with tag('tr'):
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
        with tag('h2'):
            text('Resultados por IP')
        for host in hosts:
            with tag('h3'):
                text(host.ip)
            with tag('p'):
                text('Total Bytes Received: {}b'.format(host.total_bytes_received))
            for src_host in host.hosts:
                with tag('h4'):
                    text('Bytes received from {}'.format(src_host.ip))
                with tag('p'):
                    text('Total: {}b'.format(src_host.ip, src_host.bytes_sent))
                for protocol in src_host.protocols:
                    with tag('p'):
                        text('{}: {}b'.format(protocol.name, protocol.bytes_sent))

        return indent(doc.getvalue())

    def find_host(self, ip):
        list = [x for x in hosts if x.ip == ip]
        if list:
            return list[0]
        else:
            return None

    def main(self):
        # sub.call("./create_capture.sh")
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
                    m = reg_length.search(line.decode())
                    if m and m.group('length') != 0:
                        length = int(m.group('length'))
                        host = self.find_host(event.dst)
                        if host:
                            src_host = host.find_host(event.src)
                            if src_host:
                                protocol = src_host.find_protocol(event.t_protocol)
                                if protocol:
                                    protocol.bytes_sent = protocol.bytes_sent + length
                                else:
                                    protocol = Protocol(event.t_protocol, length)
                                    src_host.protocols.append(protocol)
                            else:
                                src_host = Host(event.src)
                                protocol = Protocol(event.t_protocol, length)
                                src_host.protocols.append(protocol)
                                src_host.bytes_sent = src_host.bytes_sent + length
                                host.hosts.append(src_host)
                        else:
                            host = Host(event.dst)
                            src_host = Host(event.src)
                            protocol = Protocol(event.t_protocol, length)
                            src_host.protocols.append(protocol)
                            host.hosts.append(src_host)
                            hosts.append(host)
                        host.total_bytes_received = host.total_bytes_received + length
                m = reg_port_error.search(line.decode())
                if m:
                    add_event = 0

        code = self.generate_html()
        with open('./report_template.html') as f:
            file_str = f.read()
        new_file_str = file_str.format(code=code)
        with open('report.html', 'w') as f:
            f.write(new_file_str)

        for host in hosts:
            print (host.ip)
            print (host.total_bytes_received)
            for src in host.hosts:
                print(src.ip)
                for protocol in src.protocols:
                    print (protocol.name)
                    print (protocol.bytes_sent)

if __name__ == "__main__":
    Analyzer().main()
