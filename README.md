# My-Project
Translator Application
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
