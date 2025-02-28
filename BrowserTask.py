from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from TaskBase import TaskBase

class BrowserTask(TaskBase):
    def __init__(self, url, browser = None):
        if browser is None:
            raise ValueError("Browser is required")
        self.url = url
        self.browser = browser

        super().__init__("BrowserTask", "Open a browser and perform a task")

    def open(self):
        self.browser.get(self.url)

    def run(self, video = None, watchtime = 30):
        if video is None:
            raise ValueError("Video is required to be able to run a BrowserTask")

        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.button-submit')))
        ActionChains(self.browser).send_keys('SSE').send_keys(Keys.TAB).send_keys('_Group14').send_keys(Keys.ENTER).perform()
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.headerSearchButton'))).click()
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, 'searchTextInput'))).send_keys(video)
        WebDriverWait(self.browser, 10).until(EC.invisibility_of_element((By.CSS_SELECTOR, '.mdlSpinnerActive')))
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(self.browser.find_elements(By.CSS_SELECTOR, f"a[title='{video}']")[-1])).click()
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btnPlay'))).click()

        # Do any task we want to measure here
        sleep(watchtime)

        self.browser.close()