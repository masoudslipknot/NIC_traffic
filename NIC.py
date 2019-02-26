import socket
import Packing


def main():
#create an INET, raw socket
 s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
 s.bind(("192.168.242.1",0))
 s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
 s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

# receive a packet
 while True:
    # print output on terminal
    currPacket = s.recvfrom(65565)
    unpack = Packing.unpack()

    data = unpack.ip_header( currPacket[0][14:34])

    print("data is",data)


if __name__ == '__main__':
    main()