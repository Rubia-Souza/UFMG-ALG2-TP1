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