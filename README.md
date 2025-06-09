# My-Project
Translator Application
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

To run this application all you need to download the "translator_final.py" and "words.csv" files into "Translator" Folder.
