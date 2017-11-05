import random

### Console Display Set-up ###

fig_unrevealed = "*"
fig_arrow = " <<<"

### Game Set-up ###

default_deck_value = { # dictionary <string, int>
     "+15": 15,
     "+11": 11,
     "+8" : 8,
     "+5" : 5,
     "+3" : 3,
     "0"  : 0,
     "-5" : -5,
     "-8" : -8,
     "DOG": 0,
     "dog": 0
}

# compute the score of series according to deck_value
def compute_series_score (series, deck_value):
     has_DOG = False
     has_dog = False
     aux_list = [] # array of int, series without DOG and dog

     for key in series:
          if (key == "DOG"):
               has_DOG = True
          elif (key == "dog"):
              has_dog = True
          elif (key in deck_value.keys()):
               aux_list.append(deck_value[key])

     score = sum(aux_list)
     if (has_DOG and has_dog):
          score = 0
     elif (has_DOG):
          score = score - max(aux_list) # DOG eliminates max value
     elif (has_dog):
          score = score - min(aux_list) # dog eliminates min value

     return score


default_deck = {} # dictionary <string, bool>
for key in list(default_deck_value.keys()):
     default_deck[key] = True
     
# convert a dictionary <string, bool> to an array of string
# e.g. {"+5":True, "+3":False, "DOG":True} -> ["+5", "DOG"]
def show_deck (deck):
     deck_list = []
     for key in deck.keys():
          if (deck[key] == True):
               deck_list.append(key)
     return deck_list

total_round = 10
default_score = 0
default_token = 15
max_bid = 2
skip_rewards = [1, 2, 3, 4] # length must not exceed num_of_player
reward_pointer = 0
num_of_player = 4

# output a string containing the rewards information 
def  rewards_info (skip_rewards, reward_pointer):
     reward = skip_rewards[reward_pointer]
     output = "Skip Rewards: " + str(skip_rewards) + \
              " Reward Pointer: " + str(reward_pointer) + \
              " Current Reward: " + str(skip_rewards[reward_pointer])
     return output

### Players ###

player_template = {
     "deck": {}, # dictionary <string, bool>
     "show_deck_public": {},
     "score": default_score,
     "token": default_token,
     "bid": 0,
     "skipped": False
}

players = [] # array of dictionary
for i in range(num_of_player):
     players.append(player_template.copy())
     players[i]["deck"] = default_deck.copy()

# output a string containing the public information (excluding bid information) of a player
def player_info (player):
     output = "Score: " + str(player["score"]) + \
              " Token: " + str(player["token"]) + \
              " Deck: " + str(player["show_deck_public"])
     return output

# output a string containing the public information (including bid information) of a player
def player_info_bid (player):
     output = "Score: " + str(player["score"]) + \
              " Token: " + str(player["token"]) + \
              " Bid: " + str(player["bid"]) + \
              " Skipped: " + str(player["skipped"]) + \
              " Deck: " + str(player["show_deck_public"])
     return output

# output a string containing the information (excluding bid information) of a player when the game is over
def player_info_game_over (player):
     output = "Score: " + str(player["score"]) + \
              " Token: " + str(player["token"]) + \
              " Deck: " + str(show_deck(player["deck"]))
     return output

### Agent ###

agent_input = {
     "total_round": total_round,
     "default_deck_value": default_deck_value,
     "max_bid": max_bid,
     "round": -1,
     "starting_player_index": -1,
     "players_public": [],
     "my_deck": [],
     "central_series_public": [],
     "skip_rewards": skip_rewards,
     "reward_pointer": -1,
     "current_highest_bid": -1
}

# output card_to_sell (string)
def selling_handler_manual (player, agent_input):
     # possible conditions
     card_to_sell = input("Please choose a card to sell: ")
     invalid_card = (card_to_sell not in player["deck"])
     played_card = (not invalid_card) and (player["deck"][card_to_sell] == False)
     while (invalid_card or played_card):
          print("You don't have " + card_to_sell)
          card_to_sell = input("Please choose a card to sell: ")
          # recompute possible conditions
          invalid_card = (card_to_sell not in player["deck"])
          played_card = (not invalid_card) and (player["deck"][card_to_sell] == False)
     return card_to_sell

