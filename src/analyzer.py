import subprocess as sub
import re
import sys
from event import *
from host import *
from protocol import *
from yattag import Doc
from yattag import indent
sys.path.append('./')

# Global variables
# Regular expressions (both strings and compiled expressions) to parse TCPDump output
# Regex including timestamp. First line of every packet
regex_timestamp = r'(?P<timestamp>(?:\d{1,2}\:){2}\d{1,2}\.\d{1,6}) (?P<protocol>\w+)'
# First line of every IP datagram
regex_ip_1 = r'IP (?:\(tos \w*, ttl \d*, id (?P<id>\d*), offset (?P<offset>\d*), flags \[\w*\], proto (?P<transport_protocol>\w*) (?:\(\d*\))?, length (?P<length>\d*)\))'
# Second line of every IP datagram
regex_ip_2 = r'(?P<src>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<src_port>\d*) > (?P<dst>(?:\d{1,3}\.){3}\d{1,3})\.?(?P<dst_port>\d*): (?P<transport_protocol>\w+)'
# Port unreachable error. Packet should get discarded
regex_port_error = r'port \w+ unreachable'
# Regex to get length of TCP packet
regex_length = r'length (?P<length>\d+)'
# Compiled regexs
reg_ip_1 = re.compile(regex_ip_1)
reg_ip_2 = re.compile(regex_ip_2)
reg_length = re.compile(regex_length)
reg_timestamp = re.compile(regex_timestamp)
reg_port_error = re.compile(regex_port_error)
# List of all events logged
events = []
# List of terminals involved in the network
hosts = []


