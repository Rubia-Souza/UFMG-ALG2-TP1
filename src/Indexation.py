import os
from src.CompressedTrie import CompressedTrie

def create_compressed_trie_from_file(file_path):
    trie = CompressedTrie()
    with open(file_path, 'r') as file:
        for line in file:
            cleaned_line = line.strip()
            words = cleaned_line.split()
            for word in words:
                trie.insert(word)
    return trie

def save_trie_in_file(trie, file_path):
    with open(file_path, 'w') as file:
        trie_data = trie.serialize()
        file.write(trie_data)

def create_compressed_tries_to_folder(folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    for filename in os.listdir(folder_path):
        output_file_name = f"{os.path.splitext(filename)[0]}_trie.txt"
        output_file_path = os.path.join(output_folder_path, output_file_name)
        if os.path.isfile(output_file_path):
            continue

        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            trie = create_compressed_trie_from_file(file_path)
            save_trie_in_file(trie, output_file_path)

if __name__ == "__main__":
    print(f"[LOG]: Creating Compressed Tries to folder business.")
    create_compressed_tries_to_folder('noticias/business', 'inverted_index/business')

    print(f"[LOG]: Creating Compressed Tries to folder entertainment.")
    create_compressed_tries_to_folder('noticias/entertainment', 'inverted_index/entertainment')

    print(f"[LOG]: Creating Compressed Tries to folder politics.")
    create_compressed_tries_to_folder('noticias/politics', 'inverted_index/politics')

    print(f"[LOG]: Creating Compressed Tries to folder sport.")
    create_compressed_tries_to_folder('noticias/sport', 'inverted_index/sport')

    print(f"[LOG]: Creating Compressed Tries to folder tech.")
    create_compressed_tries_to_folder('noticias/tech', 'inverted_index/tech')
