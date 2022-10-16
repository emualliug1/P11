from selenium import webdriver
from selenium.webdriver.common.by import By


class TestAuthentification:

    def setup(self):
        # gecko driver 64bits à mettre dans C:\Python\Scripts
        # lien pour le download https://github.com/mozilla/geckodriver/releases
        try:
            self.driver = webdriver.Firefox()
        except:
            pass

    def teardown(self):
        self.driver.close()

    def test_signup(self):
        self.driver.get('http://127.0.0.1:5000/')
        email = self.driver.find_element(By.ID, 'email-input')
        email.send_keys("a@a")
        signup = self.driver.find_element(By.ID, 'button-login')
        signup.click()
        page_url = self.driver.current_url
        assert page_url == 'http://127.0.0.1:5000/show_summary'

