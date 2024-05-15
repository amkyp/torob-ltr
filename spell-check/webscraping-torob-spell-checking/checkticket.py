#pip install selenium
#pip install webdriver-manager
#pip install win10toast
#pip install playsound==1.2.2
#python -m pip install persiantools
from selenium import webdriver
import threading
from datetime import datetime
import time
import re
from win10toast import ToastNotifier
from playsound import playsound
from persiantools import  digits
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

driver = webdriver.Firefox(firefox_profile=profile)
toast = ToastNotifier()
def getTicket(date,notif=True,song=False):
    print(date)
    driver.get("https://safar724.com/bus/tehran-ilam?date="+date)    
    buscapacitys=driver.find_elements("xpath","//span[contains(@class,'available-seat')]")
   # print(buscapacitys)
    for bs in buscapacitys:
         extractText=bs.get_attribute("innerText")
        # print(extractText)
         a= digits.fa_to_en(extractText)
         if (re.search("\.*[1-9].*", a)):
             if(notif): 
                toast.show_toast(
                     "کجایی بیا بلیط بگیر",
                     "بلیط موجود شد",
                     duration = 10,
                     threaded = True,
                    )
                
             if(song):
                 playsound('alert.mp3')
         print(a)

def printit():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time Check =", dt_string)
    threading.Timer(20.0, printit).start()
    getTicket("1401/12/25",True,True)
    time.sleep(10)
    driver.refresh()
    
printit()

