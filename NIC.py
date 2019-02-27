#!/usr/bin/python

import struct
import socket
import requests
import Packing
import csv
import time






def UDP_packets(data):
    # Here udp packets are parced.
    src_port, dest_port, packet_length = struct.unpack('!HHH', data[:6])
    return data[8:],src_port, dest_port


def TCP_packets(data):
    # Here tcp packets are parced.
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

    return data[tcp_header_length:],src_port, dest_port,flag_ack


def Packets(data, protocol):
    # classifiying different protocols
    application_packet = None
    src_port=0
    dest_port=0
    flg_ack=0
    if protocol == 'TCP':
        application_packet,src_port, dest_port, flg_ack = TCP_packets(data)
    elif protocol == 'UDP':
        application_packet,src_port, dest_port = UDP_packets(data)

    return application_packet,protocol,src_port, dest_port,flg_ack




# *******Main************
def main():
    # Make the socket connection
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
      with open("results.csv", 'a') as csvfile:
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




            application_packet,protocol,src_port, dest_port,flg_ack = Packets(packet[ip_header_length:], transport_proto)
            Duration = 0
            Tcp_flow = []
            if protocol=='TCP':
                start_time = time.time()
                if flg_ack!=1:
                    Tcp_flow.append(application_packet)
                elif flg_ack==1:
                  end = time.time()
                  Duration = end - start_time

            #In this part of code, we write on the CSV file
            writer = csv.writer(csvfile)
            if Duration!=0 and protocol=='TCP':
             finalstr = str(src_ip)+ ","+ str(dest_ip)+","+str(src_port)+","+str(dest_port)+","+protocol+str(Duration)
             writer.writerow(finalstr)
            elif protocol=='UDP':
                finalstr = str(src_ip) + "," + str(dest_ip) + "," + str(src_port) + "," + str( dest_port) + "," + protocol
                writer.writerow(finalstr)




            csvfile.close()



main()