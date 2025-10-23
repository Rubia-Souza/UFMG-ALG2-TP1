from CompressedTrie import CompressedTrie

if __name__ == "__main__":
    trie = CompressedTrie()
    with open('noticias/business/001.txt', 'r', encoding='utf-8') as file:
        for line in file:
            cleaned_line: str = line.strip()
            words: list[str] = cleaned_line.split()
            for word in words:
                word = word.lower().strip()
                trie.insert(word, 'noticias/business/001.txt')

    print(trie.jsonafy())

    # Example search
    trie = CompressedTrie()
    trie.insert("computer", "noticias/tech/001.txt")
    trie.insert("computation", "noticias/tech/002.txt")
    trie.insert("computing", "noticias/tech/003.txt")

    # Example search
    search_results = trie.search("computer")
    print("Search results for 'computer':", search_results)
    search_results = trie.search("computation")
    print("Search results for 'computation':", search_results)
    search_results = trie.search("computing")
    print("Search results for 'computing':", search_results)
    search_results = trie.search("comp")
    print("Search results for 'comp':", search_results)

    # Example get_word_info
    word_info = trie.get_word_info("computer")
    if word_info:
        print("Word info for 'computer':", word_info.frequency, word_info.documents)
    else:
        print("Word 'computer' not found in trie.")
    word_info = trie.get_word_info("computation")
    if word_info:
        print("Word info for 'computation':", word_info.frequency, word_info.documents)
    else:
        print("Word 'computation' not found in trie.")
    word_info = trie.get_word_info("computing")
    if word_info:
        print("Word info for 'computing':", word_info.frequency, word_info.documents)
    else:
        print("Word 'computing' not found in trie.")
    word_info = trie.get_word_info("comp")
    if word_info:
        print("Word info for 'comp':", word_info.frequency, word_info.documents)
    else:
        print("Word 'comp' not found in trie.")