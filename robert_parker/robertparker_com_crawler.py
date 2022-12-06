import os
import time

from selenium.common import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.common.by import By

from robert_parker.database.request_to_country import select_requests, update_current_page, update_status
from dotenv import load_dotenv
from robertparker_com_parser import RobertparkerComParser
from firefox_driver import driver

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
LOGIN_URL = os.getenv('LOGIN_URL')


class RobertparkerCom:
    def __init__(self):
        self.diver = driver
        self.parser = RobertparkerComParser

    def login(self):
        self.diver.get(LOGIN_URL)
        time.sleep(2)
        self.diver.find_element(By.XPATH, '//*[@id="at-field-username_and_email"]').send_keys(LOGIN)
        self.diver.find_element(By.XPATH, '//*[@id="at-field-password"]').send_keys(PASSWORD)
        self.diver.find_element(By.XPATH, '//button[contains(text(), "Sign In")]').click()
        time.sleep(4)

    def search_link_gen(self):
        for link in self.search_links():
            yield link

    @staticmethod
    def build_current_page(link: str, page: int):
        return f'{link}&page={page}'

    def open_link_and_sleep(self, link, sleep, xpath=None, next_xpath=None):
        self.diver.get(link)
        if xpath:
            while True:
                try:
                    return self.diver.find_element(By.XPATH, xpath)
                except (NoSuchElementException, InvalidArgumentException):
                    time.sleep(0.01)
                    try:
                        return self.diver.find_element(By.XPATH, next_xpath)
                    except (NoSuchElementException, InvalidArgumentException):
                        continue
        time.sleep(sleep)

    def parse_products(self):
        results = select_requests()
        requests = results.fetchall()
        if not requests:
            return
        requests.reverse()
        for link, request_id, current_page in requests:
            self.open_link_and_sleep(link, 5, '//span[contains(text(), "Last")]',
                                     '//h2[contains(text(), "No results")]')
            last_page_number = self.parser.extract_last_page_number(self.diver)
            if not last_page_number:
                update_status(request_id, status=2)
                continue
            for page in range(current_page, last_page_number + 1):
                print(f'{page} of {last_page_number}')
                self.open_link_and_sleep(self.build_current_page(link, page), 5,
                                         '//*[@id="by-location"]/div/div[2]/div[1]/div/div/div')
                update_current_page(request_id, page)
            update_status(request_id, status=1)


robert_parker = RobertparkerCom()
# robert_parker.login()
robert_parker.parse_products()
