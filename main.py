import logging
import trie
import python_address
import parse
from entity import Result


# Simulate entity and parse (you need to implement or adjust based on actual structure)

def main():
    test_mode = 1

    if test_mode == 1:
        test_simple()
    elif test_mode == 2:
        test_with_real_cases()
    elif test_mode == 3:
        test_prebuild_trie()
    else:
        debug_trie()

def test_prebuild_trie():
    python_address.build_tries()
    result = python_address.process_address("Tiểu khu 3, thị trấn Ba Hàng, huyện Phổ Yên, tỉnh Thái Nguyên.")
    print_result(result)

def debug_trie():
    wards = python_address.import_ward_db("python_address/assets/wards.csv")
    trie_dic = trie.Trie(False)
    trie_dic.build_trie_with_wards(wards)

    sentence = "thị trấn Ba Hàng Đồi"
    sentence = python_address.normalize_input(sentence)

    word, _ = trie_dic.extract_word(sentence, 0)
    print(word)


def test_simple():
    wards = python_address.import_ward_db("python_address/assets/wards.csv")
    trie_dic = trie.Trie(False)
    trie_dic.build_trie_with_wards(wards)

    reversed_trie = trie.Trie(True)
    reversed_trie.build_trie_with_wards(wards)

    input_address = [
        "Tiểu khu 3, thị trấn Ba Hàng, huyện Phổ Yên, tỉnh Thái Nguyên.",
    ]

    for i in range(100000):
        address = input_address[0]
        result = python_address.classify_address(address, trie_dic, reversed_trie)
        if i == 0:
            print_result(result)

        if True:
            print_result(result)
            print_result(parse.CorrectedResult)  # Replace with actual corrected result logic
            log_words(parse.Words)  # Replace with actual words logic
            log_words(parse.SkipWords)  # Replace with actual skip words logic
            print("OriginLocations:", parse.OriginLocations)  # Replace with actual Locations logic
            print("Locations:", parse.Locations)  # Replace with actual Locations logic
            break


def test_with_real_cases():
    wards = python_address.import_ward_db("python_address/assets/wards.csv")
    trie_tree = trie.Trie(False)
    trie_tree.build_trie_with_wards(wards)

    reversed_trie = trie.Trie(True)
    reversed_trie.build_trie_with_wards(wards)

    cases = python_address.import_test_cases_new("python_address/assets/inputs.json")
    fail_num = 0

    for i, c in enumerate(cases):
        result = python_address.classify_address(c["text"], trie_tree, reversed_trie)
        if result.ward != c["result"]["ward"] or result.district != c["result"]["district"] or result.province != c["result"]["province"]:
            print_result(result)
            log_words(parse.Words)
            log_words(parse.SkipWords)
            print("OriginLocations:", parse.OriginLocations)
            print("Locations:", parse.Locations)
            fail_num += 1
        else:
            print(f"{i} Passed")

    print(f"Fail num: {fail_num} / {len(cases)}")


def log_result(result: Result):
    logging.info(f"Result: Province {result.province}, District {result.district}, Ward {result.ward}")


def print_result(result):
    print(f"Result: Province {result.province}, District {result.district}, Ward {result.ward}")


def log_words(words: list[str]):
    text = "|".join(words)
    print(f"Words: {text}")


if __name__ == "__main__":
    main()