import unittest
from trie import Trie

class TestTrie(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()
        self.trie.insert("apple", termFrequencyCount=5, entity_type="fruit", neighbors=["apples"], canonical="Apple")

    def test_search(self):
        results = self.trie.search_with_correction("aple")
        self.assertEqual(results[0]['text'], "apple")

    def test_search_without_correction(self):
        results = self.trie.search_with_correction("aple", correct_spelling=False)
        self.assertEqual(len(results), 0)

    def test_insert_and_search(self):
        trie = Trie()
        trie.insert("apple", 5, "fruit", [], "Apple")
        trie.insert("appetite", 3, "noun", [], "Appetite")
        trie.insert("apex", 2, "noun", [], "Apex")
        trie.insert("banana", 7, "fruit", [], "Banana")

        assert trie.search("apple")[0]['text'] == "apple"
        assert trie.search("app")[0]['text'] == "apple"
        assert trie.search("ban")[0]['text'] == "banana"
        assert not trie.search("berry")

    def test_search_with_correction(self):  
        trie = Trie()
        trie.insert("apple", 5, "fruit", [], "Apple")
        trie.insert("appetite", 3, "noun", [], "Appetite")
        trie.insert("apex", 2, "noun", [], "Apex")
        trie.insert("banana", 7, "fruit", [], "Banana")

        results = trie.search_with_correction("appl")
        self.assertTrue(results and results[0]['text'] == "apple")

        results = trie.search_with_correction("banan")
        self.assertTrue(results and results[0]['text'] == "banana")

        results = trie.search_with_correction("bery")
        self.assertFalse(results)  # Expecting no results for "bery"    

    def test_update(self):
        trie = Trie()
        trie.insert("apple", 5, "fruit", [], "Apple")
        trie.update("apple", 3)
        assert trie.search("apple")[0]['termFrequencyCount'] == 8

        try:
            trie.update("berry", 2)
        except ValueError as e:
            assert str(e) == "Word 'berry' not found in trie."

if __name__ == '__main__':
    unittest.main()
