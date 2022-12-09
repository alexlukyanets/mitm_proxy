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
        self.driver = driver
        self.parser = RobertparkerComParser

    def login(self):
        self.driver.get(LOGIN_URL)
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="at-field-username_and_email"]').send_keys(LOGIN)
        self.driver.find_element(By.XPATH, '//*[@id="at-field-password"]').send_keys(PASSWORD)
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Sign In")]').click()
        time.sleep(4)

    def search_link_gen(self):
        for link in self.search_links():
            yield link

    @staticmethod
    def build_current_page(link: str, page: int):
        return f'{link}&page={page}'

    def parse_products(self):
        results = select_requests()
        requests = results.fetchall()
        if not requests:
            return
        requests.reverse()
        for link, request_id, current_page in requests:
        # for link, request_id, current_page in (('https://www.robertparker.com/search/wines?max-rating=100'
        #                                         '&min-rating=85&expand=true&country[]=Ukraine'
        #                                         '&show-unrated=true&show-tasting-note=true', 232, 1),):
            self.driver.get(link)
            last_page_number = self.parser.extract_last_page_number(self.driver)
            if not last_page_number:
                update_status(request_id, status=3)
                continue
            for page in range(current_page, last_page_number + 1):
                self.driver.get(self.build_current_page(link, page))
                if not self.parser.find_xpath_delay(self.driver,
                                                    xpath1='//*[@id="by-location"]/div/div[2]/div[1]/div/div/div'):
                    continue
                print(f'{page} of {last_page_number}')
                update_current_page(request_id, page)
            update_status(request_id, status=1)


robert_parker = RobertparkerCom()
# robert_parker.login()
robert_parker.parse_products()
