import re

def remove_punctuation_from_beginning_and_end(word: str) -> str:
    word_without_ponctuation_start: str = re.sub(r'^[.,;:!?()\[\]\'{}"`~^<>/\\|]+', '', word)
    word_without_ponctuation_end: str = re.sub(r'[.,;:!?()\[\]\'{}"`~^<>/\\|]+$', '', word_without_ponctuation_start)

    return word_without_ponctuation_end