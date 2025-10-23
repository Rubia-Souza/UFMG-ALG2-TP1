import re
import os
from src.CompressedTrie import CompressedTrie
from src.Indexation import create_compressed_trie_from_file

def search_in_reversed_index(expression: str) -> list[dict] | None:
    def parse_expression(expression: str) -> str:
        def remove_ponctuation(expression: str) -> str:
            word_without_ponctuation_start: str = re.sub(r'^[.,;:!?\[\]{}"`~^<>/\\|]+', '', expression)
            word_without_ponctuation_end: str = re.sub(r'[.,;:!?\[\]{}"`~^<>/\\|]+$', '', word_without_ponctuation_start)

            return word_without_ponctuation_end
        
        def lowercase_search_terms(expression: str) -> str:
            return re.sub(r'\b([a-zA-Z]+)\b', lambda m: m.group(1).lower() if m.group(1) not in ['AND', 'OR'] else m.group(1), expression)
        
        def surround_words_with_trie_search(expression: str) -> str:
            return re.sub(r'([a-z0-9\'%$£\-.,:]+)', r'trie.search("\1")', expression)
        
        def replace_logical_operators(expression: str) -> str:
            return expression.replace('AND', '&').replace('OR', '|')
        
        expression_without_punctuation: str = remove_ponctuation(expression)
        expression_lowercased: str = lowercase_search_terms(expression_without_punctuation)
        expression_with_trie: str = surround_words_with_trie_search(expression_lowercased)
        expression_with_python_ops: str = replace_logical_operators(expression_with_trie)

        return expression_with_python_ops    

    def build_response_object(list_of_matched_files: list[str], searched_words: str) -> list[dict]:
        def extract_title_from_file(file_path: str) -> str:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    first_line: str = file.readline().strip()
                    return first_line
            except Exception as e:
                print(f"[ERROR]: Could not read file {file_path} to extract title: {e}")
                return "Title not found"
        
        def extract_snippet_from_file(file_path: str, searched_words: str) -> str:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content: str = file.read()
                    # Remove and and or from searched_words
                    searched_words = re.sub(r'\b(AND|OR)\b', '', searched_words).strip()
                    # Find the first occurrence of any of the searched words
                    pattern: re.Pattern = re.compile(r'(' + '|'.join(re.escape(word) for word in re.findall(r'[a-zA-Z0-9\'%$£\-.,:]+', searched_words)) + r')', re.IGNORECASE)
                    match: re.Match | None = pattern.search(content)
                    if(match):
                        start: int = max(match.start() - 80, 0)
                        end: int = min(match.end() + 80, len(content))
                        snippet: str = content[start:end].strip()
                        if(start > 0):
                            snippet = '...' + snippet
                        if(end < len(content)):
                            snippet = snippet + '...'
                        snippet = pattern.sub(r'<span class="highlight">\1</span>', snippet)
                        return snippet
                    else:
                        return "No snippet available"
            except Exception as e:
                print(f"[ERROR]: Could not read file {file_path} to extract snippet: {e}")
                return "Snippet not found"

        def find_z_score(file_path: str, searched_words: str) -> float:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content: str = file.read().lower()
                    # Remove and and or from searched_words
                    searched_words = re.sub(r'\b(AND|OR)\b', '', searched_words).strip()
                    # Find all words in searched_words
                    words: list[str] = re.findall(r'\b[a-zA-Z0-9]+\b', searched_words.lower())
                    # Find all words in content
                    total_words: int = len(re.findall(r'\b[a-zA-Z]+\b', content))
                    if(total_words == 0):
                        return 0.0
                    count: int = sum(content.count(word) for word in words)
                    z_score: float = count / total_words
                    return round(z_score, 4)
            except Exception as e:
                print(f"[ERROR]: Could not read file {file_path} to calculate z-score: {e}")
                return 0.0

        response: list[dict] = []

        for file_path in list_of_matched_files:
            title: str = extract_title_from_file(file_path)
            snippet: str = extract_snippet_from_file(file_path, searched_words)
            z_score: float = find_z_score(file_path, searched_words)

            response.append({
                "title": title,
                "snippet": snippet,
                "z_score": z_score
            })

        response.sort(key = lambda x: x['z_score'], reverse = True)
        return response
    
    parsed_expression: str = parse_expression(expression)
    list_of_results: list[str] = []

    for category in ['business', 'entertainment', 'politics', 'sport', 'tech']:
        folder_path: str = f'inverted_index/{category}'
        if(not os.path.exists(folder_path)):
            print(f"[WARNING]: Folder {folder_path} does not exist. Skipping.")
            continue

        for filename in os.listdir(folder_path):
            if(filename.endswith('_trie.txt')):
                file_path: str = os.path.join(folder_path, filename)
                trie: CompressedTrie | None = create_compressed_trie_from_file(file_path)
                try:
                    if(eval(parsed_expression, globals(), {'trie': trie})):
                        base_file_name: str = filename.replace('_trie.txt', '.txt')
                        base_file_path: str = os.path.join('noticias', category, base_file_name)
                        list_of_results.append(base_file_path)
                except Exception as e:
                    print(f"[ERROR]: Error evaluating expression ({parsed_expression}) in file {filename}: {e}")
                    continue
                finally:
                    del trie

    if len(list_of_results) > 0:
        return build_response_object(list_of_results, expression)
    else:
        return None
    
def find_news_by_title(title: str) -> dict | None:
    for category in ['business', 'entertainment', 'politics', 'sport', 'tech']:
        folder_path: str = f'noticias/{category}'
        if(not os.path.exists(folder_path)):
            print(f"[WARNING]: Folder {folder_path} does not exist. Skipping.")
            continue

        for filename in os.listdir(folder_path):
            if(not filename.endswith('.txt')):
                continue

            file_path: str = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    first_line: str = file.readline().strip()
                    if first_line == title:
                        content: str = file.read()
                        return {"title": first_line, "content": content}
            except Exception as e:
                print(f"[ERROR]: Could not read file {file_path} to find news by title: {e}")
                continue
    return None

def mark_searched_words_in_content(content: str, searched_words: str) -> str:
    searched_words = re.sub(r'\b(AND|OR)\b', '', searched_words).strip()
    pattern: re.Pattern = re.compile(r'(' + '|'.join(re.escape(word) for word in re.findall(r'([a-zA-Z0-9\'%$£\-:]+)', searched_words)) + r')', re.IGNORECASE)
    marked_content: str = pattern.sub(r'<span class="highlight">\1</span>', content)
    return marked_content