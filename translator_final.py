
"""
This project creates a translator application that uses English words as the source language
and translates them into different target languages.
Currently, it supports four languages: 1) French, 2) German, 3) Spanish, and 4) Italian.

The vocabulary is loaded from the tab-separated file "words.txt", which is expected to contain
English words and their translations in the specified target languages.
This project is designed to be scalable:
- To add more languages, simply add a new column heading (separated by a tab) in "words.txt"
  and include the corresponding translations for existing words.
- To add more words, append new rows with English words and their translations in all
  supported languages.

The core logic is handled by the parametric helper function `load_translations_from_file(filepath, target_languages)`,
which efficiently reads and structures the translation data.
"""

import os

# --- Helper Function: Load Translations from File ---

def load_translations_from_file(filepath, target_languages):
    """
    Loads translation data from a tab-separated text file into a nested dictionary.

    The file is expected to have a header row with language names (e.g., English, French, German, Spanish).
    The first column must be 'English' (case-insensitive), serving as the source language.

    Args:
        filepath (str): The absolute or relative path to the tab-separated text file containing translations.
        target_languages (list): A list of lowercase strings representing the target languages
                                 to load (e.g., ['french', 'german', 'spanish', 'italian']).

    Returns:
        dict: A nested dictionary structured as:
              {
                  'target_lang_1': {'english_word_1': 'translation_1', ...},
                  'target_lang_2': {'english_word_1': 'translation_1', ...},
                  ...
              }
              Returns dictionaries with empty language-specific sub-dictionaries if the file
              is empty, unreadable, or missing required language columns in its header.
    """
    # Initialize a dictionary to store translations for each target language.
    # Each target language will have its own dictionary mapping English words to translations.
    all_language_translations = {lang: {} for lang in target_languages}

    source_language_name = 'english' # Our base language for translation

    try:
        # Open the tab-separated file for reading with UTF-8 encoding.
        with open(filepath, 'r', encoding='utf-8') as f:
            header_line = f.readline()
            # If the file is empty or has no header, print an error and return empty dictionaries.
            if not header_line:
                print(f"Error: File '{filepath}' is empty or missing header.")
                return {lang: {} for lang in target_languages}

            # Process the header: strip whitespace, convert to lowercase, and split by tab.
            headers = [h.strip().lower() for h in header_line.strip().split('\t')]

            # Create a mapping from header names (language names) to their column indices.
            column_indices = {}
            for i, header in enumerate(headers):
                column_indices[header] = i

            # Verify that all required language columns (source and targets) exist in the header.
            required_cols = [source_language_name] + target_languages
            for col_name in required_cols:
                if col_name not in column_indices:
                    print(f"Error: Missing '{col_name}' column in header of '{filepath}'. Ensure all required languages are present.")
                    return {lang: {} for lang in target_languages}

            # Get the column index for the English (source) language.
            english_idx = column_indices[source_language_name]

            # Iterate over the rest of the lines in the file (translation data).
            for line in f:
                line = line.strip()
                if not line:
                    continue # Skip any empty lines

                parts = line.split('\t') # Split the line into columns using tab as delimiter

                # Ensure the current row has enough columns to avoid IndexError.
                # It must have at least as many parts as the maximum column index needed.
                if len(parts) > max(column_indices.values()):
                    english_word = parts[english_idx].strip().lower()

                    # Populate translations for each target language using their respective column indices.
                    for lang in target_languages:
                        lang_idx = column_indices[lang]
                        translation = parts[lang_idx].strip()
                        all_language_translations[lang][english_word] = translation
                else:
                    # Warn about and skip rows that do not have enough columns.
                    print(f"Warning: Skipping malformed row (not enough columns) in file '{filepath}': '{line}'")
    except FileNotFoundError:
        print(f"Error: The translation file '{filepath}' was not found. Please ensure it exists at that location.")
        return {lang: {} for lang in target_languages} # Return empty dicts on file not found
    except Exception as e:
        print(f"An unexpected error occurred while reading '{filepath}': {e}")
        return {lang: {} for lang in target_languages} # Return empty dicts on other unexpected errors

    return all_language_translations

# --- Main Program Logic ---

# Define the relative path to the translation data file.
file_path = os.path.join('Translator','words.txt') # 

# List of target languages to load from the translation file.
TARGET_LANGUAGES_TO_LOAD = ['french', 'german', 'spanish', 'italian'] # 

print(f"Loading translations from: {file_path}") # 
# Call the helper function to load all translation data.
all_translations = load_translations_from_file(file_path, TARGET_LANGUAGES_TO_LOAD) # 

# Extract available target languages and sort available English words for display/validation.
available_target_languages = list(all_translations.keys()) # 
available_english_words = [] # 

# Populate available_english_words if any target languages were successfully loaded.
if available_target_languages: # 
    first_target_lang = available_target_languages[0] # 
    if all_translations.get(first_target_lang): # 
        available_english_words = sorted(list(all_translations[first_target_lang].keys())) # 
    else:
        # Warn if no English words were loaded despite languages being specified.
        print(f"Warning: No English words found for translation, even though language '{first_target_lang}' was specified. Check '{file_path}'.") # 

# --- User Interaction and Translation Loop ---

print(f"Welcome to Translator") # 
print() # 
print(f"This translator's vocabulary is loaded from '{os.path.basename(file_path)}'.") # 
print() # 

# Display available languages and a prompt to check the translation file.
print(f"Available target languages: {', '.join(available_target_languages)}") # 
print(f"Please check the attached file for words.") # 
# Confirm the number of English words successfully loaded for translation.
print(f"Successfully loaded {len(available_english_words)} English words for translation.") # 
print() # 

# Outer loop: Allows the user to select a translation language repeatedly.
while True:
    # Construct the prompt for language selection, listing available options.
    language_prompt_choices = ", ".join(available_target_languages) if available_target_languages else "no languages available" # 
    user_language_choice = input(f"In what language do you want to translate (e.g., {language_prompt_choices})? Or type 'exit' to quit: ").lower() # 

    # Exit the application if the user types 'exit'.
    if user_language_choice == "exit": # 
        break # 

    # Validate the user's language choice.
    if user_language_choice not in available_target_languages: # 
        print(f"Invalid language. Please choose from {', '.join(available_target_languages)}.") # 
        continue # Ask for language again

    # If no English words were loaded, inform the user and continue to language selection.
    if not available_english_words: # 
        print("No English words are available for translation. Please check the file.") # 
        continue # 

    # Inner loop: Allows the user to translate multiple words in the chosen language.
    while True:
        # Prompt for English word, including option to go 'back' to language selection.
        user_word_input = input(f"Please enter the English word you want to translate (or type 'back' to choose a different language): ").lower() # 

        # If the user types 'back', return to the outer language selection loop.
        if user_word_input == "back": # 
            print("Returning to language selection.") # 
            break # Exit the inner loop

        # Look up the translation in the nested dictionary for the chosen language.
        translated_word = all_translations[user_language_choice].get(user_word_input) # 

        # If a translation is found, display it and break the inner loop (word translated).
        if translated_word: # 
            print(f"'{user_word_input}' translated to {user_language_choice} is '{translated_word}'.") # 
            break # Exit the inner loop because a valid word was entered
        else:
            # If no translation is found, inform the user and provide guidance.
            print(f"Sorry, '{user_word_input}' is not available for translation in {user_language_choice}.") # 
            print(f"Please check your spellings or choose any word from the available English words.") # 
            print(f"Available English words are in the file attached.") # 

print(f"Thank you for using the translator.") # 