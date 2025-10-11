from CompressedTrie import CompressedTrie

if __name__ == "__main__":
    trie = CompressedTrie()
    trie.insert("computer")
    trie.insert("compute")
    trie.insert("computing")
    trie.print_trie()
    print(trie.search("computer"))  # True
    print(trie.search("compute"))   # True
    print(trie.search("computing")) # True
    print(trie.search("commute"))   # False
    print(trie.search("comp"))      # False
    trie.insert("commute")
    trie.print_trie()
    print(trie.search("commute"))   # True

    