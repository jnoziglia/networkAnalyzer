from protocol import *

class Host:
    def __init__(self, ip):
        self.ip = ip
        self.total_bytes_received = 0
        self.bytes_sent = 0
        self.hosts = []
        self.protocols = []

    def process_host(self, event, length):
        host_list = [x for x in self.hosts if x.ip == event.src]
        if host_list:
            host = host_list[0]
            host.process_protocol(event, length)
        else:
            host = Host(event.src)
            protocol = Protocol(event.t_protocol, length)
            packet = Packet(event.src_port, event.dst_port, length)
            protocol.packets.append(packet)
            host.protocols.append(protocol)
            self.hosts.append(host)
        host.bytes_sent += length

    def process_protocol(self, event, length):
        protocol_list = [x for x in self.protocols if x.name == event.t_protocol]
        if protocol_list:
            protocol = protocol_list[0]
            protocol.process_packet(event, length)
            protocol.bytes_sent += length
        else:
            protocol = Protocol(event.t_protocol, length)
            packet = Packet(event.src_port, event.dst_port, length)
            protocol.packets.append(packet)
            self.protocols.append(protocol)
