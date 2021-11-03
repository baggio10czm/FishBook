"""
 User: Czm
 Date: 2021/10/29
 Time: 12:41
"""
import threading
import time

from werkzeug.local import LocalStack

test = LocalStack()

test.push(7)

# top 只取不弹(不删)
print(test.top)
# pop 取并弹(删)
print(test.pop())
# None
print(test.top)

# 栈 先进后出,后进先出
test.push(7)
test.push(3)
print(test.top)  # 3
print(test.top)  # 3
print(test.pop())  # 3
print(test.top)  # 7

# 多线程
# 使用线程隔离的意义在于,使当前线程能够正确的引用到他自己所创建的对象,
# 而不是引用到其他线程所创建的对象
print('____________多线程___________')

my_stack = LocalStack()
my_stack.push(1)


def worker():
    # 主线程(其他线程)赋值不会影响新线程,所以是None
    print('新线程my_stack.top的值:' + str(my_stack.top))
    # 新线程push操作
    my_stack.push(2)
    print('新线程赋值后:my_stack.top=' + str(my_stack.top))


new_t = threading.Thread(target=worker, name='new_thread')
new_t.start()
time.sleep(1)

# 主线程
print('主线程my_stack.top=' + str(my_stack.top))


# 不使用线程隔离的情况
class NoneLocal:
    def __init__(self, v):
        self.v = v


n = NoneLocal(7)


# 以线程ID号作为key的字典 -> Local->LocalStack
# AppContext RequestContext -> LocalStack
# Flask -> AppContext       Request -> RequestContext
# current_app -> (LocalStack.top = AppContext   top.app=Flask)
# request ->  (LocalStack.top = RequestContext   top.app=Request)
