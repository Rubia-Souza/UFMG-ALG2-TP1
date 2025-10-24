import os
from src.CompressedTrie import CompressedTrie
from src.Cleaner import clean_word_indexation

def create_compressed_trie_from_file(file_path: str) -> CompressedTrie | None:
    trie: CompressedTrie = CompressedTrie()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line: str = line.strip()
                words: list[str] = cleaned_line.split()
                for word in words:
                    word = clean_word_indexation(word)
                    trie.insert(word, file_path)
        return trie
    except Exception as e:
        print(f"[ERROR]: Could not create trie from file {file_path}. Exception: {e}")
        return None

def create_compressed_trie_from_reversed_index() -> CompressedTrie:
    data: list[dict] = []
    reversed_index_file_path: str = 'inverted_index/full_trie.txt'
    try:
        with open(reversed_index_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                entry: dict = eval(line.strip())
                data.append(entry)
    except Exception as e:
        print(f"[ERROR]: Could not read reversed index file {reversed_index_file_path}. Exception: {e}")

    trie: CompressedTrie = CompressedTrie()
    trie.create_from_json(data)
    return trie

def create_compressed_trie_from_raw_files() -> None:
    output_file_path: str = 'inverted_index/full_trie.txt'
    if(os.path.isfile(output_file_path)):
        return

    trie: CompressedTrie = CompressedTrie()

    for category in ['business', 'entertainment', 'politics', 'sport', 'tech']:
        files_folder: str = f'noticias/{category}'

        if (not os.path.exists(files_folder)):
            print(f"[WARNING]: Folder {files_folder} does not exist. Skipping.")
            continue

        for filename in os.listdir(files_folder):
            if filename.endswith('.txt'):
                file_path: str = os.path.join(files_folder, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            cleaned_line: str = line.strip()
                            words: list[str] = cleaned_line.split()
                            for word in words:
                                word = clean_word_indexation(word)
                                trie.insert(word, file_path)
                except Exception as e:
                    print(f"[ERROR]: Could not read file {file_path} to insert words into trie: {e}")
                    continue

    with open(output_file_path, 'w', encoding='utf-8') as file:
        trie_as_json: list[dict] = trie.jsonafy()
        for entry in trie_as_json:
            file.write(f"{entry}\n")


if __name__ == "__main__":
    create_compressed_trie_from_raw_files()
