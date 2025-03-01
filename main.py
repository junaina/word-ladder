from collections import defaultdict, deque
import heapq
import time
import random

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
  #intuition: making this a set cause i need faster search
  # 
  # 
  with open('words.txt', 'r') as file:
    for word in file:
      cleaned_word = word.strip().lower()
      words_set.add(cleaned_word)
  # print("loaded words (first 20):", list(words_set)[:20])
    # print("ssample words:", list(words_set)[:20])  
    # three_letter_words = [word for word in words_set if len(word) == 3]
    # print("threeletter words:", three_letter_words[:20])  
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


#the find path function
def find_path(start_word, goal_word, word_graph, algorithm):
  if algorithm.lower() == "astar":
    return a_star_search(start_word, goal_word, word_graph)
  elif algorithm.lower() == "ucs":
    return uniform_cost_search(start_word, goal_word, word_graph)
  elif algorithm.lower() == "bfs":
    return bfs_search(start_word, goal_word, word_graph)
  else:
    return "incorrect specifier. chose from astar, ucs, bfs" 

# print(bfs_search("bit","dog", word_graph))
###################testing the algorithms against differentinpust####### 
# word_graph = convert_words_to_a_graph()
# test_cases = [
#     ("red", "bed"),
#     ("cat", "dog"),
#     ("lead", "gold"),
#     ("hope", "fear"),
#     ("cold", "warm"),
#     ("start", "end"),
#     ("heart", "smart"),
# ]

# for start, goal in test_cases:
#     print(f"a* search from '{start}' to '{goal}':", find_path(start, goal, word_graph, algorithm="astar"))
#     print(f"bfs search from '{start}' to '{goal}':", find_path(start, goal, word_graph, algorithm="bfs"))
#     print(f"ucs search from '{start}' to '{goal}':", find_path(start, goal, word_graph, algorithm="ucs"))
#     print("-------")



###############algorithm performance############
word_graph = convert_words_to_a_graph()
def compare_algos(start_word, goal_word, word_graph):
  results = {}
  for algo in ["astar", "ucs", "bfs"]:
    starttime = time.time()
    path = find_path(start_word, goal_word, word_graph, algo)
    results[algo]= {"path":path,"time":time.time()-starttime}
  return results

#generting random words
def generate_start_and_end_words(word_graph, level="beginner"):
  print("entered generate_start_and_end_words")
  all_words = list(word_graph.keys())

  length_groups =  defaultdict(list)
  for word in all_words:
    length_groups[len(word)].append(word)
  print("length groups:", length_groups)

  valid_lengths = list(length_groups.keys())
  chosen_length = random.choice(valid_lengths)
  all_words = length_groups[chosen_length]
  print("all words:", all_words)

  #difficulty level based on heuristics
  if level=="beginner":
    print("breakpt1")
    max_dist = 3
    print("breakpt2")
  elif level=="advanced":
    max_dist = 6
  else:
    max_dist = 9
    # banned_words = set(random.sample(all_words, min(len(all_words), 5)))
    # restricted_letters = set(random.sample("abcdefghijklmnopqrstuvwxyz", 2))
  for _ in range(100):
    start_word, goal_word = random.sample(all_words, 2)
    heuristic_dist = heuristic(start_word, goal_word)

    #filtering banned words and restricted letters in challenge ode
    if level == "challenge":

      banned_words = set(random.sample(all_words, min(len(all_words), 5)))
      path1 = find_path(start_word, goal_word, word_graph, "astar")
      # print("path1:", path1)
      #bfs path to ensue multiple unbanned paths exist
      path2 = find_path(start_word, goal_word, word_graph, "bfs")
      # print("path2:", path2)
      if path1!="no valid path" and path2!= "no valid path" and len(path1)>1 and len(path2)>1:
        if any(word in banned_words for word in path1):
          print("shortest path contains banned words. switching to second shortest path.")
          return start_word, goal_word, banned_words, path2
        return start_word, goal_word, banned_words, path1

    if heuristic_dist <= max_dist:
      path = find_path(start_word, goal_word, word_graph, "astar")
      if path != "no valid path":
        return start_word, goal_word
  #fallback
  return random.sample(all_words, 2)
  # while True:
  #   start_word, goal_word =random.sample(all_words, 2)
  #   if find_path(start_word, goal_word, word_graph, "astar") != "no valid path":
  #     return start_word, goal_word

##########################game play#########################################
def gameplay(word_graph):
  print("=========================================================\n")
  print("WORD LADDER 🪜")
  print("=========================================================\n")
  level = input("choose a difficulty level (beginner, advanced, challenge): ").strip().lower()
  result = generate_start_and_end_words(word_graph, level)

  if len(result) == 4:
      start_word, goal_word, banned_words, ai_path = result
  else:
      start_word, goal_word = result
      banned_words, ai_path = set(), []
  print("instructions")
  print("1. you are given a start word and a goal word.")
  print(f"your challenge: transform '{start_word}' into '{goal_word}'")

  banned_words = set()
  if level == "challenge":
    print(f"🚫 BANNED WORDS: {banned_words}")
  current_path = [start_word]

  while current_path[-1]!= goal_word:
    print("current path:", current_path)
    next_word = input("enter the next word🧠 or enter '?' for an ai generated hint🪄: ").strip().lower()

    if next_word == "?":
      print("guru at work🧝‍♀️")
      # ai_path= find_path(start_word, goal_word, word_graph, "astar")
      #wen and if i get no errors
      ai_path = find_path(current_path[-1], goal_word, word_graph, "astar")
      if isinstance(ai_path, list) and len(ai_path)>1:
        # ai_path = find_path(current_path[-1], goal_word, word_graph, "astar")
        for word in ai_path[1:]:
          if (word not in current_path and word not in banned_words ):
            print(f"psst! try '{word}'")
            break
          
          else:
                print("couldn't find a valid move that avoids banned words and letters.")
      else:
        print("why look at that! you managed to mess up so bad even ai gave up:/")
        print(f"ai path: {ai_path}") 
      continue
    if level == "challenge":
      if next_word in banned_words:
          print("🚫🚫🚫🚫🚫🚫🚫 this word is banned >-< >-< >-< give it another shot.🚫🚫🚫🚫🚫🚫🚫")
          continue
     
    
    if next_word in word_graph[current_path[-1]]:
      current_path.append(next_word)

    else:
      print("invalid move, try again")

  print(f"congratulations! you have successfully completed the word ladder in '{len(current_path)-1}' moves")
  algo_performace= compare_algos(start_word, goal_word, word_graph)
  print("algorithm performance:")
  for algo, performance in algo_performace.items():
    print(f"{algo.upper()} search: path:{performance['path']},time: {performance['time']}s")
  if input("play again? (yes/no):").strip().lower() != "yes":
        print("thanks for playing!")
        return 
  gameplay(word_graph)
gameplay(word_graph)

# start_word, goal_word = "heart", "smart"
# comparison_results = compare_algos(start_word, goal_word, word_graph)
# for algo, result in comparison_results.items():
#     print(f"{algo.upper()} search:")
#     print(f"path: {result['path']}")
#     print(f"time elapsed: {result['time']}seconds\n")