# output bid_to_add (int)
def bidding_handler_manual (player, agent_input):
     bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
     # possible conditions
     numeric = bid_to_add.isnumeric()
     skip = numeric and (int(bid_to_add) == 0)
     negative_input = numeric and (int(bid_to_add) < 0)
     weak_bid = numeric and (player["bid"] + int(bid_to_add) <= agent_input["current_highest_bid"]) and (not skip)
     insufficient_token = numeric and (int(bid_to_add) > current_player["token"])
     while ((not numeric) or negative_input or weak_bid or insufficient_token):
          if (not numeric):
               bid_to_add = input("Please input a number:")
          elif (negative_input):
               bid_to_add = input("Please input a non-negative number:")
          elif (weak_bid):
               print("Your bid (" + str(current_player["bid"] + int(bid_to_add)) + \
                     ") cannot beat the highest bid (" + str(current_highest_bid) + ")")
               bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
          else: # insufficient_token
               print("You don't have enough tokens (" + str(current_player["token"]) + ")!")
               bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
           # recompute possible conditions    
          numeric = bid_to_add.isnumeric()
          skip = numeric and (int(bid_to_add) == 0)
          negative_input = numeric and (int(bid_to_add) < 0)
          weak_bid = numeric and (player["bid"] + int(bid_to_add) <= agent_input["current_highest_bid"]) and (not skip)
          insufficient_token = numeric and (int(bid_to_add) > current_player["token"])
     return int(bid_to_add)

def selling_handler_random_agent (player, agent_input):
     card_to_sell = random.choice(show_deck(player["deck"]))
     print("RANDOM AGENT sells " + card_to_sell)
     #hold = input("Press any key to continue...")
     return card_to_sell

def bidding_handler_random_agent (player, agent_input):
     max_bid_to_add = min(
          [agent_input["current_highest_bid"] - player["bid"] + 1, current_player["token"], agent_input["max_bid"]]
     )
     if (max_bid_to_add == 0):
          bid_to_add = 0
     else:
          bid_to_add = random.randrange(max_bid_to_add + 1)
     print("RANDOM AGENT adds " + str(bid_to_add))
     #hold = input("Press any key to continue...")
     return bid_to_add

### Game ###

current_round = 0
starting_player_index = 0
reward_pointer = 0
current_highest_bid = 0
current_highest_bidder_index = -1

history = [] # array of array
for _ in range(num_of_player):
     history.append([])

central_series = [] # array of string
central_series_revealed_length = 0

# convert an array to an array
# e.g. ["+5", "+3", "0", "DOG"] -> ["+5", "+3", "*", "*"] (revealed_length = 2)
def show_series (series, revealed_length):
     series_list = series[0: revealed_length]
     unrevealed_length = len(series) - revealed_length
     for _ in range(unrevealed_length):
          series_list.append(fig_unrevealed)
     return series_list

### Game Start ###

print("\n### GAME START ###")

