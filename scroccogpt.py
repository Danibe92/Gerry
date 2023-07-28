from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
import time
def load_session(path):
    import platform
    is_android = platform.system() == 'Android'
    # Imposta il percorso del file ChromeDriver
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-usb")
    chrome_options.add_argument("--headless")
    if is_android:
       chrome_options.add_experimental_option('androidPackage', 'com.android.chrome')
       driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    else:
      driver = webdriver.Chrome(options=chrome_options,executable_path=path)
    driver.get("https://www.pizzagpt.it/")
    return driver
def gpt(driver,question):
    wait = WebDriverWait(driver, 10)
    while True:
     try:
      element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
      element.click()
      break
     except:
      driver.get("https://chat.chatbot.sex/chat/")

    input = driver.find_element(By.TAG_NAME, "textarea")
    input.send_keys(question)  
    input.send_keys(Keys.ENTER)
    i=driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[1]")
    cancel_button=i.find_element(By.ID,"cancelButton")
    time.sleep(10)
    while True:
        if cancel_button.is_displayed()==True:
            # Attendi un po' prima di riprovare
            #print("boo")
            time.sleep(5)
            continue
        else:
            break
    responses=driver.find_elements(By.CLASS_NAME,"message")
    i=len(responses)
    i=i-1
    response=responses[i].find_element(By.CLASS_NAME,"content")
    return response.text

def pizzagpt(driver,text):
    input = driver.find_element(By.TAG_NAME, "textarea")
    input.send_keys(text+" rispondi in modo breve come se fossi Gerry Scotti senza mai dire di esserlo")
    input.send_keys(Keys.ENTER)
    responses=driver.find_elements(By.CSS_SELECTOR,".chat-start .chat-bubble")
    i=len(responses)
    while True:
     try:
      response=responses[i-1].find_elements(By.TAG_NAME,"p")
      if response[0].text =="Sembra che ti piaccia PizzaGPT. Ogni giorno tantissime persone come te stanno utizzando questo tool gratuito, ma la pubblicità non basta per coprire i costi. Considera di effettuare una donazione, per tenere aperto il servizio. Grazie!":
         response=responses[i-2].find_elements(By.TAG_NAME,"p")
         break
      else:
         break

     except:
      responses=driver.find_elements(By.CSS_SELECTOR,".chat-start .chat-bubble")
      i=len(responses)
      continue
    responsef=""
    for o in response:
        responsef=responsef+o.text
    return responsef
'''
driver=load_session("chromedriver.exe")

while True:
  inp = input("\nYou: ")
  if inp=="quit":
     driver.quit()
     break
  else:
   print(pizzagpt(driver,inp))'''