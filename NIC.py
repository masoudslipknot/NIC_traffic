#!/usr/bin/python

import struct
import socket
import requests
import Packing






def parse_UDP(data):
    src_port, dest_port, packet_length = struct.unpack('!HHH', data[:6])
    print('---------UDP Packet---------')
    print("Source_Port:", src_port, "\tDestination_Port:", dest_port,
          "\nPacket_Length:", packet_length)
    return data[8:],src_port, dest_port


def parse_TCP(data):
    src_port, dest_port, seq, ack, offset_flags = struct.unpack('!HHLLH', data[:14])

    # Extract first 4 bits and multiply by 4 to get the header length.
    tcp_header_length = (offset_flags >> 12) * 4

    # Extract all the flags starting at positon 5 from left and so and with 2^5
    flag_urg = (offset_flags & 32) >> 5
    flag_ack = (offset_flags & 16) >> 4
    flag_psh = (offset_flags & 8) >> 3
    flag_rst = (offset_flags & 4) >> 2
    flag_syn = (offset_flags & 2) >> 1
    flag_fin = offset_flags & 1

    print('---------TCP Packet---------')
    print("Source_Port:", src_port, "\tDestination_Port:", dest_port,
          "\nHeader_Length:", tcp_header_length)


    return data[tcp_header_length:],src_port, dest_port


def parse_transport_packet(data, protocol):
    application_packet = None
    if protocol == 'TCP':
        application_packet,src_port, dest_port = parse_TCP(data)
    elif protocol == 'UDP':
        application_packet,src_port, dest_port = parse_UDP(data)

    return application_packet,protocol,src_port, dest_port




# *******Main************
def main():
    # Make the socket connection
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
      with open("results.csv", 'w') as csvfile:
        # Receive the ethernet frame
        payload, addr = conn.recvfrom(65535)
        packet, ip_protocol = Packing.parse_frame(payload)
        if ip_protocol == 'IPv4':
            # Contains IP version and Header Length
            first_byte = packet[0]

            # First 4 bits is version
            ip_version = first_byte >> 4
            # Next 4 bits is header_length
            ip_header_length = (first_byte & 15) * 4

            ttl, proto, src, dest = struct.unpack('!8xBB2x4s4s', packet[:20])

            # Ip address in string format..
            src_ip = Packing.get_ipv4(src)
            dest_ip = Packing.get_ipv4(dest)

            if proto == 1:
                transport_proto = 'ICMP'
            elif proto == 6:
                transport_proto = 'TCP'
            elif proto == 17:
                transport_proto = 'UDP'
            else:
                transport_proto = 'Unknown Protocol Field = ' + str(proto)


            print("Source_IP:", src_ip, "\tDestination_IP:", dest_ip,
                  "\nTTL:", ttl, 'hops\t', '\tTransport_Protocol:', transport_proto)

            application_packet = parse_transport_packet(packet[ip_header_length:], transport_proto)


main()