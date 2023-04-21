from spellchecker import SpellChecker

spell = SpellChecker()

data = "weght"

text = list(data.split(" "))
# find those words that may be misspelled
misspelled = spell.unknown(text)

for index, word in enumerate(text):
    if word in misspelled:
        text[index] = spell.correction(word)

newtext = ' '.join(text)
print(newtext)