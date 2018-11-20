#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 
    @author: icejoywoo
    @date: 2018/10/18
"""


class Node(object):
    __slots__ = ('has_word', 'children')

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.has_word = False
        self.children = {}


class Trie(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node()

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        current = self.root
        for i in word:
            if i not in current.children:
                current.children[i] = Node()
            current = current.children[i]
        current.has_word = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        current = self.root
        for i in word:
            if i in current.children:
                current = current.children[i]
            else:
                return False
        return current.has_word

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        current = self.root
        for i in prefix:
            if i in current.children:
                current = current.children[i]
            else:
                return False
        return True


# https://leetcode.com/problems/implement-trie-prefix-tree/
# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

if __name__ == '__main__':
    trie = Trie()

    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True

    trie.insert("app")
    assert trie.search("app") is True
