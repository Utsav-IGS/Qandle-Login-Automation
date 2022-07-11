from datetime import datetime
from time import sleep
from seleniumSetup import SeleniumSetup
from selenium.webdriver.common.by import By

class Qandle(SeleniumSetup):
    """
    Qandle interface xpaths for buttons elements
    """    
    def __init__(self) -> None:
        SeleniumSetup.__init__(self)
        self.driver = self.chrome_driver()
        self.required_hours = self.convert_time("09:00:00")
        self.qandle_url = "https://igs.qandle.com/"
        self.email_input_xpath = "//input[@name='email' and @type='email']"
        self.password_input_xpath = "//input[@name='password' and @type='password']"
        self.login_button_xpath = "//button[contains(text(), 'Sign In') and @id='signInSubmit']"
        self.clock_in_xpath = "//span[contains(text(), 'Clock In')]/parent::button"
        self.clock_out_xpath = "//span[contains(text(), 'Clock Out')]/parent::button"
        self.logged_time_xpath = "//div[starts-with(@class, 'timer-time') and contains(@class, 'timer-container')]/child::div[starts-with(@class, 'timer-time-set') and contains(@class, 'blue')]"
        self.modal_yes_xpath = "//span[contains(text(), 'Yes')]/parent::button"
        
    def open_qandle(self):
        self.driver.get(self.qandle_url)
        
    def convert_time(self, time_str):
        return datetime.strptime(time_str, '%H:%M:%S')
    
    def get_logged_hours(self):
        work_time = self.find_element_by_xpath(self.logged_time_xpath)
        if work_time.is_displayed():
            total_work_time = self.convert_time(work_time.text)
        return self.required_hours - total_work_time
        
    def login(self, email: str, password: str):
        """Login to qandle by providing email and password

        Args:
            email (str): Login mail ID
            password (str): Account Password
        """
        # open qandle in chrome
        self.open_qandle()
        
        # get email, password and login button elements
        email_field = self.find_element_by_xpath(self.email_input_xpath)
        password_field = self.find_element_by_xpath(self.password_input_xpath)
        login_button = self.find_element_by_xpath(self.login_button_xpath)
        
        # check email field 
        if email_field is not None and email_field.is_displayed() and email:
            email_field.send_keys(email)
        else:
            self.driver.close()
            raise Exception("Problem with email or email field")
        
        if password_field is not None and password_field.is_displayed() and password:
            password_field.send_keys(password)
        else:
            self.driver.close()
            raise Exception("Problem with password or password field")
        
        if login_button is not None and login_button.is_displayed() and login_button.is_enabled():
            login_button.click()
        else:
            self.driver.close()
            raise Exception("No login button")
                
    def clock_in(self):
        """
        Click on Clock In and start the timer
        """
        clock_in_button = self.find_element_by_xpath(self.clock_in_xpath)
        clock_out_button = self.find_element_by_xpath(self.clock_out_xpath)
        work_time = self.find_element_by_xpath(self.logged_time_xpath)
        
        if clock_out_button.is_displayed():
            print(f"Already Clocked In for today for {work_time.text} hours")
            self.driver.close()
            return
        
        if clock_in_button is not None and clock_in_button.is_displayed():
            clock_in_button.click()
            return
        else:
            self.driver.close()
            raise Exception("No Clock In button")
           
    def clock_out(self):
        """
        Click on Clock Out and stop the timer
        """
        clock_out_button = self.find_element_by_xpath(self.clock_out_xpath)
        modal_yes_button = self.find_element_by_xpath(self.modal_yes_xpath)
        total_work_time = self.get_logged_hours()
        work_time = self.find_element_by_xpath(self.logged_time_xpath)
        min_hours_met = self.convert_time(work_time.text) >= self.required_hours
        
        if min_hours_met:
            if clock_out_button.is_displayed():
                clock_out_button.click()
                sleep(5)
                modal_yes_button.click()
                sleep(5)
            else:
                raise Exception("No Clock out Button")
        else:
            print("Minimum hours not met")
            self.driver.close()
            return
        
    def find_element_by_xpath(self, xpath: str):
        """Finds element with the given xpath

        Args:
            xpath (str): xpath for the required element

        Returns:
            WebElement: WebElement if found
        """
        try:
            return self.driver.find_element(By.XPATH, xpath)
        except Exception:
            return None