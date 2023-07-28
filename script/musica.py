from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def youtube_music(name,driver):

    # Use ChromeDriverManager to automatically download and manage the correct ChromeDriver version
    driver.get(f"https://music.youtube.com/search?q={name}")

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.VfPpkd-LgbsSe")))
    button.click()
    play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytmusic-play-button-renderer#play-button")))
    play_button.click()
        # Clicca sul pulsante "Salta gli annunci" se presente
    # Gestisci lo skip button
    time.sleep(5)
    while True:
        # Gestisci lo skip button
        try:
            skip_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-ad-skip-button")
            if skip_button.is_displayed():
                skip_button.click()
                break  # Esci dal ciclo quando lo skip button viene cliccato
        except:
            pass

        # Attendi un secondo prima di verificare nuovamente lo skip button
        time.sleep(1)
    '''
    time_info = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.time-info")))
    time_text = time_info.text.strip()
    current_time, total_duration = time_text.split(" / ")

    total_duration_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(total_duration.split(":"))))

    remaining_time_seconds = total_duration_seconds - int(current_time.split(":")[1])
    time.sleep(remaining_time_seconds)

    # Close the browser
    driver.close()'''
def music_driver(path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-plugins-discovery")
    # Inserisci il tuo percorso corretto qui
    # Aggiungi le seguenti opzioni per gestire i cookie
    #chrome_options.add_argument("--user-data-dir=selenium")
    #chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-usb")

    return webdriver.Chrome(options=chrome_options)

def skippa(driver):
    print("skippo")
    skip=driver.find_element(By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[5]/tp-yt-iron-icon")
    skip.click()


def quit(driver):
    driver.quit()
