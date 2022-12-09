from typing import Union, Optional

from sqlalchemy import update
from sqlalchemy.sql import select
from robert_parker.database.models.parker_wine import Base, Request, ParkerWine

from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import insert

import sqlalchemy
from robert_parker.database.mysql_connection_string import mysql_connection_string
import pycountry
from robert_parker.items import WineItem

engine = sqlalchemy.create_engine(mysql_connection_string())
engine.connect()
Base.metadata.create_all(engine)


def create_requests(url: str, country_name, amount, current_page):
    inseted_stmt = insert(Request).values(
        {'url': url, 'country_name': country_name, 'amount': amount, 'current_page': current_page})
    compile_execute_selection(inseted_stmt)


def select_requests():
    stmt = select(Request.url, Request.id, Request.current_page).where(Request.status == 0)
    return compile_execute_selection(stmt)


def update_current_page(request_id, current_page):
    stmt = update(Request).where(Request.id == request_id).values({'current_page': current_page})
    compile_execute_selection(stmt)


def update_status(request_id, status):
    stmt = update(Request).where(Request.id == request_id).values({'status': status})
    compile_execute_selection(stmt)


def select_item(item: WineItem):
    stmt = select(ParkerWine.id).where(ParkerWine.name == item.name,
                                       ParkerWine.rating_low == item.rating_low,
                                       ParkerWine.name_display == item.name_display,
                                       ParkerWine.rating_high == item.rating_high,
                                       ParkerWine.drink_date == item.drink_date,
                                       ParkerWine.reviewer == item.reviewer,
                                       ParkerWine.source_link == item.source_link,
                                       ParkerWine.reviewer_id == item.reviewer_id,
                                       ParkerWine.wine_id == item.wine_id,
                                       ParkerWine.description == item.description,
                                       ParkerWine.region == item.region,
                                       ParkerWine.producer_id == item.producer_id)
    result = compile_execute_selection(stmt)
    wine_ids = result.fetchall()
    if not wine_ids or len(wine_ids) != 1:
        return
    return wine_ids[0]


def compile_execute_selection(stmt, item=None):
    try:
        stmt_compiled = stmt.compile(compile_kwargs={"literal_binds": True}, dialect=mysql.dialect())
    except (TypeError, AttributeError):
        return
    return engine.execute(str(stmt_compiled), tuple(stmt_compiled.params.values()))


def insert_to_db(item: WineItem):
    inserted_stmt = insert(ParkerWine)
    stmt = inserted_stmt.values(item.__dict__)
    compile_execute_selection(stmt, item)


def update_item(item, wine_id):
    item['id'] = wine_id[0]
    stmt = update(ParkerWine).where(ParkerWine.id == wine_id[0]).values(item)
    compile_execute_selection(stmt)


def insert_or_update(wine_item: WineItem):
    wine_id = select_item(wine_item)
    if wine_id:
        update_item(wine_item.__dict__, wine_id)
        return
    insert_to_db(wine_item)


if __name__ == '__main__':
    # update_status_counter_request(1, 0)
    for country in pycountry.countries:
        url = f'https://www.robertparker.com/search/wines?max-rating=100&min-rating=85&expand=true&country[]={country.name}&show-unrated=true&show-tasting-note=true'
        create_requests(url, country_name=country.name, amount=0, current_page=1)
    france_url_one = "https://www.robertparker.com/search/wines?max-rating=100&min-rating=85&expand=true&countryg=100&country[]=France&region[]=Alsace&region[]=Beaujolais&region[]=Bordeaux&region[]=Burgundy&region[]=Champagne&region[]=Corsica&region[]=Coteaux%20Champenois&region[]=Cr%C3%A9mant%20d%E2%80%99Alsace&region[]=IGP%20Vin%20des%20Allobroges%20(Savoie)&region[]=Jura&region[]=Languedoc&region[]=Languedoc-Roussillon&region[]=Loire&region[]=Loire%20Valley&region[]=Lorraine&region[]=Normandy&region[]=Provence&region[]=Roussillon&region[]=R%C3%A9gion%20Sud-Ouest%20de%20la%20France&region[]=Savoie&region[]=South%20West&region[]=Southern%20France&region[]=Southern%20Rhone&region[]=Southern%20Rh%C3%B4ne&region[]=Val%20de%20Loire&region[]=Vin%20de%20France&region[]=Vin%20de%20Pays&region[]=Vin%20de%20Pays%20de%20l%27Atlantique&show-tasting-note=true"
    create_requests(france_url_one, country_name='france', amount=0, current_page=1)
    france_url_two = 'https://www.robertparker.com/search/wines?max-rating=100&min-rating=85&expand=true&country[]=France&region[]=Rh%C3%B4ne&show-unrated=true&show-tasting-note=true'
    create_requests(france_url_one, country_name='france', amount=0, current_page=1)
