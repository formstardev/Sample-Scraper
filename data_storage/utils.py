import json
import uuid
from datetime import timezone, datetime
from flatten_json import flatten


def flatten_json(data={}, separator=".", ignore_keys={"_createdBy"}):
    return flatten(data, separator, root_keys_to_ignore=ignore_keys)


def convert_class_objects_to_list_dic(objects):
    return [obj.__dict__["_values"] for obj in objects]


def get_json_from_file(filepath=""):
    f = open(filepath)
    data = json.load(f)
    f.close()
    return data


def get_uuid():
    return str(uuid.uuid4()).replace("-", "")


def get_current_time():
    return datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")


def clean_text(text=""):
    filter_sen = "".join([chr(i) for i in range(1, 32)])
    return text.translate(str.maketrans("", "", filter_sen)).strip()


def clean_price(text=""):
    text = text.lower().replace("price", "").strip()
    if text == "list":
        text = "MSRP"
    return text


def clean_amount(text=""):
    if not text[0].isdigit():
        text = text[1:]
    return float(text.replace(",", ""))


def clean_manufacturer_sku(text=""):
    return text.split(":")[-1].strip()
