from src.StringUtils import remove_special_characters, remove_special_characters_from_beginning_and_end, remove_special_characters_from_beginning_and_end_except_parentesis

def clean_word(word: str) -> str:
    cleaned_word: str = remove_special_characters_from_beginning_and_end_except_parentesis(word)
    cleaned_word = remove_special_characters(cleaned_word)
    cleaned_word = cleaned_word.lower()
    cleaned_word = cleaned_word.strip()
    return cleaned_word

def clean_word_indexation(word: str) -> str:
    cleaned_word: str = remove_special_characters_from_beginning_and_end(word)
    cleaned_word = cleaned_word.lower()
    cleaned_word = cleaned_word.strip()
    return cleaned_word

def clean_expression(expression: str) -> str:
    for word in expression.split():
        if word in ['AND', 'OR', '&', '|']:
            continue

        cleaned_word: str = clean_word(word)
        expression = expression.replace(word, cleaned_word)
    
    return expression.strip()
