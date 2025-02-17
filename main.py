from collections import defaultdict, heapq

def check_one_letter_difference(word1, word2):
  #checking length of the word
  if len(word1) != len(word2):
    return False
  #checking whether words differ by only word
  diff_count =0;
  #zip to pair and compare the no of differences of letters in the two words
  for a,b in zip(word1, word2):
    if a!=b:
      diff_count= diff_count+1

    if diff_count > 1:
      return False
  if diff_count == 1:
    return True
# print(check_one_letter_difference("red", "bed")) 
# print(check_one_letter_difference("led", "mad")) 


def load_words_from_file():
  words_set = set()
  with open('words.txt', 'r') as file:
    for word in file:
      words_set.add(word.strip())
    return words_set
#convrting to graph
def convert_words_to_a_graph():

  words_set = load_words_from_file()

  #optimized version

  #grouping words by length
  length_based_groups = defaultdict(list)
  for word in words_set:
    length_based_groups[len(word)].append(word)

  word_graph = defaultdict(list)

  #comparing only same sized words
  for word_list in length_based_groups.values():
    #making a set out of the word list for faster search - damn algorithms aren't so pointless afterall
    word_search = set(word_list)
    for word in word_list: #everyword
      for i in range(len(word)): #everycharacter
        for char in "abcdefgijklmnopqrstuvwxyz":
          new_formed_word = word[:i] + char + word[i+1:]#all possile combos
          if new_formed_word in word_search and new_formed_word !=word:
            word_graph[word].append(new_formed_word)
    return word_graph


    

  #bad code performance
  # #dictionary adjacency list
  # word_graph = defaultdict(list)
  # word_list = list(words_set)
  # for i in range(len(word_list)):
  #   for j in range(i+1, len(word_list)):
  #     if check_one_letter_difference(word_list[i], word_list[j]):
        
  #       #undirected graph
  #       word_graph[word_list[i]].append(word_list[j])
  #       word_graph[word_list[j]].append(word_list[i])
  return word_graph
#print('hi')
#print(convert_words_to_a_graph()) 

######################search algorithms#############

#ucs
 def uniform_cost_search(start_word, goal_word, word_graph):
  




