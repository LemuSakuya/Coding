#2
import datetime

class BA:
    def __init__(self, acc, init_blc=0):
        self.acc = acc
        self.blc = init_blc
        self.tac = []
        self.add("开户", init_blc)
    
    def add(self, tac, amt):
        tac = {
            "type": tac,
            "amount": amt,
            "balance": self.blc,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tac.append(tac)
    
    def deposit(self, amt):
        if amt <= 0:
            print("WA")
            return False
        
        self.blc += amt
        self.add("存款", amt)
        print(f"成功存入 {amt} 元")
        return True
    
    def withdraw(self, amt):
        if amt <= 0:
            print("WA")
            return False
        
        if amt > self.blc:
            print("ER")
            return False
        
        self.blc -= amt
        self.add("取款", amt)
        print(f"成功取出 {amt} 元")
        return True
    
    def print_tac(self):
        print(f"\n{'*' * 80}")
        print(f"账户名称: {self.acc}")
        print(f"{'*' * 80}")
        print("{:<20} {:<10} {:<10} {:<20}".format("交易时间", "交易类型", "金额", "余额"))
        
        for ts in self.tac:
            print("{:<26} {:<10} {:<12} {:<20}".format(
                ts["time"],
                ts["type"],
                ts["amount"],
                ts["balance"]
            ))
        
        print(f"{'*' * 80}")
        print(f"当前余额: {self.blc} 元")
        print(f"{'*' * 80}\n")


account = BA("LemuSakuya", 0)
account.deposit(1000)

account.withdraw(200)
account.withdraw(1500)
account.deposit(1000)
account.print_tac()