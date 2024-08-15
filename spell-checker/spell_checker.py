import sys
import re
from difflib import get_close_matches

def read_file(filename):
    # Read and return the contents of a file
    with open(filename, 'r') as file:
        return file.read()

def load_dictionary(dict_file):
    # Load words from the dictionary file into a set
    with open(dict_file, 'r') as file:
        return set(word.strip().lower() for word in file)

def extract_words_with_positions(text):
    # Split text into words and record their positions
    lines = text.split('\n')
    words_with_positions = []
    for line_num, line in enumerate(lines, 1):
        words = re.findall(r"\b[\w'']+\b|[.,!?;:\"'()—-]", line)
        start = 0
        for word in words:
            column = line.index(word, start) + 1
            words_with_positions.append((word, line_num, column))
            start = column + len(word) - 1
    return words_with_positions

def is_proper_noun(word, prev_word):
    # Check if a word is likely to be a proper noun ex) J.R.R. Tolkien, The Two Towers in deafult-file-to-check.py
    return word[0].isupper() and prev_word not in ['.', '!', '?', None]

def is_valid_contraction(word):
    # Check if a word is a valid contraction
    contractions = ["it's", "don't", "can't", "won't", "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't", "i'm", "you're", "he's", "she's", "we're", "they're"]
    return word.lower() in contractions

def suggest_corrections(word, dictionary, max_suggestions=3):
    # Suggest possible corrections for a misspelled word
    return get_close_matches(word.lower(), dictionary, n=max_suggestions, cutoff=0.6)

def get_context(words_with_positions, index, context_size=3):
    # Get surrounding context for a word
    start = max(0, index - context_size)
    end = min(len(words_with_positions), index + context_size + 1)
    return ' '.join(word[0] for word in words_with_positions[start:end])

def check_spelling(text, dictionary):
    # Check spelling of words in the text and return misspelled words with suggestions and context
    words_with_positions = extract_words_with_positions(text)
    misspelled = []
    prev_word = None
    sentence_start = True

    for i, (word, line, column) in enumerate(words_with_positions):
        if word in [',', '.', '!', '?', ';', ':', '"', "'", '(', ')', '—', '-'] or word.isspace() or word.isnumeric() or (len(word) == 1 and word.isalpha()):
            if word in ['.', '!', '?']:
                sentence_start = True
            prev_word = word
            continue

        cleaned_word = word.strip(".,!?;:\"'()—-")
        if cleaned_word.endswith("'s"):
            cleaned_word = cleaned_word[:-2]

        lower_word = cleaned_word.lower()

        if (lower_word not in dictionary and
            not (is_proper_noun(cleaned_word, prev_word) or sentence_start) and
            not is_valid_contraction(cleaned_word) and
            len(cleaned_word) < 45):
            suggestions = suggest_corrections(cleaned_word, dictionary)
            context = get_context(words_with_positions, i)
            misspelled.append((word, line, column, suggestions, context))

        prev_word = word
        sentence_start = False

    return misspelled

def main():
    if len(sys.argv) != 3:
        print("Usage: python spell_checker.py <dictionary_file> <file_to_check>")
        sys.exit(1)

    dict_file = sys.argv[1]
    file_to_check = sys.argv[2]

    try:
        dictionary = load_dictionary(dict_file)
        text_to_check = read_file(file_to_check)
        misspelled = check_spelling(text_to_check, dictionary)

        if misspelled:
            print("Misspelled words:")
            for word, line, column, suggestions, context in misspelled:
                print(f"'{word}' at line {line}, column {column}")
                print(f"  Context: ...{context}...")
                if suggestions:
                    print(f"  Suggestions: {', '.join(suggestions)}")
                else:
                    print("  No suggestions available")
                print()
        else:
            print("No misspelled words found.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()