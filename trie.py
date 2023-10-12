from node import Node
from utils import calculate_levenshtein_distance
from config import MAX_EDIT_DISTANCE, SEARCH_LIMIT
import heapq

class Trie:
    def __init__(self, max_edit_distance=None, search_limit=None):
        self.root = Node()
        self.max_edit_distance = max_edit_distance or MAX_EDIT_DISTANCE
        self.search_limit = search_limit or SEARCH_LIMIT

    def insert(self, word, termFrequencyCount, entity_type, neighbors, canonical):
        node = self.root
        i = 0
        while i < len(word):
            prefix = self._longest_prefix(word[i:], node)
            if not prefix:
                new_child = Node(word[i:])
                node.insert_child(new_child)
                node = new_child
                i += len(word[i:])
            else:
                child = node.find_child(prefix)
                if prefix != word[i:]:
                    # Split the node
                    split_point = len(word[i:])
                    new_node_value = prefix[split_point:]
                    old_node = child

                    new_node = Node(new_node_value)
                    new_node.children = old_node.children
                    new_node.is_end_of_word = old_node.is_end_of_word
                    new_node.full_text = old_node.full_text
                    new_node.termFrequencyCount = old_node.termFrequencyCount
                    new_node.entity_type = old_node.entity_type
                    new_node.nearest_neighbors = old_node.nearest_neighbors
                    new_node.canonical_form = old_node.canonical_form

                    node.children.remove(old_node)
                    node.insert_child(Node(prefix[:split_point]))
                    node = node.find_child(prefix[:split_point])
                    node.insert_child(new_node)

                    i += split_point
                else:
                    node = child
                    i += len(prefix)

        node.is_end_of_word = True
        node.full_text = word
        node.termFrequencyCount = termFrequencyCount
        node.entity_type = entity_type
        node.nearest_neighbors = [self.search(neighbor, limit=1)[0] for neighbor in neighbors if self.search(neighbor, limit=1)]
        node.canonical_form = canonical

    
    def print_trie(self, node=None, indent=""):
        if node is None:
            node = self.root
        print(indent + node.value + ("*" if node.is_end_of_word else ""))
        for child in node.children:
            self.print_trie(child, indent + "  ")

    
    def update(self, word, termFrequencyCount_increment):
        node = self._find_word_node(word)
        if node:
            node.termFrequencyCount += termFrequencyCount_increment
        else:
            raise ValueError(f"Word '{word}' not found in trie.")

    def _find_word_node(self, word):
        node = self.root
        i = 0
        while i < len(word):
            prefix = self._longest_prefix(word[i:], node)
            if not prefix:
                return None
            node = node.find_child(prefix)
            i += len(prefix)
        return node if node.is_end_of_word else None


    def search(self, query, limit=SEARCH_LIMIT):
        results = []
        node = self.root
        i = 0
        while i < len(query):
            prefix = self._longest_prefix(query[i:], node)
            if not prefix:
                break
            node = node.find_child(prefix)
            i += len(prefix)
        self._dfs(node, query, results, limit)
        results.sort(key=lambda x: x['termFrequencyCount'], reverse=True)
        return results[:limit]

    def _dfs(self, node, prefix, results, limit):
        if len(results) >= limit:
            return
        if node.is_end_of_word and node.full_text.startswith(prefix):
            results.append({
                "text": node.full_text,
                "termFrequencyCount": node.termFrequencyCount,
                "type": node.entity_type,
                "neighbors": [neighbor.full_text for neighbor in node.get_neighbors()],
                "canonical": node.canonical_form
            })
        for child in node.children:
            self._dfs(child, prefix, results, limit)
        
    def search_with_correction(self, query, correct_spelling=True):
        results = self.search(query, self.search_limit)
        if not results and correct_spelling:
            closest_word = self.find_closest_word(query)
            if closest_word:
                results = self.search(closest_word, self.search_limit)
        return results


    def find_closest_word(self, query):
        min_distance = float('inf')
        closest_word = None
        for word in self.all_words:
            distance = calculate_levenshtein_distance(query, word)
            if distance <= self.max_edit_distance and distance < min_distance:
                min_distance = distance
                closest_word = word
        return closest_word

    # New method to get all words in the Trie for spell correction
    @property
    def all_words(self):
        words = []

        def _collect_words(node, current_word):
            if node.is_end_of_word:
                words.append(current_word + node.value)
            for child in node.children:
                _collect_words(child, current_word + node.value)

        _collect_words(self.root, "")
        return words


    def _longest_prefix(self, word, node):
        child = node.find_child(word[0])
        if child and word.startswith(child.value):
            return child.value
        return ""