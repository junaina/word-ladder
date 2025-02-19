from collections import defaultdict, deque
import heapq


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
      cleaned_word = word.strip().lower()
      words_set.add(cleaned_word)
  # print("loaded words (first 20):", list(words_set)[:20])
    # print("Ssample words:", list(words_set)[:20])  # Check the first 20 words
    # three_letter_words = [word for word in words_set if len(word) == 3]
    # print("threeletter words:", three_letter_words[:20])  # Print first 20 short words
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
  
#print('hi')
#print(convert_words_to_a_graph()) 

######################search algorithms#############

#ucs- words have been grouped by length and it takes equal amount of time to get from one word to  the other.

# word_graph = convert_words_to_a_graph()

# # Check first 10 connected words
# for word, neighbors in list(word_graph.items())[:10]:
#     # print(f"{word}: {neighbors}")

def uniform_cost_search(start_word, goal_word, word_graph):
  if start_word not in word_graph or goal_word not in word_graph:
    return "no valid path : '{start_word}' or '{end_word}' not in word list"
  #pq w a tuple  w cost, starting word and the path taken thus far
  pq = [(0, start_word, [start_word])]
  visited = set()

  while pq:
    cost, current_word, path = heapq.heappop(pq)
    # print(f"expanding: {current_word}, path so far: {path}") 
    if current_word == goal_word:
      return path
    
    if current_word not in visited:
      visited.add(current_word)

      #word_graph[current_word] is a list of neighbors of current_word, neighbor is a single word
      #updated path and updated cpst
      for neighbor in word_graph[current_word]:
        if neighbor not in visited:
        #  print (f"Adding {neighbor} to the queue") 
          heapq.heappush(pq, (cost+1, neighbor, path+[neighbor])) 
  return "no valid path"
  
#word_graph = convert_words_to_a_graph()
# #write to a file
# with open ('word_graph.txt', 'w') as file:
#   file.write(str(word_graph))

# print(uniform_cost_search("bed", "red", word_graph))


#A* searc algorithm
#heuristic function
def heuristic(first_word, second_word):
  return sum(a!=b for a,b in zip(first_word, second_word))

#a* function
def a_star_search(start_word, goal_word, word_graph):
  print("here")
  if start_word not in word_graph or goal_word not in word_graph:
    return "no valid path : '{start_word}' or '{end_word}' not in word list"
  #f(n) = g(n) + h(n), cost from node to node, start word, path
  pq=[(0+heuristic(start_word, goal_word), 0, start_word, [start_word])]
  visited = set()
  while pq:
    _, cost, current_word, path = heapq.heappop(pq)

    if current_word == goal_word:
      return path
    if current_word not in visited:
      visited.add(current_word)
      for neighbor in word_graph[current_word]:
        if neighbor not in visited:
          g= cost+1
          f=g+heuristic(neighbor, goal_word)
          heapq.heappush(pq, (f, g, neighbor, path+[neighbor]))
  return "no valid path"

# bfs searc
def bfs_search(start_word, goal_word, word_graph):
  if start_word not in word_graph or goal_word not in word_graph:
    return "no valid path: '{start_word}' or '{end_word}' not in word list"
  queue = deque([(start_word, [start_word])])
  visited = set()
  while queue:
    current_word, path= queue.popleft()

    if current_word==goal_word:
      return path

    if current_word not in visited:
      visited.add(current_word)
      for neighbor in word_graph[current_word]:
        if neighbor not in visited:
          queue.append((neighbor, path+[neighbor]))
  return "no valid path found"
word_graph = convert_words_to_a_graph()
print(bfs_search("bit","dog", word_graph))






