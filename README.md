# Trie Search Library

A Python library for efficient string search and retrieval with spell correction.

## Features

- Efficient string insertion and search using a Trie (Radix Tree) data structure.
- Spell correction using Levenshtein distance.
- Configurable search limit and max edit distance for spell correction.
- Term frequency count for ranking search results.
- Support for additional metadata like entity type, neighbors, and canonical form.

## Installation

(Provide installation instructions, e.g., using pip)

## Usage

```python
from trie_search import Trie

# Create a Trie instance
trie = Trie()

# Insert words into the Trie
trie.insert("apple", 5, "fruit", [], "Apple")
trie.insert("banana", 7, "fruit", [], "Banana")

# Search for a word
results = trie.search("appl")
print(results)

# Search with spell correction
results = trie.search_with_correction("banan")
print(results)

# Update term frequency count
trie.update("apple", 3)
