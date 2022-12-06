# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import DOUBLE


class MysqlCoordinatesMixin:
    latitude = Column("latitude", DOUBLE, nullable=True, unique=False)
    longitude = Column("longitude", DOUBLE, nullable=True, unique=False)
