import logging
from json import JSONDecodeError

from mitmproxy import http
import json
from chompjs import parse_js_object

from robert_parker.database.request_to_country import insert_to_db
from robert_parker.robertparker_com_parser import RobertparkerComParser

logger = logging.getLogger(__name__)

vintages_ids = set()


def extract_json_data(message: str):
    try:
        json_data_list = parse_js_object(message)
    except JSONDecodeError:
        return
    if not json_data_list:
        return
    if len(json_data_list) != 1:
        return
    return json.loads(json_data_list[0])


def extract_items(json_data: dict):
    try:
        return json_data['result']['items']
    except KeyError:
        return


def is_vintage_exist(message_text):
    for vintage_id in vintages_ids:
        if vintage_id in message_text:
            return True
    return False


def filter_message(messages):
    filtered_messages = []
    for message in messages:
        if 'result' not in message.text or 'items' not in message.text or is_vintage_exist(message.text):
            continue
        filtered_messages.append(message.text)
    return filtered_messages


def websocket_message(flow: http.HTTPFlow):
    filtered_messages = filter_message(flow.websocket.messages)
    if not filtered_messages:
        return
    for message in filtered_messages:
        json_data = extract_json_data(message)
        if not json_data:
            continue
        wines = extract_items(json_data)
        if not wines:
            continue
        counter = 0
        for wine in wines:
            try:
                parsed_wine = RobertparkerComParser.parse_wines(wine)
                if not parsed_wine:
                    continue
                vintages_ids.add(parsed_wine.wine_id)
                insert_to_db(parsed_wine)
            except:
                logger.error('Not Enough inf')
                raise RuntimeError
            counter += 1
        logger.info(f'{counter} items was created')
