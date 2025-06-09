""""
This project creates a translator application that uses English words as the source language
and translates them into different target languages.

The vocabulary is loaded from the comma-separated file "words.csv", which is expected to contain
English words and their translations in the specified target languages.
This project is designed to be highly flexible and scalable:
- Target languages are automatically detected from the CSV file's header (all columns
  except 'English').
- To add more languages, simply add a new column heading (separated by a comma or semicolon,
  depending on your CSV's delimiter) in "words.csv" and include the corresponding translations
  for existing words.
- To add more words, append new rows with English words and their translations in all
  supported languages.

The core logic is handled by the parametric helper function `load_translations_from_file(filepath)`,
which efficiently reads and structures the translation data.
"""

import os # import the os module for handling file path.
import csv # Import the csv module for handling CSV files

# --- Helper Function: Load Translations from File ---

def load_translations_from_file(filepath):
    """
    Loads translation data from a comma/semicolon-separated CSV file into a nested dictionary.

    The file is expected to have a header row with language names (e.g., English, French, German, Spanish).
    The first column must be 'English' (case-insensitive), serving as the source language.
    All other columns in the header are automatically detected as target languages.

    Args:
        filepath (str): The absolute or relative path to the CSV file containing translations.

    Returns:
        dict: A nested dictionary structured as:
              {
                  'target_lang_1': {'english_word_1': 'translation_1', ...},
                  'target_lang_2': {'english_word_1': 'translation_1', ...},
                  ...
              }
              Returns dictionaries with empty language-specific sub-dictionaries if the file
              is empty, unreadable, or missing the required 'English' column in its header.
    """

    # Initialize a list to hold the languages dynamically detected from the file header.
    detected_target_languages = []
    source_language_name = 'english' # Our base language for translation

    # Initialize the main translation dictionary (will be populated after languages are detected)
    all_language_translations = {}

    try:
        # Open the CSV file for reading with UTF-8 encoding.
        # Use comma as delimiter, common for Excel-generated CSVs (MS-DOS format)
        with open(filepath, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=',') # Expecting comma delimiter from Excel MS-DOS CSV

            # Read the header row using next() to get it as a list of strings.
            header_row = next(csv_reader, None)
            # If the file is empty or has no header, print an error.
            if header_row is None:
                print(f"Error: File '{filepath}' is empty or missing header.")
                return {} # Return an empty dictionary if file is empty

            # Process the header: strip whitespace from each name and convert to lowercase.
            headers = [h.strip().lower() for h in header_row]

            # Create a mapping from header names (language names) to their column indices.
            column_indices = {}
            for i, header in enumerate(headers):
                column_indices[header] = i

            # Verify that the 'English' source language column exists.
            if source_language_name not in column_indices:
                print(f"Error: Missing '{source_language_name}' column in header of '{filepath}'. Ensure it's present.")
                return {} # Return empty if crucial 'english' column is missing

            # Dynamically determine target languages from the header.
            # All headers except the source language ('english') are considered target languages.
            detected_target_languages = [h for h in headers if h != source_language_name]

            # Initialize the main dictionary with empty dicts for each detected target language.
            all_language_translations = {lang: {} for lang in detected_target_languages}

            # Get the column index for the English (source) language.
            english_idx = column_indices[source_language_name]

            # Iterate over the remaining rows in the CSV file (translation data).
            for parts in csv_reader:
                # Skip completely empty rows.
                if not parts or all(not p.strip() for p in parts):
                    continue

                # Ensure the current row has enough columns for all required languages.
                # It must have at least as many parts as the maximum column index needed.
                if len(parts) > max(column_indices.values()):
                    english_word = parts[english_idx].strip().lower()

                    # Populate translations for each detected target language.
                    for lang in detected_target_languages:
                        lang_idx = column_indices[lang] # Get the index for the current target language
                        translation = parts[lang_idx].strip()
                        all_language_translations[lang][english_word] = translation
                else:
                    # Warn about and skip rows that do not have enough columns.
                    print(f"Warning: Skipping malformed row (not enough columns) in file '{filepath}': '{parts}'")
    except FileNotFoundError:
        print(f"Error: The translation file '{filepath}' was not found. Please ensure it exists at that location.")
        return {} # Return empty dict on file not found
    except Exception as e:
        print(f"An unexpected error occurred while reading '{filepath}': {e}")
        return {} # Return empty dict on other unexpected errors

    return all_language_translations

# --- Main Program Logic ---

# Define the relative path to the translation data file.
file_path = os.path.join('Translator', 'words.csv')

print(f"Loading translations from: {file_path}")
# Call the helper function to load all translation data.
# The function now automatically detects target languages from the file header.
all_translations = load_translations_from_file(file_path)

# Extract available target languages from the keys of the loaded translations.
available_target_languages = list(all_translations.keys())

# Initialize a list to hold sorted English words.
available_english_words = []

# Populate available_english_words if any target languages were successfully loaded.
if available_target_languages:
    # Use the first available target language's dictionary to get the list of English words.
    first_target_lang = available_target_languages[0]
    if all_translations.get(first_target_lang):
        available_english_words = sorted(list(all_translations[first_target_lang].keys()))
    else:
        # Warn if no English words were found for translation, even if languages were detected.
        print(f"Warning: No English words found for translation, even though languages were detected. Check '{file_path}'.")

# --- User Interaction and Translation Loop ---

print(f"Welcome to Translator")
print()
print(f"This translator's vocabulary is loaded from '{os.path.basename(file_path)}'.")
print()

# Display available languages, now automatically detected.
print(f"Available target languages: {', '.join(available_target_languages)}")
print(f"Please check the attached file for words.")
# Confirm the number of English words successfully loaded for translation.
print(f"Successfully loaded {len(available_english_words)} English words for translation.")
print()

# Outer loop: Allows the user to select a translation language repeatedly.
while True:
    # Construct the prompt for language selection, listing automatically detected options.
    language_prompt_choices = ", ".join(available_target_languages) if available_target_languages else "no languages available"
    user_language_choice = input(f"In what language do you want to translate (e.g., {language_prompt_choices})? Or type 'exit' to quit: ").lower()

    # Exit the application if the user types 'exit'.
    if user_language_choice == "exit":
        break

    # Validate the user's language choice against the automatically detected languages.
    if user_language_choice not in available_target_languages:
        print(f"Invalid language. Please choose from {', '.join(available_target_languages)}.")
        continue # Ask for language again

    # If no English words were loaded (e.g., empty file after header), inform the user.
    if not available_english_words:
        print("No English words are available for translation. Please check the file.")
        continue # Continue to language selection (in case a valid word list loads later)

    # Inner loop: Allows the user to translate multiple words in the chosen language.
    while True:
        # Prompt for English word, including option to go 'back' to language selection.
        user_word_input = input(f"Please enter the English word you want to translate (or type 'back' to choose a different language): ").lower()

        # If the user types 'back', return to the outer language selection loop.
        if user_word_input == "back":
            print("Returning to language selection.")
            break # Exit the inner loop

        # Look up the translation in the nested dictionary for the chosen language.
        translated_word = all_translations[user_language_choice].get(user_word_input)

        # If a translation is found, display it and break the inner loop (word translated).
        if translated_word:
            print(f"'{user_word_input}' translated to {user_language_choice} is '{translated_word}'.")
            break # Exit the inner loop because a valid word was entered
        else:
            # If no translation is found, inform the user and provide guidance.
            print(f"Sorry, '{user_word_input}' is not available for translation in {user_language_choice}.")
            print(f"Please check your spellings or choose any word from the available English words.")
            print(f"Available English words are in the file attached.")

print(f"Thank you for using the translator.")