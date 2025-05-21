from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from dotenv import load_dotenv
import os
load_dotenv(override=True)

# Set up Chrome webdriver
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service(os.getenv("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)


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

def start_machine(machine_name):
    driver.get(f"https://app.hackthebox.com/machines/{machine_name}")
    try:
        start_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.spawn-machine-button > div')))
        start_button.click()
    except TimeoutException:
        # if machine was already started this will time out
        pass
    machine_ip = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.fontBold.color-green.cursorPointer')))
    return machine_ip.text

def stop_machine(machine_name):
    driver.get(f"https://app.hackthebox.com/machines/{machine_name}")
    try:
        stop_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i.icon-stop')))
        stop_button.click()
    except TimeoutException:
        # if machine was already stopped this will time out
        pass
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.spawn-machine-button > div'))) # look for the start button again to confirm stop

def get_question(machine_name, question_index, mode="guided"):
    driver.get(f"https://app.hackthebox.com/machines/{machine_name}")
    if mode not in ["guided", "adventure"]:
        raise ValueError(f"HTB machine mode {mode} must be either 'guided' or 'adventure'")
    if mode == "adventure":
        raise NotImplementedError("Adventure mode is not implemented yet")
    mode_div = wait.until(EC.presence_of_element_located((By.ID, mode))) # search within the corresponding div
    wait.until(lambda _: mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content p')) # wait until the questions are loaded
    active_questions = mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content p')
    return active_questions[question_index].text

def check_answer(machine_name, question_index, answer, mode="guided"):
    driver.get(f"https://app.hackthebox.com/machines/{machine_name}")
    if mode not in ["guided", "adventure"]:
        raise ValueError(f"HTB machine mode {mode} must be either 'guided' or 'adventure'")
    if mode == "adventure":
        raise NotImplementedError("Adventure mode is not implemented yet")
    mode_div = wait.until(EC.presence_of_element_located((By.ID, mode))) # search within the corresponding div
    wait.until(lambda _: mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content p')) # wait until the questions are loaded
    active_questions = mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content div.v-input__slot input')
    if active_questions[question_index].get_attribute("disabled") == "true": # if the question is already answered
        return answer == active_questions[question_index].get_attribute("value")
    else:
        active_questions[question_index].send_keys(answer)
        submit_button = mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content button.v-btn')
        submit_button[question_index].click()
        try:
            wait.until(lambda _: mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content button.v-btn pointerEventsNone')) # if button grays out, answer is correct
            return True
        except TimeoutException:
            return False
    

if __name__ == "__main__":
    login_to_htb()
    print(start_machine("Cap"))
    print(get_question("Cap", 0, "adventure"))
    print(check_answer("Cap", 0, "3", "adventure"))
    print(check_answer("Cap", 1, "test", "adventure"))
    stop_machine("Cap")