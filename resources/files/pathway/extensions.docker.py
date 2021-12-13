import random
import json
import os
import csv
from py_code.py_logging import py_logging


# this is an example of a function that will return a random item from a file
# https://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file
def random_line(file_name, file_path=None):
    current_dirname = os.path.dirname(__file__)
    if not file_path:
        file_path = os.path.join(current_dirname, "../", file_name)

    try:
        with open(file_path, "r") as file:
            line = next(file)
            for num, aline in enumerate(file, 2):
                if random.randrange(num):
                    continue
                line = aline
            return line
    except Exception:
        py_logging.log("File not found", "mainLog", [file_path])


def obs(quantity, unit, code, display):
    json_string = """
    {"quantity":"",
     "unit":"",
     "code": {"coding":[{
         "system": "http://snomed.info/sct",
         "code": "",
         "display": ""}]}
    }
    """
    # could be some validation and lookup logic here, but for now really simple...
    data = json.loads(json_string)
    data['quantity'] = quantity
    data['unit'] = unit
    data['code']['coding'][0]['code'] = code
    data['code']['coding'][0]['display'] = display
    return data


# functions to return delay for use in the pathway timer events
def mins(minimum, maximum):
    timing = {'quantity': random.randint(minimum, maximum), 'unit': 'minutes'}
    return timing


def hours(minimum, maximum):
    timing = {'quantity': random.randint(minimum, maximum), 'unit': 'hours'}
    return timing


# function to get example data from files
def getvalue(key=None, item=None):
    current_dirname = os.path.dirname(__file__)
    key_path = os.path.join(current_dirname, "{0}.csv".format(key))
    try:
        with open(key_path, "r") as f:
            read_key_file = csv.DictReader(f)
            for row in read_key_file:
                if str(item) == row['id']:
                    return row
    except (IOError, KeyError):
        py_logging.log("File not found", "mainLog", [key_path])
    values_path = os.path.join(current_dirname, "values.json")
    try:
        with open(values_path, "r") as read_values_file:
            data = json.load(read_values_file)
            return data[key]
    except (IOError, KeyError):
        py_logging.log("File not found", "mainLog", [values_path])


def smartonfhir():
    return {'base': 'http://fhir:8080/baseDstu3/',
            'headers': {'Content-Type': 'application/xml'},
            'include_id': True,
            'method_request': 'PUT'}


def ccri():
    return {'base': 'http://ccriserver:8186/ccri-fhir/STU3/',
            'headers': {'Content-Type': 'application/xml'},
            'include_id': False,
            'method_request': 'POST'}
