import re
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
        

        def no_accent_vietnamese(input_string):
            input_string = re.sub('[áãăắằẳẵặấầẫậàạâ]', 'a', input_string) # ạâảẩ
            # input_string = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', input_string)
            # input_string = re.sub(u'Đ', 'D', input_string)
            input_string = re.sub(u'đ', 'd', input_string)
            input_string = re.sub('[éèẻẽẹêếềểễệ]', 'e', input_string)
            # input_string = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', input_string)
            input_string = re.sub('[õọóòôốồổỗộơớờởỡợ]', 'o', input_string) # ỏ
            # input_string = re.sub('[ỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', input_string) # ÓÒ
            input_string = re.sub('[íìỉĩị]', 'i', input_string)
            # input_string = re.sub('[ÍÌỈĨỊ]', 'I', input_string)
            input_string = re.sub('[úủũưứừửữự]', 'u', input_string) # ù
            # input_string = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', input_string)
            input_string = re.sub('[ýỳỷỹỵ]', 'y', input_string)
            # input_string = re.sub('[ÝỲỶỸỴ]', 'Y', input_string)
            return input_string

        # Remove "." at the end
        processed_string = input_string[:-1] if input_string[-1] == "." else input_string
        
        # Lower string first
        processed_string = processed_string.lower()

        # Define a regex pattern to match numbers not preceded by the word "phường", "quận"
        pattern = r"(?<!quận )(?<!q)(?<!q\.)(?<!quận \d)(?<!q\d)(?<!q\.\d)(?<!phường )(?<!p)(?<!p\.)(?<!phường \d)(?<!p\d)(?<!p\.\d)\d+"

        # Replace matched numbers with an empty string
        processed_string = re.sub(pattern, "", processed_string)

        # Make list of delimiters         
        delimiters = [
                "t.x.", "t.", "t.t.", "h.",
                "thành phố", "thành fhố", "tỉnh", "tp.", "t.phố"
                "quận", "huyện", "huyên", "thị xã", "q.",  "tx",
                "phường", "xã", "thị trấn", "f.", "x.",
                "khu phố", "khóm", "thôn", "ấp",
                " ", "-", ".", ",", "/", "số"
                ]

        for d in delimiters:
            processed_string = processed_string.replace(d, "")
        processed_string = no_accent_vietnamese(processed_string)

        # return processed_string
        return processed_string


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