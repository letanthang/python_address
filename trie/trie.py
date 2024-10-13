def print_hello():
    print("Hello")

class Node:
    def __init__(self):
        self.weight = 0
        self.height = 0
        self.value = ""
        self.is_end = False
        self.children = {}

class Trie:
    def __init__(self):
        self.root = Node()

    def build_trie(self, words):
        for word in words:
            self.add_word(word)

    def add_word(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = Node()

            height = node.height
            node = node.children[char]
            node.value = char
            node.height = height + 1

        node.is_end = True

    def print_trie(self):
        def dfs(node, prefix):
            if node.is_end:
                print(prefix)  # Print the word when reaching the end
            for char, child in node.children.items():
                dfs(child, prefix + char)  # Recursively print child nodes

        dfs(self.root, "")

    def is_end(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def extract_word(self, sentence, offset):
        node = self.root
        for i, char in enumerate(sentence):
            if i > offset and node.is_end:
                break
            if char not in node.children:
                return ""
            node = node.children[char]

        if not node.is_end:
            return ""

        return sentence[:node.height]
