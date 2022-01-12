# -*- coding: utf-8 -*-
"""
Module handles WHOIS-API calls and Telegram-Messages
"""
from urllib.request import pathname2url
from datetime import datetime
import configparser
import requests


config = configparser.RawConfigParser()
config.read('config.properties')

whois_dict = dict(config.items('WHOIS'))
domains_list = whois_dict['domains'].split(",")
url = whois_dict['api_url']

telegram_dict = dict(config.items('Telegram'))

# Command Line Arguments still to come
DO_PRINT = True
# Choose which Quota it uses from WHOIS
# Option to output all available domain-endings


def build_request_params(req_domain):
    """
    Generates and returns request-parameters for WHOIS
    """
    return "?identifier=" + pathname2url(req_domain)


def evaluate_response(req_response, print_result):
    """
    Evaluates the WHOIS-Response
    """
    response_json = req_response.json()
    if ('name' in response_json) \
        and ('registered' in response_json):
        resp_domain = response_json['name']
        resp_registered = response_json['registered']
        if print_result:
            # dd.mm.YY H:M:S for logging
            now = datetime.now()
            dt_string = now.strftime("%d.%m.%Y %H:%M:%S")
            print(dt_string)
            print('Result for ' + resp_domain + ': ')
            print('Registered: ' + str(resp_registered))
            print('---------------------------\n')
        if resp_registered == False:
            send_message("URL " + resp_domain + " is available!")


def request(req_url, req_apiuser, req_apikey, req_domain):
    """
    Sends the WHOIS-request
    """
    req_params = build_request_params(req_domain)
    return requests.get(req_url + req_params, auth=(req_apiuser, req_apikey))
 #   return urlopen(req_url + req_params).read().decode('utf8')


def query_domains():
    """
    Working method for WHOIS.
    Iterates through URLs from property-file which should be checked
    """
    api_key = whois_dict['api_key']
    api_user = whois_dict['api_user']

    for domain in domains_list:
        response = request(url, api_user, api_key, domain)

        if 'Request timeout' in response:
            response = request(url, api_user, api_key, domain)

        #print(response.json())
        evaluate_response(response, DO_PRINT)


def send_message(message):
    """
    Sends message to every chat_id from property-file
    """
    bot_token = telegram_dict['bot_token']
    chat_ids_list = telegram_dict['chat_ids'].split(",")
    for chat_id in chat_ids_list:
        telegram_bot_sendtext(message, chat_id, bot_token)
        # response = telegram_bot_sendtext(message, chat_id, bot_token)
        # print(response)


def telegram_bot_sendtext(bot_message, chat_id, bot_token):
    """
    Sends a message to the given chat_id.

    Returns response for evaluation, if needed
    """
    send_text = 'https://api.telegram.org/bot' + bot_token + \
                '/sendMessage?chat_id=' + chat_id + \
                '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()


# Starts domain evaluation / checking
query_domains()
