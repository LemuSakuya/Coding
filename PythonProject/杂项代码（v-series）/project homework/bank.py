# bank.py
import os
from datetime import datetime

class BA:

    def __init__(self, acc, acn, init_bla=0):
        self.acc = acc
        self.acn = acn
        self.bla = init_bla
        self.tac_log = f"bank_log_{acn}.txt"
        
        if not os.path.exists(self.tac_log):
            with open(self.tac_log, 'w') as f:
                f.write(f"账户创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"初始余额: {init_bla}\n")
    
    def _log_tac(self, tac_typ, amu):
        with open(self.tac_log, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - {tac_typ}: {amu:.2f}, 余额: {self.bla:.2f}\n")
    
    def deposit(self, amu):
        if amu <= 0:
            raise ValueError("存款金额必须为正数")
        self.bla += amu
        self._log_tac("存款", amu)
        return self.bla
    
    def withdraw(self, amu):
        if amu <= 0:
            raise ValueError("取款金额必须为正数")
        if amu > self.bla:
            raise ValueError("余额不足")
        self.bla -= amu
        self._log_tac("取款", amu)
        return self.bla
    
    def get_bla(self):
        return self.bla
    
    def get_tacs(self):
        try:
            with open(self.tac_log, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "交易记录文件不存在"
    
    def __str__(self):
        return f"账户: {self.acn}, 持有人: {self.acc}, 余额: {self.bla:.2f}"


class Bank:
    
    def __init__(self, name):
        self.name = name
        self.acc = {}
        self.bank_log = "bank_master_log.txt"
        
        if not os.path.exists(self.bank_log):
            with open(self.bank_log, 'w') as f:
                f.write(f"{self.name}银行系统日志\n")
                f.write(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    def _log_bank_activity(self, activity):
        with open(self.bank_log, 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{timestamp} - {activity}\n")
    
    def create_acc(self, acc, acn, init_bla=0):
        if acn in self.acc:
            raise ValueError("该账号已存在")
        new_acc = BA(acc, acn, init_bla)
        self.acc[acn] = new_acc
        self._log_bank_activity(f"创建账户: {acn}, 持有人: {acc}, 初始余额: {init_bla}")
        return new_acc
    
    def get_acc(self, acn):
        if acn not in self.acc:
            raise ValueError("账户不存在")
        return self.acc[acn]
    
    def get_all_tacs(self):
        try:
            with open(self.bank_log, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "银行主日志文件不存在"
    
    def __str__(self):
        return f"{self.name}银行 - 账户数量: {len(self.acc)}"