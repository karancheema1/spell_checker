# Spell Checker Project
This project is a simple spell checker that identifies misspelled words in a text file, provides suggestions for corrections, and shows the context of each misspelling.

## Requirements

Python 3.6 or higher 

## Usage
To use the spell checker, you need two files:

A dictionary file containing a list of correctly spelled words (one word per line).
A text file that you want to check for spelling errors.

Run the spell checker with the following command:
```text
python spell_checker.py path/to/dictionary.txt path/to/file_to_check.txt
```
For example:
```text
python spell_checker.py dictionary.txt default-file-to-check.txt
```

## Sample Files
The repository includes sample files for testing:

dictionary.txt: A sample dictionary file.
default-file-to-check.txt: A sample text file with some intentional spelling errors.

## Output
The spell checker will output:

- Each misspelled word 
- The line and column where the misspelled word appears 
- The context surrounding the misspelled word 
- Suggestions for correct spellings 
