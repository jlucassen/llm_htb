from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Set up Chrome webdriver
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(os.getenv("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)


def login_to_htb():
    driver.get("https://app.hackthebox.com/machines")
    cookie_button = wait.until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
    cookie_button.click()
    email_input = wait.until(EC.presence_of_element_located((By.ID, "loginEmail")))
    email_input.send_keys(os.getenv("HTB_EMAIL"))
    password_input = wait.until(EC.presence_of_element_located((By.ID, "loginPassword")))
    password_input.send_keys(os.getenv("HTB_PASSWORD"))
    login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    login_button.click()
    wait.until(EC.presence_of_element_located((By.ID, "topnavbar"))) # wait until login is complete

if __name__ == "__main__":
    login_to_htb()
