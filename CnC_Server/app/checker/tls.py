import socket
import ssl


def getTLSVersion(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        # print(sock)
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # print(ssock.version())
            return str(ssock.version())

# hostname = 'msun.ru'
# getTLSVersion(hostname)