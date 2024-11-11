import logging
import trie
import triehelper
import parse
from entity import Result  # Importing the Result class from the entity module

# Simulate entity and parse (you need to implement or adjust based on actual structure)

def main():
    test_mode = 2

    if test_mode == 1:
        test_simple()
    elif test_mode == 2:
        test_with_real_cases()
    else:
        debug_trie()


def debug_trie():
    wards = triehelper.import_ward_db("./assets/wards.csv")
    trie_dic = trie.Trie(False)
    trie_dic.build_trie_with_wards(wards)

    sentence = "thị trấn Ba Hàng Đồi"
    sentence = triehelper.normalize_input(sentence)

    word, _ = trie_dic.extract_word(sentence, 0)
    print(word)


def test_simple():
    wards = triehelper.import_ward_db("./assets/wards.csv")
    trie_dic = trie.Trie(False)
    trie_dic.build_trie_with_wards(wards)

    reversed_trie = trie.Trie(True)
    reversed_trie.build_trie_with_wards(wards)

    input_address = [
        "Tiểu khu 3, thị trấn Ba Hàng, huyện Phổ Yên, tỉnh Thái Nguyên.",
    ]

    for i in range(1):
        address = input_address[0]
        result = triehelper.classify_address(address, trie_dic, reversed_trie)
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
    wards = triehelper.import_ward_db("./assets/wards.csv")
    trie_tree = trie.Trie(False)
    trie_tree.build_trie_with_wards(wards)

    reversed_trie = trie.Trie(True)
    reversed_trie.build_trie_with_wards(wards)

    cases = triehelper.import_test_cases_new("./assets/inputs.json")
    fail_num = 0

    for i, c in enumerate(cases):
        result = triehelper.classify_address(c["text"], trie_tree, reversed_trie)
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