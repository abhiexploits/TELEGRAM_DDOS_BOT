import json
import os

class Config:
    @staticmethod
    def load(config_file="config.json"):
        if not os.path.exists(config_file):
            default_config = {
                "bot_token": "YOUR_BOT_TOKEN_HERE",
                "admin_ids": [123456789, 987654321],
                "max_attacks": 10,
                "log_level": "INFO"
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            print("Please edit config.json and add your bot token")
            exit(1)
        
        with open(config_file, 'r') as f:
            return json.load(f)
