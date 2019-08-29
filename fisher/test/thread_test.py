from threading import Thread
import threading
import time
from werkzeug.local import Local, LocalStack


def worker(key):
    print('i an a new thread!' + str(key))
    # t = Thread.current_thread()
    time.sleep(10)
    # print(t.getName())
    print('2')

key = 111111111
new_t = Thread(target=worker, args=[key], name='new_thread' )
new_t.start()
print('这是一个线程')
t = threading.current_thread()
print(t.getName())

# key = 111111111
# new_t = threading.Thread(target=worker, args=[key], name='new_thread' )
# new_t.start()


# class A:
#     b = 2
#
#
# my_obj = LocalStack()
# print(my_obj.top)
# my_obj.push(1)
#
#
# def worker1():
#     my_obj.push(2)
#
# new_t1 = Thread(target=worker1)
# new_t1.start()
# time.sleep(1)
# print(my_obj.top)