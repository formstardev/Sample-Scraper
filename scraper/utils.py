import json
import random
import time
from fake_useragent import UserAgent
from . import settings

time_tuple = (
    2012,  # Year
    9,  # Month
    6,  # Day
    0,  # Hour
    38,  # Minute
    0,  # Second
    0,  # Millisecond
)


def acp_api_send_request(driver, message_type, data=None):
    if data is None:
        data = {}
    message = {
        "receiver": "antiCaptchaPlugin",  # this receiver has to be always set as antiCaptchaPlugin
        "type": message_type,  # request type, for example setOptions
        # merge with additional data
        **data,
    }
    # run JS code in the web page context
    # precisely we send a standard window.postMessage method
    return driver.execute_script(
        """
    return window.postMessage({});
    """.format(
            json.dumps(message)
        )
    )


def get_random_proxy():
    proxies_list = settings.PROXY_LIST
    proxy = proxies_list[random.randint(0, len(proxies_list) - 1)]
    proxy = "185.189.39.242:8800"
    print("proxy:", proxy)
    return proxy


def get_user_agent():
    return UserAgent().random


def get_random_number(min=10, max=20):
    return random.randint(min, max)


def random_sleep(min=10, max=20):
    time.sleep(random.randint(min, max))


def convert_class_objects_to_list_dic(objects):
    return [obj.__dict__["_values"] for obj in objects]


def slug_to_name(slug):
    return slug.replace("-", " ").title().strip()


def clean_text(text=""):
    filter_sen = "".join([chr(i) for i in range(1, 32)])
    return text.translate(str.maketrans("", "", filter_sen)).strip()
