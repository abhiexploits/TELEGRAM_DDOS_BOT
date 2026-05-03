import json
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file="attack_logs.json"):
        self.log_file = log_file
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                json.dump([], f)
    
    def log(self, message):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        logs.append(log_entry)
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def get_attack_count(self):
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        return len(logs)
    
    def get_detailed_stats(self):
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        
        stats = f"Total attacks: {len(logs)}\n\nRecent attacks:\n"
        for log in logs[-10:]:
            stats += f"{log['timestamp']}: {log['message']}\n"
        return stats
