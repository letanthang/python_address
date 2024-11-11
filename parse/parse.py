from entity import Result, LocationType  # Assumes these are classes from your `entity` module
import trie  # You would need to define or import a similar Trie class
import stringutil

# Global variables
Debug = False
DebugFlag = "empty"
Words = []
OriginLocations = []
SkipWords = []
CorrectedResult = Result()
Locations = []
delimiters = {' ', ',', '-'}


def dynamic_parse(origin_sentence, trie_dic: trie.Trie, reversed_trie: trie.Trie):
    global Words, OriginLocations, SkipWords, CorrectedResult, Locations
    skip_words = []
    words = []
    locations = []
    DebugFlag = "empty"
    result = Result()

    if trie_dic is None or not origin_sentence:
        return result

    word_map = {}

    def extract(sentence):
        nonlocal skip_words, words, locations
        if not sentence:
            return

        # Skip delimiters at the start
        first = 0
        while first < len(sentence) and sentence[first] in delimiters:
            first += 1
        sentence = sentence[first:]

        # Skip words not in trie
        skip = trie_dic.skip(sentence)
        if skip > 0:
            skip_words.append(sentence[:skip])

        if skip >= len(sentence):
            return
        sentence = sentence[skip:]

        offset = 0
        while offset < len(sentence):
            word, node = trie_dic.extract_word(sentence, offset)
            if not word:
                return
            offset += len(word)

            if word not in word_map:
                word_map[word] = None
                words.append(word)
                locations.extend(node.locations)

            if offset >= len(sentence):
                return

            extract(sentence[offset:])

    extract(origin_sentence)
    print_words(words, "words")
    print_words(skip_words, "skips")

    Words = words
    OriginLocations = locations
    locations = trie_dic.filter_location(locations, words, origin_sentence)
    Locations = locations
    SkipWords = skip_words

    result = get_location_from_locations(locations)
    if result.is_complete():
        return result

    CorrectedResult = dynamic_parse_with_levenshtein(skip_words, reversed_trie)
    merge_result(CorrectedResult, result)

    return result


def dynamic_parse_with_levenshtein(skip_words, trie_dic: trie.Trie):
    result = Result()
    if not skip_words or trie_dic is None:
        return result

    corrected_words = []
    for skip_word in skip_words:
        skip_word = stringutil.remove_delimiters(skip_word)
        corrected_word, _, node = trie_dic.extract_word_with_auto_correct(skip_word)
        if corrected_word:
            corrected_words.append(corrected_word)

            sorted_locations = sorted(node.locations)
            add_location_to_result(result, sorted_locations[0])

        print_words(corrected_words, "corrected words: ")
    return result


def get_location_from_locations(locations):
    """
    This function takes a list of Location objects and creates a Result object based on them.
    """
    result = Result()
    for location in locations:
        add_location_to_result(result, location)
    return result

def add_location_to_result(result, location):
    """
    This function updates the Result object with information from a Location object
    based on the LocationType of the location.
    """
    if location.location_type == LocationType.WARD:
        result.ward = trie.WardMap[location.id].no_prefix_name
    elif location.location_type == LocationType.DISTRICT:
        result.district = trie.DistrictMap[location.id].no_prefix_name
    elif location.location_type == LocationType.PROVINCE:
        result.province = trie.ProvinceMap[location.id].no_prefix_name

def merge_result(source, destination):
    """
    This function merges two Result objects, giving preference to the `source` Result
    if a field in the `destination` Result is empty.
    """
    if source.ward and not destination.ward:
        destination.ward = source.ward
    if source.district and not destination.district:
        destination.district = source.district
    if source.province and not destination.province:
        destination.province = source.province


def print_words(words, word_type):
    """
    This function prints a list of words with a specified label, but only if Debug is set to True.
    """
    if not Debug:
        return

    text = "|".join(words)
    print(f"{word_type}: {text}")


