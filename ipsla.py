__author__ = 'zhutong'

import struct
import time


def get_milliseconds():
    return int(time.time()) * 1000 % 4294967296


def convert_string(string):
    return ''.join([chr(eval('0x%s' % s)) for s in string.split(':')])


def pack_init_request(sn, dst_ip, udp_port, unknown):
    paras = 1, sn, 52, 4, 16, dst_ip, udp_port, unknown, 1, 28
    return struct.pack('!BBH4xHH4x4sHHHH24x', *paras)


def unpack_init_req(string):
    return struct.unpack('!xB14x4sHH28x', string)


def pack_init_response(init_request):
    return init_request[:3] + chr(24) + init_request[4:24]


def unpack_init_res(string):
    return struct.unpack('!BBH4xHH4x4BHH', string)


def pack_jitter_request(sn):
    paras = (2, 0, get_milliseconds(), 0, sn, 0, 0xabcdabcdabcdabcd, 0xabcdabcdabcdabcd)
    return struct.pack('!HHIIHH2Q', *paras)


def unpack_jitter_req(string):
    return struct.unpack('!HHIIHH2Q', string)


def unpack_jitter_request(string):
    return struct.unpack('!HHIIHH2Q', string)


def pack_jitter_response(request):
    p = unpack_jitter_req(request)
    paras = (p[0], p[1], p[2], get_milliseconds(), p[4], p[4], p[6], p[7])
    return struct.pack('!HHIIHH2Q', *paras)


def unpack_jitter_res(string):
    return struct.unpack('!HHIIHH2Q', string)


pcap_init_req = '''
01:b8:00:34:00:00:00:00:00:04:00:10:00:00:00:00:0a:4f:94:d3:27:10:1b:58:00:01:00:1c:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
01:b9:00:34:00:00:00:00:00:04:00:10:00:00:00:00:0a:4f:94:d3:27:10:1b:58:00:01:00:1c:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
01:ba:00:34:00:00:00:00:00:04:00:10:00:00:00:00:0a:4f:94:d3:27:10:1b:58:00:01:00:1c:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
01:64:00:34:00:00:00:00:00:04:00:10:00:00:00:00:c0:a8:dd:65:27:10:1b:58:00:01:00:1c:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00
'''.strip().splitlines()

pcap_init_res = '''
01:b8:00:18:00:00:00:00:00:04:00:10:00:00:00:00:0a:4f:94:d3:27:10:1b:58
01:b9:00:18:00:00:00:00:00:04:00:10:00:00:00:00:0a:4f:94:d3:27:10:1b:58
01:ba:00:18:00:00:00:00:00:04:00:10:00:00:00:00:0a:4f:94:d3:27:10:1b:58
'''.strip().splitlines()

pcap_req = '''
00:02:00:00:05:0b:02:a6:00:00:00:00:00:01:00:00:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
00:02:00:00:05:0b:02:b1:00:00:00:00:00:02:00:00:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
00:02:00:00:05:0b:77:d7:00:00:00:00:00:01:00:00:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
00:02:00:00:05:0b:77:e1:00:00:00:00:00:02:00:00:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
'''.strip().splitlines()

pcap_res = '''
00:02:00:00:05:0b:02:a6:04:e6:3f:10:00:01:00:01:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
00:02:00:00:05:0b:02:b1:04:e6:3f:1b:00:02:00:02:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
00:02:00:00:05:0b:77:d7:04:e6:b4:3e:00:01:00:01:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
00:02:00:01:05:0b:77:e1:04:e6:b4:47:00:02:00:02:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd:ab:cd
'''.strip().splitlines()

if __name__ == '__main__':
    import socket

    ip = '192.168.221.101'
    dst_ip = socket.inet_aton(ip)
    udp_port = 10000
    sn = 100
    unknown = 7000

    init_req = pack_init_request(sn, dst_ip, udp_port, unknown)
    init_res = pack_init_response(init_req)
    req = pack_jitter_request(sn)
    res = pack_jitter_response(req)

    # print unpack_init_req(init_req)
    # print unpack_init_res(init_res)
    # print unpack_jitter_req(req)[:6]
    # print unpack_jitter_res(res)[:6]
    #
    # for i in range(3):
    #     string = convert_string(pcap_init_req[i])
    #     print unpack_init_req(string)
    #     string = convert_string(pcap_init_res[i])
    #     print unpack_init_res(string)
    #
    for i in range(4):
        string = convert_string(pcap_req[i])
        print unpack_jitter_req(string)
        string = convert_string(pcap_res[i])
        print unpack_jitter_res(string)

    address = ('192.168.100.106', 10000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    start_time = time.time()
    while 1:
        message, ip = s.recvfrom(2048)
        p = unpack_jitter_req(message)
        print ip, '%6f'%(time.time() - start_time)
        print p[:6]
        # r = pack_jitter_response(message)
        # print unpack_jitter_res(r)
        # s.sendto(r, ip)
    s.close()
