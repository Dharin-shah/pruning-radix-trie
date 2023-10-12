class Node:
    def __init__(self, value=""):
        self.value = value
        self.children = []
        self.is_end_of_word = False
        self.full_text = None
        self.termFrequencyCount = 0
        self.entity_type = None
        self.nearest_neighbors = []
        self.canonical_form = None

    # Helper function to find a child node with a given prefix
    def find_child(self, prefix):
        low, high = 0, len(self.children) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.children[mid].value.startswith(prefix):
                return self.children[mid]
            elif self.children[mid].value < prefix:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def insert_child(self, child):
        index = 0
        while index < len(self.children) and self.children[index].value < child.value:
            index += 1
        self.children.insert(index, child)

    # Updated method to get neighbors
    def get_neighbors(self):
        return self.nearest_neighbors
