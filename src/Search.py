import re
import os
from CompressedTrie import CompressedTrie
from Indexation import create_compressed_trie_from_file

def search_in_reversed_index(expression):
    def parse_expression(expression):
        # Lowercase every word except AND, OR
        expression = re.sub(r'\b(AND|OR)\b', lambda m: m.group(1).upper(), expression, flags=re.IGNORECASE)
        expression = re.sub(r'\b([a-zA-Z]+)\b', lambda m: m.group(1).lower() if m.group(1).upper() not in ['AND', 'OR'] else m.group(1).upper(), expression)
        
        # Replace words with trie.search("word")
        expression_with_trie = re.sub(r'\b([a-z]+)\b', r'trie.search("\1")', expression)
        
        # Replace AND with & and OR with |
        expression_with_python_ops = expression_with_trie.replace('AND', '&').replace('OR', '|')

        return expression_with_python_ops
    
    parsed_expression = parse_expression(expression)
    list_of_results = []

    for category in ['business', 'entertainment', 'politics', 'sport', 'tech']:
        folder_path = f'inverted_index/{category}'
        if(not os.path.exists(folder_path)):
            print(f"[WARNING]: Folder {folder_path} does not exist. Skipping.")
            continue

        for filename in os.listdir(folder_path):
            if(filename.endswith('_trie.txt')):
                file_path = os.path.join(folder_path, filename)
                trie = create_compressed_trie_from_file(file_path)
                try:
                    if(eval(parsed_expression, globals(), {'trie': trie})):
                        base_file_name = filename.replace('_trie.txt', '.txt')
                        base_file_path = os.path.join('noticias', category, base_file_name)
                        list_of_results.append(base_file_path)
                except Exception as e:
                    print(f"[ERROR]: Error evaluating expression ({parsed_expression}) in file {filename}: {e}")
                    continue
                finally:
                    del trie

    if len(list_of_results) > 0:
        return build_response_object(list_of_results, expression)
    else:
        return [{"title": "No results found", "snippet": ""}]

def build_response_object(result, searched_words):
    def extract_title_from_file(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                return first_line
        except Exception as e:
            print(f"[ERROR]: Could not read file {file_path} to extract title: {e}")
            return "Title not found"
    
    def extract_snippet_from_file(file_path, searched_words):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Remove and and or from searched_words
                searched_words = re.sub(r'\b(AND|OR)\b', '', searched_words, flags=re.IGNORECASE).strip()
                # Find the first occurrence of any of the searched words
                pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in re.findall(r'\b[a-zA-Z]+\b', searched_words)) + r')\b', re.IGNORECASE)
                match = pattern.search(content)
                if(match):
                    start = max(match.start() - 80, 0)
                    end = min(match.end() + 80, len(content))
                    snippet = content[start:end].strip()
                    if(start > 0):
                        snippet = '...' + snippet
                    if(end < len(content)):
                        snippet = snippet + '...'
                    return snippet
                else:
                    return "No snippet available"
        except Exception as e:
            print(f"[ERROR]: Could not read file {file_path} to extract snippet: {e}")
            return "Snippet not found"

    def find_z_score(file_path, searched_words):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                # Remove and and or from searched_words
                searched_words = re.sub(r'\b(AND|OR)\b', '', searched_words, flags=re.IGNORECASE).strip()
                # Find all words in searched_words
                words = re.findall(r'\b[a-zA-Z]+\b', searched_words.lower())
                # Find all words in content
                total_words = len(re.findall(r'\b[a-zA-Z]+\b', content))
                if(total_words == 0):
                    return 0.0
                count = sum(content.count(word) for word in words)
                z_score = count / total_words
                return round(z_score, 4)
        except Exception as e:
            print(f"[ERROR]: Could not read file {file_path} to calculate z-score: {e}")
            return 0.0

    response = []

    for file_path in result:
        title = extract_title_from_file(file_path)
        snippet = extract_snippet_from_file(file_path, searched_words)
        z_score = find_z_score(file_path, searched_words)

        response.append({
            "title": title,
            "snippet": snippet,
            "z_score": z_score
        })

    response.sort(key=lambda x: x['z_score'], reverse=True)
    return response