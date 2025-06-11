from logger import Logger
from auth import Auth
from alerts import Alerts
from network import scan_ports

CONFIG = "config.json"
DB = "users.db"

def main():
    logger = Logger(CONFIG)
    auth = Auth(DB)
    alerts = Alerts(CONFIG)

    user = input("Username: ")
    pwd = input("Password: ")

    if auth.verify_user(user, pwd):
        logger.info(f"User '{user}' authenticated")
        target = input("Host to scan: ")
        ports = scan_ports(target, [22, 80, 443, 8080])
        logger.info(f"Open ports on {target}: {ports}")
    else:
        logger.warning(f"Failed login attempt: '{user}'")
        alerts.send_email("Security Alert", f"Failed login for user {user}")

if __name__ == "__main__":
    main()
