import re
from typing import List, Dict
from .trie import WardMap, DistrictMap, HighWeight, MediumWeight, LowWeight, LowestWeight
from entity import Location, LocationType


def filter_location(locations: List[Location], words: List[str], sentence: str) -> List[Location]:
    if not locations:
        return []

    words_count_map = count_words(words, sentence)

    result = []
    location_map, ward_ids, district_ids, province_ids = simplify(locations)

    # filter province
    filter_province_locations = []
    province_id = ""
    if len(province_ids) == 1:
        filter_province_locations.append(location_map[province_ids[0]])
    elif len(province_ids) > 0:
        filter_province_locations = [location_map[id_] for id_ in province_ids]
        filter_province_locations.sort(key=lambda location: location.weight, reverse=True)

    # choose only 1 province
    if filter_province_locations:
        province_id = filter_province_locations[0].id
        result.append(location_map[province_id])
        words_count_map[location_map[province_id].name] -= 1

    # filter district
    filter_district_locations = []
    district_id = ""
    if len(district_ids) == 1:
        filter_district_locations.append(location_map[district_ids[0]])
    elif len(district_ids) > 1:
        for id_ in district_ids:
            district = DistrictMap.get(id_)
            if district and district.province_code == province_id and words_count_map.get(location_map[id_].name, 0) > 0:
                words_count_map[location_map[id_].name] -= 1
                filter_district_locations.append(location_map[id_])

        filter_district_locations.sort(key=lambda location: location.weight, reverse=True)
        if not filter_district_locations:
            filter_district_locations.append(location_map[district_ids[0]])

    # choose only 1 district
    if filter_district_locations:
        district_id = district_ids[0]
        result.append(filter_district_locations[0])
        words_count_map[filter_district_locations[0].name] -= 1

    # filter ward
    filter_ward_locations = []
    if ward_ids:
        # filter by both province and district if possible
        if province_id and district_id:
            for id_ in ward_ids:
                ward = WardMap.get(id_)
                if ward and ward.province_code == province_id and ward.district_code == district_id and words_count_map.get(location_map[id_].name, 0) > 0:
                    filter_ward_locations.append(location_map[id_])
        # filter wards by province
        if not filter_ward_locations:
            for id_ in ward_ids:
                ward = WardMap.get(id_)
                if ward and ward.province_code == province_id and words_count_map.get(location_map[id_].name, 0) > 0:
                    filter_ward_locations.append(location_map[id_])
        # filter wards by district
        if not filter_ward_locations:
            for id_ in ward_ids:
                ward = WardMap.get(id_)
                if ward and ward.district_code in district_ids and words_count_map.get(location_map[id_].name, 0) > 0:
                    filter_ward_locations.append(location_map[id_])

        # if we can't filter ward by district, get the first one and still have word count
        if not filter_ward_locations and words_count_map.get(location_map[ward_ids[0]].name, 0) > 0 and location_map[ward_ids[0]].weight > LowWeight:
            filter_ward_locations.append(location_map[ward_ids[0]])
        elif len(filter_ward_locations) > 1:
            filter_ward_locations.sort(key=lambda location: location.weight, reverse=True)

    # choose only 1 ward
    if filter_ward_locations:
        if len(filter_ward_locations) == 1 or filter_ward_locations[0].weight != filter_ward_locations[1].weight:
            result.append(filter_ward_locations[0])
            words_count_map[filter_ward_locations[0].name] -= 1
        else:
            result.append(filter_ward_locations[1])
            words_count_map[filter_ward_locations[1].name] -= 1

    return result

def count_words(words: List[str], sentence: str) -> Dict[str, int]:
    return {word: find_occurrences(sentence, word) for word in words}

def find_occurrences(big: str, small: str) -> int:
    return len(re.findall(re.escape(small), big))

def simplify(locations: List[Location]) -> (Dict[str, Location], List[str], List[str], List[str]):
    location_map = {loc.id: loc for loc in locations}
    province_ids = [loc.id for loc in locations if loc.location_type == LocationType.PROVINCE]
    district_ids = [loc.id for loc in locations if loc.location_type == LocationType.DISTRICT]
    ward_ids = [loc.id for loc in locations if loc.location_type == LocationType.WARD]
    return location_map, ward_ids, district_ids, province_ids