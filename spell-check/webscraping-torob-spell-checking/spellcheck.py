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
profile = webdriver.FirefoxProfile()
profile.accept_untrusted_certs = True

driver = webdriver.Firefox(firefox_profile=profile)
toast = ToastNotifier()
def getSpell(query):
    driver.get("https://torob.com/search/?query="+query)    
    check_spell=driver.find_elements("xpath","//p[contains(@class,'black_p')]")

    names=driver.find_elements("xpath","//h2[contains(@class,'jsx-fa8eb4b3b47a1d18')]")
    for name in names:
         extractText=name.get_attribute("innerText")
         print(extractText)

    
    for cs in check_spell:
        extractText=cs.get_attribute("innerText")
        if extractText.startswith("جستجو غلط‌گیری شد:"):
             print(extractText.split(":")[1])
             
def printit():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time Check =", dt_string)
    threading.Timer(20.0, printit).start()
    getSpell("دورخه")
    time.sleep(10)
    driver.refresh()
    
printit()

