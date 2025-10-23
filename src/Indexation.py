import re
import os
from src.CompressedTrie import CompressedTrie
from src.StringUtils import remove_punctuation_from_beginning_and_end

def create_compressed_trie_from_file(file_path: str) -> CompressedTrie | None:
    trie: CompressedTrie = CompressedTrie()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line: str = line.strip()
                words: list[str] = cleaned_line.split()
                for word in words:
                    word = word.lower().strip()
                    word = remove_punctuation_from_beginning_and_end(word)
                    trie.insert(word, file_path)
        return trie
    except Exception as e:
        print(f"[ERROR]: Could not create trie from file {file_path}. Exception: {e}")
        return None

def save_trie_in_file(trie: CompressedTrie, file_path: str) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            trie_data: str = trie.serialize()
            file.write(trie_data)
    except Exception as e:
        print(f"[ERROR]: Could not save trie to file {file_path}. Exception: {e}")

def create_compressed_tries_to_folder(folder_path: str, output_folder_path: str) -> None:
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    for filename in os.listdir(folder_path):
        output_file_name: str = f"{os.path.splitext(filename)[0]}_trie.txt"
        output_file_path: str = os.path.join(output_folder_path, output_file_name)
        if os.path.isfile(output_file_path):
            continue

        if filename.endswith('.txt'):
            file_path: str = os.path.join(folder_path, filename)
            trie: CompressedTrie | None = create_compressed_trie_from_file(file_path)
            if trie is not None:
                save_trie_in_file(trie, output_file_path)
            else:
                print(f"[ERROR]: Trie creation failed for file {file_path}.")

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
                                word = word.lower().strip()
                                word = remove_punctuation_from_beginning_and_end(word)
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
