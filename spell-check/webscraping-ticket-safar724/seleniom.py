#pip install selenium
#pip install webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading




Options=Options()
Options.add_argument("--headless")#dont show browser
Options.add_argument("--ignore-certificate-errors")
Options.add_experimental_option("detach",True)
Options.add_argument('--ignore-certificate-errors-spki-list') 
Options.add_argument('log-level=3')
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=Options)
driver.get("https://safar724.com/bus/tehran-ilam?date=1401/12/19")
def getTicket():    
    buscapacitys=driver.find_elements("xpath","//span[contains(@class,'available-seat')]")
    for bs in buscapacitys:
         print(bs.get_attribute("innerText"))




def printit():
  threading.Timer(1.0, printit).start()
  getTicket()
  driver.refresh()

printit()
    

