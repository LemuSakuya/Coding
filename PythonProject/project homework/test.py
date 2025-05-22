# test.py
from bank import Bank

def test_bank_system():
    bank = Bank("LemuSakuya")
    
    try:
        acc1 = bank.create_acc("Lemu", "10001", 1000)
        acc2 = bank.create_acc("Sakuya", "10002", 500)
        print(bank)
    except ValueError as e:
        print("错误:", e)

    try:
        acc1.deposit(500)
        acc1.withdraw(200)
        acc2.deposit(1000)
        acc2.withdraw(300)
    except ValueError as e:
        print("交易错误:", e)

    print("\nLemu的交易记录:")
    print(acc1.get_tacs())
    
    print("\nSakuya的交易记录:")
    print(acc2.get_tacs())
    
    print("\n银行所有活动记录:")
    print(bank.get_all_tacs())

if __name__ == "__main__":
    test_bank_system()