import platform

class Environment:
    def __init__(self):
        self.environment_os = platform.system()
    
    def environment_default_web_directory(self):
        if self.environment_os == "Windows":
            return 'C:\\xampp\\htdocs\\ebay_scanner\\'
        else:
            return '/var/www/html/'