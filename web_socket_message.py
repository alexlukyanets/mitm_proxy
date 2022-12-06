from json import JSONDecodeError

from mitmproxy import http
import json
from chompjs import parse_js_object
from mitmproxy.websocket import WebSocketMessage

from robert_parker.database.request_to_country import insert_or_update
from robert_parker.robertparker_com_parser import RobertparkerComParser


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


def websocket_message(flow: http.HTTPFlow):
    messages = flow.websocket.messages
    filtered_messages = [message.text for message in messages if 'result' in message.text and 'items' in message.text]
    if not filtered_messages:
        return
    for message in filtered_messages:
        json_data = extract_json_data(message)
        if not json_data:
            continue
        wines = extract_items(json_data)
        if not wines:
            continue
        for wine in wines:
            parsed_wine = RobertparkerComParser.parse_wine(wine)
            if not parsed_wine:
                continue
            insert_or_update(parsed_wine)
            print('Write item')
