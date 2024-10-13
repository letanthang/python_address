import logging
from trie import Trie
from trie import dynamic_parse

class Result:
    def __init__(self, street='', ward='', district='', city=''):
        self.street = street
        self.ward = ward
        self.district = district
        self.city = city

    def __repr__(self):
        return f"Result(street='{self.street}', ward='{self.ward}', district='{self.district}', city='{self.city}')"

def main():
    trie_dic = import_dictionary("./assets/example.txt")

    input_addresses = [
        "nguyen tri phuong, phuong 10, quan 10, tp ho chi minh",
        # "nguyen tri phuong, phuong 10, quan 10, tp ho chi minh",
        # "nguyen tri phuong, phuong 10, tp ho chi minh, quan 10",
        # "nguyen tri phuong phuong 10 tp ho chi minh quan 10",
    ]

    for address in input_addresses:
        result = classify_address(normalize_input(address), trie_dic)
        logging.info(f"final result: {result}")

def classify_address(input_string, trie_dic):
    result = Result()

    ok, words = dynamic_parse(input_string, trie_dic)
    if ok:
        log_words(words)

    return result

def normalize_input(input_string):
    return input_string.lower()

def import_dictionary(file_name):
    trie_dic = Trie()

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    trie_dic.add_word(line)
    except IOError as e:
        logging.error(f"Error opening file: {e}")

    return trie_dic

def log_words(words):
    logging.info(f"Words Count: {len(words)}")
    for i, word in enumerate(words, 1):
        logging.info(f"{i}: {word}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()