while (current_round < total_round):

     current_round += 1

     print("\n========")
     print(" Round " + str(current_round))
     print("========")
     agent_input["round"] = current_round
     agent_input["starting_player_index"] = starting_player_index

     # Restoration

     central_series = [] # empty the central series
     central_series_revealed_length = 1
     reward_pointer = 0
     current_highest_bid = 0
     current_highest_bidder_index = -1

     fleeing_detector = 1 # detect fleeing
     fleeing = False # explanation:
     blanking = False # explanation:
     fleeing_loop_terminator = False

     for i in range(num_of_player):
          players[i]["show_deck_public"] = show_deck(players[i]["deck"])
          players[i]["bid"] = 0
          players[i]["skipped"] = False

     # Selling Stage

     print("\n-----------------")
     print(" Selling Stage")
     print("-----------------")

     for i in range(num_of_player):

          current_player_index = (starting_player_index + i) % num_of_player
          current_player = players[current_player_index]
          current_deck = current_player["deck"]

          print("\n<Player " + str(current_player_index) + "'s Turn>\n")
          
          # information (excluding bid) of all players
          agent_input["players_public"] = []
          for i in range(num_of_player):
               if (i == current_player_index):
                    placeholder = fig_arrow
               else:
                    placeholder = ""
               print("Player " + str(i) + placeholder + "\n" + player_info(players[i]) )
               agent_input["players_public"].append(players[i].copy())
               del agent_input["players_public"][i]["deck"]
        
          print("\n" + str(show_deck(current_deck)))
          agent_input["my_deck"] = show_deck(current_deck)

          ###card_to_sell = selling_handler_manual (current_player, agent_input)
          card_to_sell = selling_handler_random_agent (current_player, agent_input)
               
          current_deck[card_to_sell] = False
          central_series.append(card_to_sell)

     # Bidding Stage

     print("\n-----------------")
     print("Bidding Stage")
     print("-----------------")

     current_player_index = starting_player_index - 1

     while ( (reward_pointer < num_of_player - 1) or fleeing):
          
          if (fleeing):
               fleeing_loop_terminator = True
          
          current_player_index = (current_player_index + 1) % num_of_player
          current_player = players[current_player_index]

          if (current_player["skipped"]):
               continue

          print("\n<Player " + str(current_player_index) + "'s Turn>\n")
          
          # information (including bid) of all players
          agent_input["players_public"] = []
          for i in range(num_of_player):
               if (i == current_player_index):
                    placeholder = fig_arrow
               else:
                    placeholder = ""
               print("Player " + str(i) + placeholder + "\n" + player_info_bid(players[i]))
               agent_input["players_public"].append(players[i].copy())
               del agent_input["players_public"][i]["deck"]
          
          print("\n" + str(show_series(central_series, central_series_revealed_length)))
          agent_input["central_series_public"] = show_series(central_series, central_series_revealed_length)
          print("Starting Player: " + str(starting_player_index))
          print(rewards_info(skip_rewards, reward_pointer))
          agent_input["reward_pointer"] = reward_pointer
          agent_input["current_highest_bid"] = current_highest_bid

          skip = False
          
          # forced to skip
          if (current_player["token"] <= current_highest_bid - current_player["bid"]):
               if (fleeing):
                    blanking = True
               print("You are forced to skip since you don't have enough tokens to win the bid.")
               skip = True

          # not forced to skip  
          else:
               if (fleeing):
                    print("All other players fleed. Now you are the only bidder.")
                    
               ###bid_to_add = bidding_handler_manual (current_player, agent_input)
               bid_to_add = bidding_handler_random_agent (current_player, agent_input)
               
               skip = (bid_to_add == 0)
                                   
               if  (skip):
                    print("You chose to skip.")
               else:
                    current_player["token"] -= bid_to_add
                    current_player["bid"] += bid_to_add
                    current_highest_bid = current_player["bid"]
                    current_highest_bidder_index = current_player_index
                    print("You added your bid to " + str(current_player["bid"]))

          if (skip):
               current_player["skipped"] = True
               current_player["token"] += current_player["bid"]
               current_player["bid"] = 0
               
               # receive the reward
               reward = skip_rewards[reward_pointer]
               current_player["token"] += reward
               if (reward > 1):
                    placeholder = " tokens."
               else:
                    placeholder = " token."
               print("You receive a skip reward of " + str(reward) + placeholder)
               reward_pointer += 1
               central_series_revealed_length += 1
               
               if (fleeing): # fleeing + last player skip = blanking
                    blanking = True
               elif (fleeing_detector): # detect fleeing
                    fleeing_detector += 1
                    if (fleeing_detector == num_of_player): # fleeing detected
                         fleeing = True
          else: # if a player does not skip , turn off the fleeing detector
               fleeing_detector = 0

          if (fleeing_loop_terminator):
               break

     print("\n" + str(show_series(central_series, central_series_revealed_length)))

     if (blanking):
          print("All players skipped.")
     else:
          if (fleeing): # fleeing but not blanking
               bid_winner_index = current_player_index
          else: # not fleeing
               bid_winner_index = current_highest_bidder_index

          score = compute_series_score(central_series, default_deck_value)
          bid_winner = players[bid_winner_index]
          cost = bid_winner["bid"]
          bid_winner["bid"] = 0
          bid_winner["score"] += score

          if (reward > 1):
               placeholder = " tokens."
          else:
               placeholder = " token."

          print("Player " + str(bid_winner_index) + " win the bid of score " +\
                str(score) + " at the cost of " + str(cost) + placeholder)

          starting_player_index = bid_winner_index

# Game Over #

print("\n### GAME OVER ###\n")

total_scores = []

for i in range(num_of_player):
     total_scores.append(players[i]["score"] + players[i]["token"])
     print("Player " + str(i) + "\n" + player_info_game_over(players[i]) )

winner_index = total_scores.index(max(total_scores))

print("\n--------------")
print("Total Score")
print("--------------")

for i in range(num_of_player):
     if (i == winner_index):
          placeholder = fig_arrow
     else:
          placeholder = ""
     print("Player " + str(i) + " " + str(total_scores[i]) + placeholder)

print("\nThe winner is Player " + str(winner_index) + "!")
