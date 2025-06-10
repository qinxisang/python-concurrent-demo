import threading
import random


class ConflictBankAccount:
    def __init__(self):
        self.balance = 1000

    def transfer(self, amount):
        # 扩大计算窗口（创造冲突机会）
        delay = random.random() * 0.001  # 随机延时

        # 模拟更复杂的银行操作
        ledger = self.balance  # 读取总账
        threading.Event().wait(delay)  # 随机延时1

        net_value = ledger + amount  # 计算新净值
        threading.Event().wait(delay)  # 随机延时2

        # 双重验证（模拟风控系统）
        if net_value < 0:
            net_value = ledger  # 拒绝透支
        threading.Event().wait(delay)  # 随机延时3

        self.balance = net_value  # 写入新值

class UltimateConflictAccount(ConflictBankAccount):
    def transfer(self, amount):
        # 强制在关键点放弃CPU
        if threading.current_thread().name.endswith('0'):
            threading.Event().wait(0.01)
        super().transfer(amount)
# 测试方法（添加了进度显示）
def stress_test(account_class):
    account = account_class()
    threads = []

    print(f"测试 {account_class.__name__}...")
    for i in range(100):
        t = threading.Thread(
            target=account.transfer,
            args=(-10,)  # 每次转出10元
        )
        threads.append(t)
        t.start()
        # 动态显示进度
        if i % 20 == 0:
            print(f"▌已启动{i + 1}个线程", end='\r')

    for t in threads:
        t.join()

    return account.balance


# 运行冲突测试（至少执行3次观察变化）
print("===== 数据冲突演示 =====")
for i in range(5):
    result = stress_test(UltimateConflictAccount)
    print(f"测试 {i + 1} → 余额: {result}元")