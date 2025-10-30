class WordInfo:
    def __init__(self, word: str):
        self.word: str = word
        self.frequency: int = 0
        self.documents: set[str] = set()

class TrieNode:
    def __init__(self, prefix: str = ''):
        self.prefix: str = prefix
        self.children: list[TrieNode] = []
        self.is_end_of_word: bool = False
        self.word_info: WordInfo = WordInfo(prefix)

class CompressedTrie:
    def __init__(self):
        self.root: TrieNode = TrieNode()

    def __common_prefix_length(self, target_1: str, target_2: str) -> int:
        length: int = 0
        while(length < len(target_1) and length < len(target_2) and target_1[length].lower() == target_2[length].lower()):
            length += 1
        return length
    
    def insert(self, word: str, file_path: str) -> None:
        if (not word):
            return
        
        current_node: TrieNode = self.root
        index: int = 0

        while(index < len(word)):
            actual_character: str = word[index]

            child_starts_with_actual_character: bool = False
            next_node: TrieNode | None = None
            for child in current_node.children:
                if(child.prefix[0] == actual_character):
                    child_starts_with_actual_character = True
                    next_node = child
                    break
            
            if(not child_starts_with_actual_character):
                new_node: TrieNode = TrieNode(word[index:])
                new_node.is_end_of_word = True
                new_node.word_info.frequency += 1
                new_node.word_info.documents.add(file_path)
                current_node.children.append(new_node)
                return

            current_node = next_node
            common_prefix_length: int = self.__common_prefix_length(current_node.prefix, word[index:])
            if(common_prefix_length < len(current_node.prefix)):
                split_node: TrieNode = TrieNode(current_node.prefix[common_prefix_length:])
                split_node.children = current_node.children
                split_node.is_end_of_word = current_node.is_end_of_word
                split_node.word_info = current_node.word_info

                current_node.prefix = current_node.prefix[:common_prefix_length]
                current_node.children = [split_node]
                current_node.is_end_of_word = False
                current_node.word_info = WordInfo(current_node.prefix)

            index += common_prefix_length
            if(index == len(word)):
                current_node.is_end_of_word = True
                current_node.word_info.frequency += 1
                current_node.word_info.documents.add(file_path)
                return
                

    def search(self, word: str) -> bool:
        current_node: TrieNode = self.root
        index: int = 0

        while(index < len(word)):
            actual_character: str = word[index]

            child_starts_with_actual_character: bool = False
            next_node: TrieNode | None = None
            for child in current_node.children:
                if(child.prefix[0] == actual_character):
                    child_starts_with_actual_character = True
                    next_node = child
                    break
            
            if(not child_starts_with_actual_character):
                return False

            current_node = next_node
            common_prefix_length: int = self.__common_prefix_length(current_node.prefix, word[index:])
            if(common_prefix_length != len(current_node.prefix)):
                return False

            index += common_prefix_length
            if(index == len(word)):
                return current_node.is_end_of_word
    
        return False

    def get_word_info(self, word: str) -> WordInfo | None:
        current_node: TrieNode = self.root
        index: int = 0

        while(index < len(word)):
            actual_character: str = word[index]

            child_starts_with_actual_character: bool = False
            next_node: TrieNode | None = None
            for child in current_node.children:
                if(child.prefix[0] == actual_character):
                    child_starts_with_actual_character = True
                    next_node = child
                    break
            
            if(not child_starts_with_actual_character):
                return None

            current_node = next_node
            common_prefix_length: int = self.__common_prefix_length(current_node.prefix, word[index:])
            if(common_prefix_length != len(current_node.prefix)):
                return None

            index += common_prefix_length
            if(index == len(word)):
                if(current_node.is_end_of_word):
                    return current_node.word_info
                else:
                    return None
    
        return None
    
    def print_all_words(self, node: TrieNode | None = None, current_prefix: str = '') -> None:
        if node is None:
            node = self.root

        if node.is_end_of_word:
            print(current_prefix + node.prefix)
            print("   Frequency:", node.word_info.frequency)
            print("   Documents:", node.word_info.documents)

        for child in node.children:
            self.print_all_words(child, current_prefix + node.prefix)

    def print_trie(self, node: TrieNode | None = None, level: int = 0) -> None:
        if node is None:
            node = self.root

        print(' ' * level + repr(node.prefix) + ('*' if node.is_end_of_word else ''))

        for child in node.children:
            self.print_trie(child, level + 2)
    
    def jsonafy(self) -> list[dict]:
        result: list[dict] = []
        def _jsonafy(node: TrieNode, current_prefix: str) -> None:
            if(node.is_end_of_word):
                result.append({
                    'word': current_prefix + node.prefix,
                    'frequency': node.word_info.frequency,
                    'documents': list(node.word_info.documents)
                })
            for child in node.children:
                _jsonafy(child, current_prefix + node.prefix)
        
        _jsonafy(self.root, '')
        return result
    
    def create_from_json(self, data: list[dict]) -> None:
        for entry in data:
            word: str = entry['word']
            frequency: int = entry['frequency']
            documents: list[str] = entry['documents']

            current_node: TrieNode = self.root
            index: int = 0

            while(index < len(word)):
                actual_character: str = word[index]

                child_starts_with_actual_character: bool = False
                next_node: TrieNode | None = None
                for child in current_node.children:
                    if(child.prefix[0] == actual_character):
                        child_starts_with_actual_character = True
                        next_node = child
                        break
                
                if(not child_starts_with_actual_character):
                    new_node: TrieNode = TrieNode(word[index:])
                    new_node.is_end_of_word = True
                    new_node.word_info.frequency = frequency
                    new_node.word_info.documents = set(documents)
                    current_node.children.append(new_node)
                    break

                current_node = next_node
                common_prefix_length: int = self.__common_prefix_length(current_node.prefix, word[index:])
                if(common_prefix_length < len(current_node.prefix)):
                    split_node: TrieNode = TrieNode(current_node.prefix[common_prefix_length:])
                    split_node.children = current_node.children
                    split_node.is_end_of_word = current_node.is_end_of_word
                    split_node.word_info = current_node.word_info

                    current_node.prefix = current_node.prefix[:common_prefix_length]
                    current_node.children = [split_node]
                    current_node.is_end_of_word = False
                    current_node.word_info = WordInfo(current_node.prefix)

                index += common_prefix_length
                if(index == len(word)):
                    current_node.is_end_of_word = True
                    current_node.word_info.frequency = frequency
                    current_node.word_info.documents = set(documents)
                    break