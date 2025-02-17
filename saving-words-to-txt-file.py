from nltk.corpus import words
words_set= set(words.words())

with open('words.txt', 'w') as file:
  for word in words_set:
    file.write(word+'\n')
