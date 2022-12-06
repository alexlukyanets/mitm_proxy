from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, INTEGER, DATETIME
from sqlalchemy import Column

from robert_parker.database.models.mixins import MysqlTimestampsMixin, MysqlPrimaryKeyMixin, MysqlStatusMixin

Base = declarative_base()


class ParkerWine(Base, MysqlPrimaryKeyMixin, MysqlTimestampsMixin):
    __tablename__ = 'parker_wine'

    wine_id = Column(VARCHAR(50))
    country = Column(VARCHAR(150))
    maturity = Column(VARCHAR(500))
    locale = Column(VARCHAR(768))
    type = Column(VARCHAR(768))
    color = Column(VARCHAR(50))
    variety = Column(VARCHAR(768))
    sweetness = Column(VARCHAR(768))

    rating_high = Column(INTEGER)
    rating_low = Column(INTEGER)
    rating_computed = Column(INTEGER)
    vintage = Column(VARCHAR(768))

    name = Column(VARCHAR(768))
    name_display = Column(VARCHAR(768))
    producer_name = Column(VARCHAR(768))
    producer_show = Column(VARCHAR(768))
    location_name = Column(VARCHAR(768))
    region = Column(VARCHAR(768))
    source_text = Column(VARCHAR(768))
    source_link = Column(VARCHAR(768))
    reviewer = Column(VARCHAR(768))
    reviewer_id = Column(VARCHAR(768))
    drink_date = Column(VARCHAR(100))
    issue_date = Column(VARCHAR(100))
    producer_id = Column(VARCHAR(100))
    description = Column(TEXT)


class Request(Base, MysqlPrimaryKeyMixin, MysqlTimestampsMixin, MysqlStatusMixin):
    __tablename__ = 'request'

    url = Column(TEXT)
    country_name = Column(VARCHAR(100))
    current_page = Column(INTEGER)
    amount = Column(INTEGER)
