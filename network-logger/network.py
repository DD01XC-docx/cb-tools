import socket

def scan_ports(host: str, ports: list[int]) -> list[int]:
    open_ports = []
    for port in ports:
        with socket.socket() as s:
            s.settimeout(0.5)
            try:
                s.connect((host, port))
                open_ports.append(port)
            except:
                pass
    return open_ports
