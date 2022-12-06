import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from robert_parker.items import WineItem
# from robert_parker.database.parker_database import insert_or_update
from datetime import datetime


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
        wine_item.sweetness = wine_dict['dryness']['value']
        wine_item.vintage = wine_dict['vintage']
        wine_item.name = wine_dict['name']
        wine_item.name_display = wine_dict['name_display']
        wine_item.producer_name = wine_dict['producer']['name']
        wine_item.producer_show = wine_dict['producer']['show']
        wine_item.producer_id = wine_dict['producer']['_id']
        location = wine_dict.get('location')
        if location:
            wine_item.location_name = location.get('name')
        wine_item.region = wine_dict['region']['name']
        testing_notes = wine['_source']['tasting_notes'][0]
        if not testing_notes:
            return wine_item
        wine_item.reviewer = testing_notes['reviewer']['name']
        wine_item.reviewer_id = testing_notes['reviewer']['_id']
        wine_item.description = testing_notes.get('content')
        wine_item.source_text = testing_notes['source']['label']
        wine_item.source_link = testing_notes['source']['path']
        wine_item.drink_date = testing_notes.get('drink_date')
        wine_item.issue_date = cls.extract_issue_date(testing_notes)
        return wine_item

    @staticmethod
    def extract_last_page_number(driver):
        while True:
            try:
                last_page = driver.find_element(By.XPATH, '//span[contains(text(), '
                                                          '"Last")]/../..').get_attribute('href').rsplit('=', 1)[-1]
                return int(last_page)
            except NoSuchElementException:
                time.sleep(0.1)
                continue
