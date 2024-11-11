import stringutil
from entity import Ward, District, Province, Location, Locations, LocationType
from .distance import levenshtein_distance

WardMap = {}
DistrictMap = {}
ProvinceMap = {}

# Constants for weights
HighWeight = 3
MediumWeight = 1
LowWeight = 2
LowestWeight = 0

class WordDistance:
    def __init__(self, word: str, distance: int):
        self.word = word
        self.distance = distance

class Node:
    def __init__(self):
        self.weight = 0
        self.height = 0
        self.value = ""
        self.is_end = False
        self.locations = []
        self.children = {}

    def __repr__(self):
        return f"Node(value={self.value}, is_end={self.is_end}, weight={self.weight}, locations={self.locations})"

class Trie:
    def __init__(self, reversed=False):
        self.root = Node()
        self.reversed = reversed
        self.ward_map = {}
        self.district_map = {}
        self.province_map = {}

    def add_word_with_type_and_id(self, word, location_type, id, weight):
        if self.reversed:
            word = word[::-1]

        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = Node()
            child = node.children[char]
            child.height = node.height + 1
            child.value = char
            node = child

        location = Location(word, location_type, id, weight)
        node.locations.append(location)
        node.is_end = True
        # node.weight = weight

    def build_trie_with_wards(self, wards: list[Ward]):
        name = ""
        for ward in wards:
            # Remove prefix for ward, district, and province
            no_prefix_ward_name = stringutil.remove_ward_prefix(ward.name)
            no_prefix_district_name = stringutil.remove_district_prefix(ward.district)
            no_prefix_province_name = stringutil.remove_province_prefix(ward.province)

            no_prefix_no_accent_ward_name = stringutil.standardize_location(no_prefix_ward_name)
            no_prefix_no_accent_district_name = stringutil.standardize_location(no_prefix_district_name)

            ward.no_prefix_name = no_prefix_ward_name
            WardMap[ward.code] = ward
            DistrictMap[ward.district_code] = District(ward.district, no_prefix_district_name, ward.district_code, ward.province_code)

            ProvinceMap[ward.province_code] = Province(ward.province, no_prefix_province_name, ward.province_code)

            ward_name = stringutil.remove_vietnamese_accents(ward.name).lower()
            self.add_word_with_type_and_id(ward_name, LocationType.WARD, ward.code, HighWeight)

            if ward_name.startswith("xa "):
                name = ward_name[3:]
                if name != "thanh":
                    self.add_word_with_type_and_id(name, LocationType.WARD, ward.code, LowWeight)

                aliases = ["x", "x ", "x.", "x. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.WARD, ward.code, MediumWeight)

            if ward_name.startswith("phuong "):
                name = ward_name[7:]
                if not stringutil.is_integer(name) and len(name) > 3:
                    if no_prefix_ward_name == no_prefix_district_name or no_prefix_no_accent_ward_name == no_prefix_no_accent_district_name:
                        self.add_word_with_type_and_id(name, LocationType.WARD, ward.code, LowestWeight)
                    else:
                        self.add_word_with_type_and_id(name, LocationType.WARD, ward.code, LowWeight)

                aliases = ["p ", "p.", "p. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.WARD, ward.code, MediumWeight)

                alias = "p"
                if stringutil.is_integer(name):
                    self.add_word_with_type_and_id(alias + name, LocationType.WARD, ward.code, MediumWeight)
                    num_alias = stringutil.number_ward_alias_map.get(name)
                    if num_alias:
                        self.add_word_with_type_and_id(alias + num_alias, LocationType.WARD, ward.code, MediumWeight)

            if ward_name.startswith("thi tran "):
                name = ward_name[9:]
                if len(name) > 4:
                    if no_prefix_ward_name == no_prefix_district_name:
                        self.add_word_with_type_and_id(name, LocationType.WARD, ward.code, LowestWeight)
                    else:
                        self.add_word_with_type_and_id(name, LocationType.WARD, ward.code, LowWeight)

                aliases = ["tt", "tt ", "tt.", "tt. ", "t.t ", "t.t. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.WARD, ward.code, MediumWeight)

        for district in DistrictMap.values():
            no_prefix_district_name = stringutil.remove_district_prefix(district.name)
            no_prefix_province_name = stringutil.remove_province_prefix(ProvinceMap[district.province_code].name)

            district_name = stringutil.remove_vietnamese_accents(district.name).lower()
            self.add_word_with_type_and_id(district_name, LocationType.DISTRICT, district.code, HighWeight)

            if district_name.startswith("thi xa "):
                name = district_name[7:]
                if no_prefix_district_name == no_prefix_province_name:
                    self.add_word_with_type_and_id(name, LocationType.DISTRICT, district.code, LowestWeight)
                else:
                    self.add_word_with_type_and_id(name, LocationType.DISTRICT, district.code, LowWeight)

                aliases = ["tx", "tx ", "tx. ", "t.x ", "t.x. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.DISTRICT, district.code, MediumWeight)

            if district_name.startswith("thanh pho "):
                name = district_name[10:]
                if name != "vinh":
                    self.add_word_with_type_and_id(name, LocationType.DISTRICT, district.code, LowWeight)

                aliases = ["tp", "tp ", "tp. ", "t ", "t. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.DISTRICT, district.code, MediumWeight)

            if district_name.startswith("quan "):
                name = district_name[5:]
                if not stringutil.is_integer(name):
                    self.add_word_with_type_and_id(name, LocationType.DISTRICT, district.code, LowWeight)

                aliases = ["q", "q ", "q.", "q. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.DISTRICT, district.code, MediumWeight)

            if district_name.startswith("huyen "):
                name = district_name[6:]
                if name != "thanh hoa":
                    self.add_word_with_type_and_id(name, LocationType.DISTRICT, district.code, LowWeight)

                aliases = ["h ", "h.", "h. "]
                for alias in aliases:
                    self.add_word_with_type_and_id(alias + name, LocationType.DISTRICT, district.code, MediumWeight)

        for province in ProvinceMap.values():
            province_name = stringutil.remove_vietnamese_accents(province.name).lower()
            self.add_province_with_prefix_alias(province_name, province.code)

    def is_end(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end


    def extract_word(self, sentence, offset=0):
        node = self.root
        for i, char in enumerate(sentence):
            if i > offset and node.is_end:
                return sentence[:node.height], node

            if char not in node.children:
                return "", None

            node = node.children[char]

        return (sentence[:node.height], node) if node.is_end else ("", None)

    def skip(self, sentence):
        skip = 0
        while skip < len(sentence):
            result, _ = self.extract_word(sentence[skip:], 0)
            if result:
                break
            skip += 1
        return skip

    def extract_word_with_auto_correct(self, word):
        if self.reversed:
            word = word[::-1]
        node = self.root

        for char in word:
            if char not in node.children:
                break
            node = node.children[char]

        prefix = word[:node.height]
        if node.height > 2:
            distances = []
            words = self.find_words_with_prefix(prefix)
            for w in words:
                distance = levenshtein_distance(word, w)
                distances.append((w, WordDistance(w, distance)))

            distances.sort(key=lambda x: x[1])
            return distances[0][0], distances[0][1], node
        return "", None, None

    def find_words_with_prefix(self, prefix):
        node = self.search_prefix(prefix)
        words = []
        if node:
            self.dfs(node, prefix, words)
        return words

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def dfs(self, node, prefix, words):
        if node.is_end:
            words.append(prefix)
        for char, child in node.children.items():
            self.dfs(child, prefix + char, words)

    def print_trie(self):
        def dfs(node, prefix):
            if node.is_end:
                # Use Locations from entity and call its to_string() method
                print(f"{prefix}, {Locations(node.locations).to_string()}")
            for char, child in node.children.items():
                dfs(child, prefix + char)

        print("------------Start print trie ----------")
        dfs(self.root, "")
        print("------------End print trie ----------")

    def print_with_prefix(self, prefix):
        node = self.search_prefix(prefix)

        def dfs(node, prefix):
            if node.is_end:
                print(f"{prefix}, {Locations(node.locations).to_string()}")
            for char, child in node.children.items():
                dfs(child, prefix + char)

        print("------------Start print trie ----------")
        dfs(node, prefix)
        print("------------End print trie ----------")

    def add_province_with_prefix_alias(self, province_name, province_code):
        trim_name = ""
        trim_names = []
        prefixes = []

        # Add the full province name with high weight
        self.add_word_with_type_and_id(province_name, LocationType.PROVINCE, province_code, HighWeight)

        # Check for "thanh pho" prefix and set prefix variations
        if province_name.startswith("thanh pho "):
            trim_name = province_name.removeprefix("thanh pho ")
            prefixes = ["", "thanh pho ", "tp", "tp ", "tp.", "tp. ", "t.", "t. ", "t.p", "t.p "]

        # Check for "tinh" prefix and set prefix variations
        elif province_name.startswith("tinh "):
            trim_name = province_name.removeprefix("tinh ")
            prefixes = ["", "tinh ", "t", "t.", "t. "]

        # Generate aliases for the trimmed name
        trim_names = get_province_alias(trim_name)

        # Add each combination of prefix and trimmed alias to the trie
        for tname in trim_names:
            for prefix in prefixes:
                if prefix:
                    self.add_word_with_type_and_id(prefix + tname, LocationType.PROVINCE, province_code, MediumWeight)
                else:
                    self.add_word_with_type_and_id(tname, LocationType.PROVINCE, province_code, LowWeight)

def get_province_alias(province_name):
    alias = province_name.replace(" ", "")
    return [province_name, alias]
