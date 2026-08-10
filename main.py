# ==========================================
# BANK MANAGEMENT SYSTEM
# Author: MUHAMMAD ABDULLAH FAROOQ
# Language: Python 3.13
# =========================================== 

from src.manager import BankManager
from src.UI import start_app

if __name__ == "__main__":
    manager = BankManager()
    start_app(manager)