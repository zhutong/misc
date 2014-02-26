'''
    Raw sockets on Linux
     
    Silver Moon (m00n.silv3r@gmail.com)
'''

# some imports
import socket, sys
import time
from struct import *

# checksum functions needed for calculation checksum
def checksum(msg):
    s = 0

    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i + 1]) << 8 )
        s = s + w

    s = (s >> 16) + (s & 0xffff);
    s = s + (s >> 16);

    #complement and mask to 4 byte short
    s = ~s & 0xffff

    return s


# ip header fields
def get_ip_header(ip_saddr, ip_daddr, ip_proto, ip_tos=0, ip_id=0, ip_ttl=64):
    ip_tot_len = 0  # kernel will fill the correct total length
    ip_frag_off = 0
    ip_proto = ip_proto
    ip_check = 0  # kernel will fill the correct checksum

    ip_ihl_ver = (4 << 4) + 5

    return pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check,
                ip_saddr, ip_daddr)


# tcp header fields
def get_tcp_header():
    tcp_source = 888  # source port
    tcp_dest = 888  # destination port
    tcp_seq = 454
    tcp_ack_seq = 0
    tcp_doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes
    #tcp flags
    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    tcp_window = socket.htons(5840)  # maximum allowed window size
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

    # the ! in the pack format string means network order
    tcp_header = pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window,
                      tcp_check, tcp_urg_ptr)

    tcp_check = checksum(tcp_header + user_data)

    # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
    return pack('!HHLLBBH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack(
        'H', tcp_check) + pack('!H', tcp_urg_ptr)


def get_packet(ip_header, l4_header, user_data):
    return ''.join((ip_header, l4_header, user_data))


def get_socket():
    """
    create a raw socket
    """
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        return


s = get_socket()
if s is None:
    sys.exit()

user_data = 'Hello, how are you'
dest_ip = '10.140.0.140'
ip_sadd = socket.inet_aton('10.124.1.97')
ip_dadd = socket.inet_aton(dest_ip)

start = time.time()
for i in range(10000):
    ip_header = get_ip_header(ip_sadd, ip_dadd, socket.IPPROTO_TCP, ip_tos=5, ip_id=i%65000)
    tcp_header = get_tcp_header()
    packet = ''.join((ip_header, tcp_header, user_data))
    s.sendto(packet, (dest_ip, 0))
print '%6f' % (time.time() - start)
# print ':'.join((hex(ord(c)) for c in packet))