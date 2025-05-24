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

class HTBMachine:
    def __init__(self, machine_name):
        # Set up Chrome webdriver
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(os.getenv("CHROMEDRIVER_PATH"))
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.machine_name = machine_name
        
        # Login and initialize
        self._login_to_htb()
        self.start_machine()

    def _login_to_htb(self):
        self.driver.get("https://app.hackthebox.com/machines")
        cookie_button = self.wait.until(EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
        cookie_button.click()
        email_input = self.wait.until(EC.presence_of_element_located((By.ID, "loginEmail")))
        email_input.send_keys(os.getenv("HTB_EMAIL"))
        password_input = self.wait.until(EC.presence_of_element_located((By.ID, "loginPassword")))
        password_input.send_keys(os.getenv("HTB_PASSWORD"))
        login_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
        login_button.click()
        self.wait.until(EC.presence_of_element_located((By.ID, "topnavbar"))) # wait until login is complete

    def start_machine(self):
        self.driver.get(f"https://app.hackthebox.com/machines/{self.machine_name}")
        try:
            start_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.spawn-machine-button > div')))
            start_button.click()
        except TimeoutException:
            # if machine was already started this will time out
            pass
        machine_ip = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.fontBold.color-green.cursorPointer')))
        return machine_ip.text

    def stop_machine(self):
        self.driver.get(f"https://app.hackthebox.com/machines/{self.machine_name}")
        try:
            stop_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i.icon-stop')))
            stop_button.click()
        except TimeoutException:
            # if machine was already stopped this will time out
            pass
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.spawn-machine-button > div'))) # look for the start button again to confirm stop

    def get_question(self, question_index, mode="guided"):
        self.driver.get(f"https://app.hackthebox.com/machines/{self.machine_name}")
        if mode not in ["guided", "adventure"]:
            raise ValueError(f"HTB machine mode {mode} must be either 'guided' or 'adventure'")
        if mode == "adventure":
            raise NotImplementedError("Adventure mode is not implemented yet")
        mode_div = self.wait.until(EC.presence_of_element_located((By.ID, mode))) # search within the corresponding div
        self.wait.until(lambda _: mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content p')) # wait until the questions are loaded
        active_questions = mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content p')
        return active_questions[question_index].text

    def check_answer(self, question_index, answer, mode="guided"):
        self.driver.get(f"https://app.hackthebox.com/machines/{self.machine_name}")
        if mode not in ["guided", "adventure"]:
            raise ValueError(f"HTB machine mode {mode} must be either 'guided' or 'adventure'")
        if mode == "adventure":
            raise NotImplementedError("Adventure mode is not implemented yet")
        mode_div = self.wait.until(EC.presence_of_element_located((By.ID, mode))) # search within the corresponding div
        self.wait.until(lambda _: mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content p')) # wait until the questions are loaded
        active_questions = mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content div.v-input__slot input')
        if active_questions[question_index].get_attribute("disabled") == "true": # if the question is already answered
            return answer == active_questions[question_index].get_attribute("value")
        else:
            active_questions[question_index].send_keys(answer)
            submit_button = mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content button.v-btn')
            submit_button[question_index].click()
            try:
                self.wait.until(lambda _: mode_div.find_elements(By.CSS_SELECTOR, 'div.v-expansion-panel-content button.v-btn pointerEventsNone')) # if button grays out, answer is correct
                return True
            except TimeoutException:
                return False

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self.stop_machine()
        if hasattr(self, 'driver'):
            self.driver.quit()


if __name__ == "__main__":
    # Example usage
    machine = HTBMachine("Cap")
    print(machine.start_machine())
    print(machine.get_question(0, "adventure"))
    print(machine.check_answer(0, "3", "adventure"))
    print(machine.check_answer(1, "test", "adventure"))
    machine.stop_machine()