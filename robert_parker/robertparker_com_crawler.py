import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from robert_parker.database.request_to_country import select_requests, update_current_page, update_status, update_amount
from dotenv import load_dotenv
from robertparker_com_parser import RobertparkerComParser
from firefox_driver import driver
from selenium.webdriver.support import expected_conditions as EC

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
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="at-field-username_and_email"]')))
        self.driver.find_element(By.XPATH, '//*[@id="at-field-username_and_email"]').send_keys(LOGIN)
        self.driver.find_element(By.XPATH, '//*[@id="at-field-password"]').send_keys(PASSWORD)
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Sign In")]').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text()[3], "Dmytro")]')))

    @staticmethod
    def build_current_page(link: str, page: int):
        return f'{link}&page={page}'

    def build_vintages_url(self, country: str):
        return f'https://www.robertparker.com/search/wines?max-rating=100&min-rating=85&expand=true&country[]={country}&show-unrated=true&show-tasting-note=true'

    @staticmethod
    def countries():
        return 'Argentina', 'Spain', 'Bulgaria', 'Armenia', 'Chile', 'Liechtenstein', 'China', 'Georgia', \
              'Lebanon', 'Canada', 'Germany', 'Switzerland', 'Algeria', 'Albania', \
               'Italy', 'Cyprus', 'Greece', 'Japan', \
               'Australia', 'Austria', 'Morocco', 'Luxembourg', 'United Kingdom', 'Hungary', 'New Zealand', \
               'Croatia', 'Israel', 'Bosnia and Herzegovina', 'Denmark'

    def parse_products(self):
        results = select_requests()
        requests = results.fetchall()
        if not requests:
            return
        requests.reverse()
        for link, request_id, current_page, country_name in requests:
            if country_name not in self.countries():
                print(f'Skip county {country_name}')
                continue
            # for link, request_id, current_page in (('https://www.robertparker.com/search/wines?max-rating=100'
            #                                         '&min-rating=85&expand=true&country[]=Ukraine'
            #                                         '&show-unrated=true&show-tasting-note=true', 232, 1),):
            self.driver.get(link)
            last_page_number = self.parser.extract_last_page_number(self.driver)
            if not last_page_number:
                continue
            # if not last_page_number:
            #     # update_status(request_id, status=3)
            #     continue
            update_amount(request_id, self.parser.extract_amount(self.driver))
            start_page = 1
            if country_name == 'New Zealand':
                start_page = 68
            for page in range(start_page, last_page_number + 1):

                self.driver.get(self.build_current_page(link, page))
                if not self.parser.find_xpath_delay(self.driver,
                                                    xpath1='//*[@id="by-location"]/div/div[2]/div[1]/div/div/div',
                                                    delay=10):
                    continue
                print(f'{page} of {last_page_number} - {country_name} \n {link}')
                if page == last_page_number:
                    print(f'Last page for {country_name}')
                update_current_page(request_id, page)
            update_status(request_id, status=1)


robert_parker = RobertparkerCom()
robert_parker.login()
robert_parker.parse_products()
