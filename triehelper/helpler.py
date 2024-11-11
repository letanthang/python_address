import csv
import json
import logging
import stringutil
from entity import Result, Ward, TestCase
from trie import Trie
from parse import dynamic_parse

# Normalize input string
def normalize_input(input_str: str) -> str:
    input_str = input_str.lower()
    input_str = stringutil.remove_vietnamese_accents(input_str)
    return input_str

# Normalize the output result
def normalize_output(result: Result) -> Result:
    out = Result()
    
    if result.province != "":
        out.province = result.province

    if result.district != "":
        out.district = result.district

    if result.ward != "":
        # Check for number ward normalization
        if result.ward in stringutil.number_ward_normalize_map:
            out.ward = stringutil.number_ward_normalize_map[result.ward]
        else:
            out.ward = result.ward

    return out

# Classify the address using trie dictionary and reversed trie
def classify_address(input_str: str, trie_dic: Trie, reversed_trie: Trie) -> Result:
    input_str = normalize_input(input_str)
    result = dynamic_parse(input_str, trie_dic, reversed_trie)
    result = normalize_output(result)
    return result

# Import Ward data from CSV file
def import_ward_db(filename: str) -> list[Ward]:
    results = []

    # Open the CSV file
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        # Skip the header
        next(reader)

        # Process each record
        for record in reader:
            ward = Ward(
                province=record[0],
                province_code=record[1],
                district=record[2],
                district_code=record[3],
                name=record[4],
                code=record[5]
            )
            results.append(ward)

    return results

# Import test cases from a JSON file
def import_test_cases(file_name: str) -> list[TestCase]:
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            test_cases = json.load(file)
    except Exception as err:
        logging.error(f"Error reading test cases: {err}")
        raise

    return test_cases

def import_test_cases_new(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            test_cases = json.load(file)
    except Exception as err:
        logging.error(f"Error reading test cases: {err}")
        raise

    return test_cases