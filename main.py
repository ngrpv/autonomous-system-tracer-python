import json
import socket

import requests


def trace(ip, hops):
    try:
        dest = socket.gethostbyname(ip)
    except socket.error:
        log('Invalid host name')
        return
    log('tracing: {}'.format(dest))
    ttl = 0
    port = 33434
    while ttl < hops:
        ttl += 1
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        receiver.bind(('', port))
        receiver.settimeout(2)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(b'', (dest, port))
        answer_from = None
        try:
            _, answer_from = receiver.recvfrom(65536)
        except socket.error:
            pass
        finally:
            receiver.close()
            sender.close()
        if answer_from:
            as_num = get_info(answer_from[0])
            log('{}\t{}\t{}'.format(ttl, answer_from[0], as_num))
        else:
            log('{}\t *****'.format(ttl))
            continue
        if answer_from[0] == dest:
            break


def get_info(ip):
    info = json.loads(
        requests.get("http://ipinfo.io/{0}/json".format(ip)).content)
    return info.get('org', '__LOCAL__') + '\t' + info.get('country', '')


def log(str):
    print(str)


print('ip or domain:')
ip = input()
trace(ip, 45)
