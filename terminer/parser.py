from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from exception import LimitException
from exception import TooOftenException

import time
import random


class Parser:

    def __init__(self, driver):
        self.driver = driver

    def start(self):
        self.random_sleep()
        self.click_button_to_termin()

    def find(self):
        self.update_page()
        found = self.first_available_date()
        if found is not None:
            found.click()
            print("Termin found! Processing to the termin page...")
            return True
        else:
            return False

    def click_first_timeslot(self):
        print("Clicking first available timesolt")
        self.random_sleep()
        self.driver.find_element(By.CSS_SELECTOR, '.timetable > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a').click()
        print("Clicked!")

    def update_page(self):
        print("Refreshing page...")
        self.driver.refresh()

    def click_button_to_termin(self):
        # print("Click button to termin calendar...")
        # self.driver.find_element(By.CSS_SELECTOR,'a.btn').click()
        self.random_sleep()

    def fill_in_data(self, name, email, phone):
        print("Filling in the data...")
        name_fld = self.driver.find_element(By.CSS_SELECTOR,'#familyName')
        mail_fld = self.driver.find_element(By.CSS_SELECTOR,'#email')
        phne_fld = self.driver.find_element(By.CSS_SELECTOR,'#telephone')
        name_fld.send_keys(name)
        mail_fld.send_keys(email)
        phne_fld.send_keys(phone)

    def agree_on_terms(self):
        print("Agreeing on the terms and condition...")
        self.driver.find_element(By.CSS_SELECTOR,'#agbgelesen').click()
        Select(self.driver.find_element(By.CSS_SELECTOR,'select[name="surveyAccepted"]')).select_by_index(1)
        time.sleep(10)

    def get_termin(self):
        self.driver.find_element(By.CSS_SELECTOR,'#register_submit').click()
        print("You have a termin!")

    def first_available_date(self):
        try:
            print("Getting first available date...")
            result = self.driver.find_element(By.CSS_SELECTOR,'.calendar-month-table td.buchbar a')
        except NoSuchElementException:
            print("Not found...")
            if "Zu viele Zugriffe" in self.driver.page_source:
                raise TooOftenException("Too much attempts")
            return None
        return result

    def random_sleep(self):
        time.sleep(random.randrange(2, 4) * 0.5)
