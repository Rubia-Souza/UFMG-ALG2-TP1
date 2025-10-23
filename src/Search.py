import re
import os
from src.CompressedTrie import CompressedTrie
from src.Indexation import create_compressed_trie_from_file, create_compressed_trie_from_reversed_index

def search_in_reversed_index(expression: str) -> list[dict] | None:
    def remove_and_or(expression: str) -> str:
        return re.sub(r'\b(AND|OR)\b', '', expression).strip()
    
    def get_searched_words(expression: str) -> list[str]:
        expression_without_operators: str = remove_and_or(expression)
        expression_lowered: str = expression_without_operators.lower()
        words: list[str] = re.findall(r'([a-z0-9\'%$£\-.,:]+)', expression_lowered)
        return words
    
    def parse_expression_to_boolean(expression: str) -> str:
        expression_with_symbols: str = expression.replace(' AND ', ' & ').replace(' OR ', ' | ')
        expression_lowered: str = expression_with_symbols.lower()
        expression_boolean: str = re.sub(r'([a-z0-9\'%$£\-.,:]+)', r'trie.search("\1")', expression_lowered)
        return expression_boolean
    
    def get_all_possible_search_files(global_trie: CompressedTrie, searched_words: list[str]) -> set[str]:
        files: set[str] = set()
        for word in searched_words:
            word_info = global_trie.get_word_info(word)
            if word_info is not None:
                files.update(word_info.documents)
        return files
    
    def filter_files_by_expression(all_files: set[str], expression: str) -> set[str]:
        boolean_expression: str = parse_expression_to_boolean(expression)

        target_files: set[str] = set()
        for file_path in all_files:
            local_file_trie: CompressedTrie | None = create_compressed_trie_from_file(file_path)
            if local_file_trie is None:
                continue

            try:
                if eval(boolean_expression, globals(), {'trie': local_file_trie}):
                    target_files.add(file_path)
            except Exception as e:
                print(f"[ERROR]: Could not evaluate boolean expression ({boolean_expression}) for file {file_path}: {e}")
                continue
            finally:
                del local_file_trie
        
        return target_files

    def build_results_from_files(target_files: set[str], searched_words: list[str], global_trie: CompressedTrie) -> list[dict]:
        def extract_title(file_path: str) -> str:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    first_line: str = file.readline().strip()
                    return first_line
            except Exception as e:
                print(f"[ERROR]: Could not read file {file_path} to extract title: {e}")
                return "Title not found"
            
        def extract_snippet(file_path: str, searched_words: list[str]) -> str:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content: str = file.read()

                    pattern: re.Pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in searched_words) + r')\b', re.IGNORECASE)
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

        def calculate_z_score(file_path: str, searched_words: list[str], global_trie: CompressedTrie) -> float:
            mean: float = global_trie.calculate_mean_words_frequency()
            std_dev: float = global_trie.calculate_standard_deviation_words_frequency(mean)

            searched_words_z_scores: list[float] = []
            for word in searched_words:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content: str = file.read()
                    word_count_in_file: int = len(re.findall(r'\b' + re.escape(word) + r'\b', content, re.IGNORECASE))
                    z_score: float = 0.0
                    if std_dev > 0:
                        z_score = (word_count_in_file - mean) / std_dev
                    else:
                        z_score = 0.0
                    searched_words_z_scores.append(z_score)

            if(len(searched_words_z_scores) > 0):
                return sum(searched_words_z_scores) / len(searched_words_z_scores)
            return 0.0

        results: list[dict] = []
        for file_path in target_files:
            title: str = extract_title(file_path)
            snippet: str = extract_snippet(file_path, searched_words)
            z_score: float = calculate_z_score(file_path, searched_words, global_trie)
            results.append({
                "title": title,
                "snippet": snippet,
                "z_score": z_score,
            })

        results.sort(key=lambda x: x['z_score'], reverse=True)
        return results

    global_trie: CompressedTrie = create_compressed_trie_from_reversed_index()
    searched_words: list[str] = get_searched_words(expression)

    files_to_search: set[str] = get_all_possible_search_files(global_trie, searched_words)
    target_files: set[str] = filter_files_by_expression(files_to_search, expression)

    return build_results_from_files(target_files, searched_words, global_trie)

    
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
    pattern: re.Pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in re.findall(r'([a-zA-Z0-9\'%$£\-:]+)', searched_words)) + r')\b', re.IGNORECASE)
    marked_content: str = pattern.sub(r'<span class="highlight">\1</span>', content)
    return marked_content

