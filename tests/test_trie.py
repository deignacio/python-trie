# coding:utf-8
import itertools
import random
import unittest
from trie import Trie


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()

    def _square_brackets(self, key):
        return self.trie[key]

    def test_basicAssignment(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEquals(1, len(self.trie))
        self.assertEquals(3, self.trie.nodeCount())
        self.assertTrue("Foo" in self.trie)
        self.trie["Bar"] = None
        self.assertTrue("Bar" in self.trie)

    def test_basicRemoval(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        del self.trie["Foo"]
        self.assertRaises(KeyError, self._square_brackets, "Foo")
        self.assertEquals(0, len(self.trie))
        self.assertEquals(0, self.trie.nodeCount())
        self.assertFalse("Foo" in self.trie)

    def test_MixedTypes(self):
        self.trie["Foo"] = True
        self.trie[[1, 2, 3]] = True
        self.assertTrue(self.trie["Foo"])
        self.assertTrue(self.trie[[1, 2, 3]])
        self.assertTrue([1, 2, 3] in self.trie)
        self.assertTrue("Foo" in self.trie)
        del self.trie[[1, 2, 3]]
        self.assertFalse([1, 2, 3] in self.trie)

    def test_Iteration(self):
        self.trie["Foo"] = True
        self.trie["Bar"] = True
        self.trie["Grok"] = True
        for k in self.trie:
            self.assertTrue(k in self.trie)
            self.assertTrue(self.trie[k])

    def test_Addition(self):
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        t3 = t2 + self.trie
        self.assertTrue("Foo" in self.trie)
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertFalse("Foo" in t2)
        self.assertTrue("Foo" in t3)
        self.assertTrue("Food" in t3)

    def test_Subtraction(self):
        self.trie["Food"] = True
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        t3 = self.trie - t2
        t4 = t2 - self.trie
        self.assertTrue("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertTrue("Foo" in t3)
        self.assertFalse("Food" in t3)
        self.assertFalse("Foo" in t4)
        self.assertFalse("Food" in t4)

    def test_SelfAdd(self):
        self.trie["Foo"] = True
        t2 = Trie()
        t2["Food"] = True
        self.assertTrue("Foo" in self.trie)
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Food" in t2)
        self.assertFalse("Foo" in t2)
        self.trie += t2
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in self.trie)

    def test_SelfSub(self):
        self.trie["Foo"] = True
        self.trie["Food"] = True
        t2 = Trie()
        t2["Food"] = True
        self.assertTrue("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)
        self.trie -= t2
        self.assertFalse("Food" in self.trie)
        self.assertTrue("Foo" in self.trie)
        self.assertTrue("Food" in t2)

    def test_SelfGet(self):
        self.trie["Foo"] = True
        self.assertTrue(self.trie["Foo"])
        self.assertRaises(KeyError, self._square_brackets, "Food")
        self.assertEquals("Bar", self.trie.get("Food", "Bar"))
        self.assertEquals("Bar", self.trie.get("Food", default="Bar"))
        self.assertTrue(self.trie.get("Foo"))
        self.assertTrue(self.trie.get("Food") is None)

    def test_Sorted(self):
        self.trie = Trie(cmp)
        letters = "abcd"
        reverse = "dcba"
        expected = ["".join(i)
                    for i in itertools.product(letters, letters, letters)]
        reverse = itertools.product(reverse, reverse, reverse)
        for k in reverse:
            self.trie[k] = k

        self.assertEquals(expected, self.trie.keys())

    def test_SortedReverse(self):
        self.trie = Trie(cmp, reverse=True)
        letters = "abcd"
        reverse = "dcba"
        forward = ["".join(i)
                    for i in itertools.product(letters, letters, letters)]
        reverse = ["".join(i)
                   for i in itertools.product(reverse, reverse, reverse)]
        for k in forward:
            self.trie[k] = k

        self.assertEquals(reverse, self.trie.keys())
