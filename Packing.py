import struct
import socket
import binascii

def get_mac_addr(bytes_addr):
    # it is for printing the mac address
    bytes_str = map("{:02x}".format, bytes_addr)
    return ':'.join(bytes_str).upper()


def get_ipv4(addr):
    # It is defined for printing the ip address
    return '.'.join(map(str, addr))

def parse_frame(frame):
    #This method is used for parsing the ethernet
    eth_len = 14
    eth_header = frame[:eth_len]
    eth_data = frame[eth_len:]
    dest_mac, src_mac, proto_field1, proto_field2 = struct.unpack('!6s6scc', eth_header)
    dest_mac = get_mac_addr(dest_mac)
    src_mac = get_mac_addr(src_mac)

    # proto is of the form b'\x08\x00'
    # print(proto_field1+proto_field2)
    proto1 = ''.join(map(str, proto_field1))
    proto2 = ''.join(map(str, proto_field2))
    proto = proto1 + proto2
    # print(proto)
    if proto == '80':
        ip_proto = 'IPv4'
    elif proto == '86':
        ip_proto = 'ARP'
    elif proto == '86DD':
        ip_proto = 'IPv6'
    else:
        ip_proto = proto
    return eth_data, ip_proto