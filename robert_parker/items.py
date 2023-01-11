from dataclasses import dataclass
from typing import Optional


@dataclass
class WineItem:
    wine_id: Optional[str] = None
    country: Optional[str] = None
    maturity: Optional[str] = None
    rating: Optional[int] = None
    locale: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    variety: Optional[str] = None
    sweetness: Optional[str] = None
    vintage: Optional[str] = None
    name: Optional[str] = None
    reviewer: Optional[str] = None
    reviewer_id: Optional[str] = None
    description: Optional[str] = None
    name_display: Optional[str] = None
    producer_name: Optional[str] = None
    producer_show: Optional[str] = None
    producer_id: Optional[str] = None
    location_name: Optional[str] = None
    region: Optional[str] = None
    source_text: Optional[str] = None
    source_link: Optional[str] = None
    drink_date: Optional[str] = None
    issue_date: Optional[str] = None
