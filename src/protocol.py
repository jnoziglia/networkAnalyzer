from packet import *

class Protocol:
    def __init__(self, name, bytes_sent):
        self.name = name
        self.packets = []
        self.bytes_sent = bytes_sent

    def process_packet(self, event, length):
        if (event.src_port == '' or event.dst_port == '' or event.t_protocol == 'ICMP'):
            packet = Packet(0, 0, length)
            self.packets.append(packet)
        else:
            packet_list = [x for x in self.packets if (x.src_port == event.src_port and x.dst_port == event.dst_port)]
            if packet_list:
                packet = packet_list[0]
                packet.size += length
            else:
                packet = Packet(event.src_port, event.dst_port, length)
                self.packets.append(packet)
