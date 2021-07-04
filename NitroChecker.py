import string
import time
from enum import Enum
import requests
import random
import json
from colorama import Fore


class Responses(Enum):
    RATE_LIMITED = 0
    INVALID_GIFT = 1
    VALID = 2
    ACCESS_DENIED = 3
    ALREADY_CLAIMED = 4
    IN_CACHE = 5


class ErrorHandler:
    def __init__(self):
        self.error_responses = {'{"message": "Unknown Gift Code", "code": 10038}': Responses.INVALID_GIFT,
                                'You are being rate limited': Responses.RATE_LIMITED,
                                'Access denied': Responses.ACCESS_DENIED,
                                }

    def handle_errors(self, response_text):
        for error in self.error_responses:
            if error in response_text:
                return self.error_responses[error]

        response_json = json.loads(response_text)
        redeemed = response_json['max_uses'] - response_json['uses'] == 0
        return Responses.VALID if not redeemed else Responses.ALREADY_CLAIMED


class NitroChecker:
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
        self.cache = {}
        self.rate_limit = {'rate_timestamp': 0, 'rate_delay': 0}

    @classmethod
    def format_message(cls, first_color: Fore, *args):
        formatted_message = f"[{first_color}{args[0]}{Fore.WHITE}]"

        for arg in args[1:]:
            formatted_message += f' - [{Fore.YELLOW}{arg}{Fore.WHITE}]'

        print(formatted_message)

    @classmethod
    def generate_code(cls):
        return ''.join([random.choice(string.ascii_letters + string.digits) for x in range(random.choice([16, 24]))])

    def check_code(self, code):
        if code in self.cache:
            return Responses.IN_CACHE

        r = requests.get(f'http://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true')

        response = self.error_handler.handle_errors(r.text)
        self.cache[code] = response

        if response == Responses.RATE_LIMITED:
            response_json = r.json()

            self.rate_limit = {'rate_timestamp': time.time(), 'rate_delay': response_json['retry_after']}

        return response
