delimiters = [' ', ',', '-']
dynamic_status = {}

def make_key(first, end):
    return (first << 16) + end

def dynamic_parse(origin_sentence, trie_dic):
    first = 0
    end = len(origin_sentence) - 1

    if trie_dic is None or end <= 0:
        return False, None

    def extract(first, end):
        if first >= end:
            return True, []

        offset = 0

        # Bỏ qua các dấu phân cách (delimiters)
        while first < len(origin_sentence) and origin_sentence[first] in delimiters:
            first += 1

        sentence = origin_sentence[first:]

        while offset < len(sentence):
            word = trie_dic.extract_word(sentence, offset)
            if word == "":
                return False, []

            offset = len(word)
            next_first = first + offset

            if next_first == len(origin_sentence) - 1:
                return True, [word]

            ok, words = extract(next_first, end)

            if ok:
                words.append(word)
                return True, words

        return False, []

    return extract(first, end)