# Main class
class Analyzer(object):
    # Method to generate size in readable unit
    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.3f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.3f%s%s" % (num, 'Yi', suffix)

    # Method to generate a list of all logged events, in HTML
    @staticmethod
    def add_event_to_html(event, main_doc, main_tag, main_text):
        with main_tag('tr'):
            with main_tag('td'):
                main_text(event.timestamp)
            with main_tag('td'):
                main_text(event.dst)
            with main_tag('td'):
                main_text(event.dst_port)
            with main_tag('td'):
                main_text(event.src)
            with main_tag('td'):
                main_text(event.src_port)
            with main_tag('td'):
                main_text(event.t_protocol)
            with main_tag('td'):
                main_text(event.length)
            with main_tag('td'):
                main_text(event.id)

    # Method to generate a list of bytes received by each host, in HTML
    def generate_received_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('h1'):
            text('Amount of data transferred from each host')
        for host in hosts:
            with tag('div', klass="col-4"):
                with tag('h2'):
                    text(host.ip)
                with tag('p'):
                    text('Total Bytes Received: {}'.format(self.sizeof_fmt(host.total_bytes_received)))
                for src_host in host.hosts:
                    with tag('h4'):
                        text('Bytes received from {}'.format(src_host.ip))
                    with tag('p'):
                        text('Total: {}'.format(self.sizeof_fmt(src_host.bytes_sent)))
                    for protocol in src_host.protocols:
                        with tag('p'):
                            text('{}: {}'.format(protocol.name, self.sizeof_fmt(protocol.bytes_sent)))
                    with tag('p'):
                        text('--------------')
        with tag('div', style="clear:both"):
            text('')
        return indent(doc.getvalue())

    # Method to generate bar chart in HTML
    @staticmethod
    def generate_graph_html():
        doc, tag, text = Doc().tagtext()
        with tag('h1'):
            text('Percentage of data transferred from each host')
        for host in hosts:
            total_received = host.total_bytes_received
            with tag('h2'):
                text(host.ip)
            with tag('table', border="0", cellpadding="0", cellspacing="0", klass="bar-chart"):
                for src_host in host.hosts:
                    received = (src_host.bytes_sent / total_received) * 100
                    with tag('tr'):
                        with tag('td', valign="middle", align="left", klass="ip-address"):
                            text(src_host.ip)
                        with tag('td', valign="middle", align="left", klass="bar"):
                            with tag('div', style="width:{}%".format(received)):
                                text('{}%'.format(round(received, 3)))
        return indent(doc.getvalue())


    def generate_packets_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('h1'):
            text('Packets transferred from each host')
        for host in hosts:
            total_received = 0
            with tag('div', klass="col-4"):
                with tag('h2'):
                    text(host.ip)
                for src_host in host.hosts:
                    total_from_host = 0
                    with tag('h4'):
                        text('Packets received from {}'.format(src_host.ip))
                    for protocol in src_host.protocols:
                        with tag('h4'):
                            text('Protocol: {}'.format(protocol.name))
                        max_size = 0
                        min_size = -1
                        amount = len(protocol.packets)
                        for packet in protocol.packets:
                            if packet.size > max_size:
                                max_size = packet.size
                            if packet.size < min_size or min_size == -1:
                                min_size = packet.size
                        total_received += amount
                        total_from_host += amount
                        with tag('p'):
                            text('Packets: {}'.format(amount))
                        with tag('p'):
                            text('Minimum size packet: {}'.format(self.sizeof_fmt(min_size)))
                        with tag('p'):
                            text('Maximum size packet: {}'.format(self.sizeof_fmt(max_size)))
                    with tag('p'):
                        with tag('strong'):
                            text('Total from {}: {} packets'.format(src_host.ip, total_from_host))
                    with tag('p'):
                        text('--------------')
                with tag('p'):
                    text('Total Received: {}'.format(total_received))
        with tag('div', style="clear:both"):
            text('')
        return indent(doc.getvalue())

    # Returns host in hosts list, filtered by IP
    @staticmethod
    def process_host(event, length):
        host_list = [x for x in hosts if x.ip == event.dst]
        if host_list:
            host = host_list[0]
            host.process_host(event, length)
        else:
            host = Host(event.dst)
            src_host = Host(event.src)
            src_host.bytes_sent += length
            protocol = Protocol(event.t_protocol, length)
            packet = Packet(event.src_port, event.dst_port, length)
            protocol.packets.append(packet)
            src_host.protocols.append(protocol)
            host.hosts.append(src_host)
            hosts.append(host)
        host.total_bytes_received += length

    # Loops through dump file generated by TCPDump, parses each line and creates objects with the information extracted
    # Returns HTML code of complete list of events
    def process_dump_file(self, p):
        add_event = 0
        main_doc, main_tag, main_text = Doc().tagtext()
        for line in iter(p.stdout.readline, b''):
            m = reg_timestamp.match(line.decode())
            if m:
                if add_event == 1:
                    events.append(event)
                    self.add_event_to_html(event, main_doc, main_tag, main_text)
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
                        self.process_host(event, length)
                m = reg_port_error.search(line.decode())
                if m:
                    add_event = 0
        return indent(main_doc.getvalue())

    # Main function, executed when ran from terminal
    def main(self, dump_file):
        p = sub.Popen(('sudo', 'tcpdump', 'ip', '-l', '-nnv', '-r', dump_file), stdout=sub.PIPE)
        events_html = self.process_dump_file(p)
        received_html = self.generate_received_html()
        graph_html = self.generate_graph_html()
        packets_html = self.generate_packets_html()
        with open('../reports/report_template.html') as f:
            file_str = f.read()
        new_file_str = file_str.format(events_html='', received_html=received_html, graph_html=graph_html, packets_html=packets_html)
        extended_file_str = file_str.format(events_html=events_html, received_html=received_html, graph_html=graph_html, packets_html=packets_html)
        with open('../reports/extended_report.html', 'w') as f:
            f.write(extended_file_str)
        with open('../reports/report.html', 'w') as f:
            f.write(new_file_str)

if __name__ == "__main__":
    Analyzer().main(sys.argv[1])
