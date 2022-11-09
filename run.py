
import threading
from usdtlist import list1,list2,list3,list4,other
from ST2 import telegbot,St_buy,st_sell,sell_pump

def infiniteloop1():
    while True:
        try:
            St_buy(list1)
            ti.sleep(1)
        except:
            pass

def infiniteloop2():
    while True:
        try:
            St_buy(list2)
            ti.sleep(1)
        except:
            pass
def infiniteloop3():
    while True:
        try:
            St_buy(list3)
            ti.sleep(1)
        except:
            pass
def infiniteloop4():
    while True:
        try:
            St_buy(list4)
            ti.sleep(1)
        except:
            pass

def infiniteloop9():
    while True:
        try:
            St_buy(other)
            ti.sleep(1)
        except:
            pass
 

def infiniteloop_sell():
    while True:
        try:
            st_sell()
            ti.sleep(1)

        except:
            pass
      
def infiniteloop_telebot():
    while True:
        try:

            telegbot()
            ti.sleep(1)

        except:
            pass

def infiniteloop_pump():
    while True:
        try:

            sell_pump()
            ti.sleep(1)

        except:
            pass




thread1 = threading.Thread(target=infiniteloop1)
thread1.start()

thread2 = threading.Thread(target=infiniteloop2)
thread2.start()
        
thread3 = threading.Thread(target=infiniteloop3)
thread3.start()

thread4 = threading.Thread(target=infiniteloop4)
thread4.start()

loop_sell = threading.Thread(target=infiniteloop_sell)
loop_sell.start()

loopbot = threading.Thread(target=infiniteloop_telebot)
loopbot.start()

pumploop = threading.Thread(target=infiniteloop_pump)
pumploop.start()

