import re

class Validator:
    @staticmethod
    def validate_ip(ip):
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        parts = ip.split('.')
        for part in parts:
            if int(part) < 0 or int(part) > 255:
                return False
        return True
    
    @staticmethod
    def validate_port(port):
        try:
            port = int(port)
            return 1 <= port <= 65535
        except:
            return False
    
    @staticmethod
    def validate_duration(duration):
        try:
            duration = int(duration)
            return 1 <= duration <= 3600
        except:
            return False
    
    @staticmethod
    def validate_threads(threads):
        try:
            threads = int(threads)
            return 1 <= threads <= 5000
        except:
            return False
