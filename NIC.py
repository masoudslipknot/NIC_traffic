import socket
import Packing


def main():

 # socket module is used for capturing the packets
 # create an INET, raw socket for windows
 s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
 s.bind(("192.168.242.1",0))
 s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
 s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

# In this section we receive the packets
 while True:
    # In this section we capture evey packets and try to extract information
    currPacket = s.recvfrom(65565)
    unpack = Packing.unpack() # Extracting packets

    data = unpack.ip_header(currPacket[0][14:34])

    print("data is",data)


if __name__ == '__main__':
    main()