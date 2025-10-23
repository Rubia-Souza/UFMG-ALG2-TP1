from src.StringUtils import remove_special_characters, remove_special_characters_from_beginning_and_end

def clean_word(word: str) -> str:
    clean_word: str = remove_special_characters_from_beginning_and_end(word)
    clean_word = remove_special_characters(clean_word)
    clean_word = clean_word.lower()
    clean_word = clean_word.strip()
    return clean_word

def clean_expression(expression: str) -> str:
    for word in expression.split():
        if word in ['AND', 'OR', '&', '|']:
            continue

        cleaned_word: str = clean_word(word)
        expression = expression.replace(word, cleaned_word)
    
    return expression.strip()
