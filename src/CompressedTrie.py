import re

class TrieNode:
    def __init__(self, prefix = ''):
        self.prefix = prefix
        self.children = []
        self.is_end_of_word = False

class CompressedTrie:
    def __init__(self):
        self.root = TrieNode()
    
    def __common_prefix_length(self, target_1, target_2):
        length = 0
        while(length < len(target_1) and length < len(target_2) and target_1[length].lower() == target_2[length].lower()):
            length += 1
        return length
    
    def insert(self, word):
        current_node = self.root
        index = 0

        word = re.sub(r'[.,;:!?()\[\]{}"\'`~^<>/\\|]', '', word)

        while(index < len(word)):
            actual_character = word[index]

            child_starts_with_actual_character = False
            next_node = None
            for child in current_node.children:
                if(child.prefix[0] == actual_character):
                    child_starts_with_actual_character = True
                    next_node = child
                    break

            if(not child_starts_with_actual_character):
                new_node = TrieNode(word[index:].lower())
                new_node.is_end_of_word = True
                current_node.children.append(new_node)
                return
            
            current_node = next_node
            common_prefix_length = self.__common_prefix_length(current_node.prefix, word[index:])

            index += common_prefix_length
            if(common_prefix_length < len(current_node.prefix)):
                new_node = TrieNode(current_node.prefix[common_prefix_length:].lower())
                new_node.is_end_of_word = current_node.is_end_of_word
                new_node.children = current_node.children
                current_node.prefix = current_node.prefix[:common_prefix_length]
                current_node.children = [new_node]
                current_node.is_end_of_word = index == len(word)

    def search(self, word):
        current_node = self.root
        index = 0

        while(index < len(word)):
            actual_character = word[index]

            child_starts_with_actual_character = False
            next_node = None
            for child in current_node.children:
                if(child.prefix[0] == actual_character):
                    child_starts_with_actual_character = True
                    next_node = child
                    break
            
            if(not child_starts_with_actual_character):
                return False

            current_node = next_node
            common_prefix_length = self.__common_prefix_length(current_node.prefix, word[index:])
            if(common_prefix_length != len(current_node.prefix)):
                return False

            index += common_prefix_length
            if(index == len(word)):
                return current_node.is_end_of_word
    
        return False
        
    def print_trie(self, node = None, level = 0):
        if node is None:
            node = self.root

        print(' ' * level + repr(node.prefix) + ('*' if node.is_end_of_word else ''))

        for child in node.children:
            self.print_trie(child, level + 2)
    
    def serialize(self):
        words = []
        def _serialize(node, current_prefix):
            if(node.is_end_of_word):
                words.append(current_prefix + node.prefix)
            for child in node.children:
                _serialize(child, current_prefix + node.prefix)
        
        _serialize(self.root, '')
        return '\n'.join(words)