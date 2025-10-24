import re

def remove_punctuation_from_beginning_and_end(word: str) -> str:
    word_without_ponctuation_start: str = re.sub(r'^[.,;:!?()\[\]\'{}"`~^<>/\\|]+', '', word)
    word_without_ponctuation_end: str = re.sub(r'[.,;:!?()\[\]\'{}"`~^<>/\\|]+$', '', word_without_ponctuation_start)

    return word_without_ponctuation_end

def remove_special_characters(word: str) -> str:
    cleaned_word: str = re.sub(r'[^a-zA-Z0-9()\'\-.,:]', '', word)
    return cleaned_word

def remove_special_characters_from_beginning_and_end_except_parentesis(word: str) -> str:
    return re.sub(r'^[^a-zA-Z0-9(]+|[^a-zA-Z0-9)]+$', '', word)

def remove_special_characters_from_beginning_and_end(word: str) -> str:
    return re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', word)