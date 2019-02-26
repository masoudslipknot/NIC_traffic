
# NIC_traffic
<h2> Project Description:</h2>
In this project, I am planning to capture packets from a machine. Then capture packets will be parsed in order to acquire the proper results.</br>
<h3> How the process is done? </h3>
It is possibl to use scapy for the whole project but, first every thing is coded here and we will pay attention to scapy after finishing our own packet sniffer.</br>
For capturing the pockets I am using the socket module. Python programming language socket module provides us the facility to play with network concept.</br>
There is a small difference in Python socket module codes based on operating systems. </br>
Here we use it for Linux. So, we have to run the python file with sudo.
<h3> Parcing process: </h3>
According to the Ethernet Frame Format Diagram,  I am going to extract the demanded properties. I have to pass an argument that going to represent field types, we want to extract in (struct.unpack) function.  The IP, TCP, UDP etc header information will be saved in a struct.</br>
An example of formats: </br>

` storeobj = struct.unpack("!BBHHHBBH4s4s", data) ` </br>

Here the ! means that receiver always receive data in reverse order. H is for Unsigned Short data types and number is for the times to use.</br>
We have a number when we parce it we can figure out which kind of packets we have. If it is 6 then its TCP, or its 17 we have UDP.
Then we extract the sourceip and destination Ip. Source port and destination port are selected when it is define we have TCP or UDP.</br>

After that, We will write all the information that we have in to the CSV_file.

Still working on the project.

