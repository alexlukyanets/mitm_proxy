import logging
import time
from typing import Optional, List

from selenium.common import NoSuchElementException, InvalidArgumentException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from robert_parker.items import WineItem
from datetime import datetime

logger = logging.getLogger(__name__)


class RobertparkerComParser:
    @staticmethod
    def exception_tuple() -> tuple:
        return AttributeError, IndexError, TypeError, ValueError

    @classmethod
    def extract_issue_date(cls, testing_notes: dict):
        try:
            return datetime.fromtimestamp(testing_notes['issue_date']['$date'] / 1e3).strftime("%m/%d/%Y, %H:%M:%S")
        except cls.exception_tuple():
            print('Enable to parse issue date')
            return

    @staticmethod
    def url_join(current_url: str):
        return f'https://www.robertparker.com{current_url}'

    @classmethod
    def parse_wine(cls, wine: dict):
        wine_dict = wine.get('_source')

        if not wine_dict:
            return
        wine_item = WineItem()
        wine_item.wine_id = wine['_id']
        wine_item.country = wine_dict['country']['name']
        maturity = wine_dict.get('maturity')
        if maturity:
            wine_item.maturity = maturity.get('value')
        rating = wine_dict.get('rating')
        if rating:
            wine_item.rating_low = rating.get('low')
            wine_item.rating_high = rating.get('high')
            wine_item.rating_computed = rating.get('computed')
        locale = wine_dict.get('locale')
        if locale:
            wine_item.locale = locale.get('name')
        wine_item.type = wine_dict['type']['value']
        wine_item.color = wine_dict['color_class']['value']
        variety = wine_dict.get('variety')
        if variety:
            wine_item.variety = variety[0].get('value')
        sweetness = wine_dict.get('dryness')
        if sweetness:
            wine_item.sweetness = sweetness.get('value')
        wine_item.vintage = wine_dict['vintage']
        if wine_item.vintage:
            wine_item.vintage = str(wine_dict['vintage'])
        wine_item.name = wine_dict['name']
        wine_item.name_display = wine_dict['name_display']
        wine_item.producer_name = wine_dict['producer']['name']
        wine_item.producer_show = wine_dict['producer']['show']
        wine_item.producer_id = wine_dict['producer']['_id']
        location = wine_dict.get('location')
        if location:
            wine_item.location_name = location.get('name')
        region = wine_dict.get('region')
        if region:
            wine_item.region = region.get('name')
        testing_notes = wine['_source']['tasting_notes']
        if not testing_notes:
            return wine_item
        testing_notes = testing_notes[0]
        wine_item.reviewer = testing_notes['reviewer']['name']
        wine_item.reviewer_id = testing_notes['reviewer']['_id']
        wine_item.description = testing_notes.get('content')
        wine_item.source_text = testing_notes['source']['label']
        wine_item.source_link = testing_notes['source']['path']
        wine_item.drink_date = testing_notes.get('drink_date')
        wine_item.issue_date = cls.extract_issue_date(testing_notes)
        return wine_item

    @classmethod
    def is_wines_exist(cls, driver: WebDriver) -> bool:
        element = cls.find_xpath_delay(driver, '/html/body/div[2]/main/div/div/div/div/div/div/div', max_counter=50)
        if element:
            return True
        return False

    @staticmethod
    def selenium_exceptions() -> tuple:
        return NoSuchElementException, InvalidArgumentException, TimeoutException

    @classmethod
    def extract_last_page_number(cls, driver: WebDriver) -> Optional[int]:
        element = cls.find_xpath_delay(driver, xpath1='//span[contains(text(), "Last")]/../..')
        if element:
            try:
                return int(element.get_attribute('href').rsplit('=', 1)[-1])
            except ValueError:
                return 1
        try:
            cls.find_xpaths(driver, ['//*[@id="by-location"]/div/div[2]/div[1]/div/div/div'], 1)
        except cls.selenium_exceptions():
            return

    @classmethod
    def find_xpaths(cls, driver: WebDriver, xpaths: List, delay):
        for item_xpath in xpaths:
            try:
                return WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, item_xpath)))
            except cls.selenium_exceptions():
                pass

    @classmethod
    def find_xpath_delay(cls, driver: WebDriver, xpath1, xpath2=None, max_counter=40, delay=0.1):
        xpaths = [item for item in [xpath1, xpath2] if item]
        if not xpaths:
            return
        counter = 0
        while counter != max_counter:
            elem = cls.find_xpaths(driver, xpaths, delay)
            if elem:
                return elem
            counter += 1
