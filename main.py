import socket

def trace(ip, hops):
    try:
        dest = socket.gethostbyname(ip)
    except socket.error:
        log( 'Invalid host name')
        return
    log('tracing: {}'.format(dest))
    ttl = 1
    port = 33434
    while ttl < hops:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        receiver.bind(('', port))
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        sender.sendto(b'', (dest, port))
        answer_from = None
        try:
            _, answer_from = receiver.recvfrom(65536)
        except socket.error:
            log('socket error ttl={}'.format(ttl))
        finally:
            receiver.close()
            sender.close()
        if answer_from:
            log('ttl = {} {}'.format(ttl, answer_from[0]))
        else:
            log('ttl = {} *****'.format(ttl))
        if answer_from[0] == dest:
            break
        ttl += 1




def log(str):
    print(str)

print('ip or domain:')
ip = input()
trace(ip, 124)