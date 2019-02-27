
# NIC_traffic
<h2> Project Description:</h2>
In this project, I am planning to capture packets from a machine. Then capture packets will be parsed in order to acquire the proper results. We only process the *TCP*  and *UDP*  packets and others such as ICMP packets are labeled **Unknown**  </br>
<h3> How the process is done? </h3>
It is possible to use scapy for the whole project but, first, everything is coded here and we will pay attention to scapy after finishing our own packet sniffer.</br>
Since we are accessing the packets, it is needed to run the code with Sudo in order to receive the permission.</br>
For capturing the pockets I am using the socket module. Python programming language socket module provides us the facility to play with network concept.</br>
There is a small difference in Python socket module codes based on operating systems. </br>
Here we use it for Linux. So, we have to run the python file with sudo.
<h3> Parsing process: </h3>
According to the Ethernet Frame Format Diagram,  I am going to extract the demanded properties. I have to pass an argument that going to represent field types, we want to extract in (struct.unpack) function.  The IP, TCP, UDP etc header information will be saved in a struct.</br>
An example of formats: </br>

` storeobj = struct.unpack("!BBHHHBBH4s4s", data) ` </br>

Here! means that receiver always receive data in reverse order. H is for Unsigned Short data types and number is for the times to use.</br>

In these line of codes, we determine which kind of IP packets we have: </br>

`if proto == '80': ` </br>
      `  ip_proto = 'IPv4'` </br>
   ` elif proto == '86': `  </br>
       ` ip_proto = 'ARP' `  </br>
  `  elif proto == '86DD': `  </br>
      `  ip_proto = 'IPv6' ` </br>
  `  else: </br>
        ip_proto = proto </br>
        `

We have a number when we parse it we can figure out which kind of packets we have. If it is 6 then its TCP, or its 17 we have UDP.
Then we extract the source and destination Ip. Source port and destination port are selected when it is define we have TCP or UDP.</br>

For every packet that we parce, the demanded information will be stored in dictionary for making the flow.
As I found out on internet,  traffic flow, packet flow or network flow is a sequence of packets from a source computer to a destination, which may be another host, a multicast group, or a broadcast domain. We need to group these packets and calculate the features which are demanded.</br>
To make the flow of packets, I check if the source IP and DestIP are the same or not. IF they are the same we store packets in lists and we calculate the duration of it and number bytes which it sends.</br>


After that, We will write all the information that we have into the CSV_file.

Still working on the project.

