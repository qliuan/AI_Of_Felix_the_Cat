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
          score -= max(aux_list)
     elif (has_dog):
          score -= min(aux_list)

     return score


default_deck = {} # dictionary <string, bool>
for key in list(default_deck_value.keys()):
     default_deck[key] = True
     
# convert a dictionary <string, bool> to an array of string
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
skip_reward = [1, 2, 3, 4] # length must not exceed num_of_player
reward_pointer = 0
num_of_player = 4

### Players ###

player_template = {
     "deck": {}, # dictionary
     "score": default_score,
     "token": default_token,
     "bid": 0,
     "skipped": False
}

# output a string containing the public information (excluding bid) of a player
def player_info (player):
     output = "Score: " + str(player["score"]) + \
              " Token: " + str(player["token"])
     return output

# output a string containing the public information (including bid) of a player
def player_info_bid (player):
     output = "Score: " + str(player["score"]) + \
              " Token: " + str(player["token"]) + \
              " Bid: " + str(player["bid"]) + \
              " Skipped: " + str(player["skipped"])
     return output

players = [] # array of dictionary
for i in range(num_of_player):
     players.append(player_template.copy())
     players[i]["deck"] = default_deck.copy()

### Game ###

current_round = 0
starting_player_index = 0
bid_winner_index = -1
next_player_index = -1
current_highest_bid = 0

history = [] # array of array
for _ in range(num_of_player):
     history.append([])

central_series = [] # array of string
central_series_revealed_length = 0

# convert an array to an array
def show_series (series, revealed_length):
     series_list = series[0: revealed_length]
     unrevealed_length = len(series) - revealed_length
     for _ in range(unrevealed_length):
          series_list.append(fig_unrevealed)
     return series_list

### Game Start ###

while (current_round < total_round):

     current_round += 1

     print("\n========")
     print(" Round " + str(current_round))
     print("========")

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
          for i in range(num_of_player):
               if (i == current_player_index):
                    placeholder = fig_arrow
               else:
                    placeholder = ""
               print("Player " + str(i) + " " + player_info(players[i]) + placeholder)
        
          print("\n" + str(show_deck(current_deck)))
          
          card_to_sell = input("Please choose a card to sell: ")
          while (card_to_sell not in current_deck):
               print("You don't have " + card_to_sell)
               card_to_sell = input("Please choose a card to sell: ")
               
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
          for i in range(num_of_player):
               if (i == current_player_index):
                    placeholder = fig_arrow
               else:
                    placeholder = ""
               print("Player " + str(i) + " " + player_info_bid(players[i]) + placeholder)
          
          print("\n" + str(show_series(central_series, central_series_revealed_length)))
          
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
               bid_to_add = int(input("Please decide the bid to add (input 0 to skip): "))

               # possible conditions
               skip = (bid_to_add == 0)
               negative_input = (bid_to_add < 0)
               weak_bid = (current_player["bid"] + bid_to_add <= current_highest_bid) and (not skip)
               insufficient_token = (bid_to_add > current_player["token"])
                
               while (negative_input or weak_bid or insufficient_token):
                    
                    if (negative_input):
                         bid_to_add = int(print("Please input a non-negative number:"))
                    elif (weak_bid):
                         print("Your bid (" + str(current_player["bid"] + bid_to_add) + \
                               ") cannot beat the highest bid (" + str(current_highest_bid) + ")")
                         bid_to_add = int(input("Please decide the bid to add (input 0 to skip): "))
                    else: # insufficient_token
                         print("You don't have enough tokens (" + str(current_player["token"]) + ")!")
                         bid_to_add = int(input("Please decide the bid to add (input 0 to skip): "))
                         
                     # recompute possible conditions    
                    skip = (bid_to_add == 0)
                    negative_input = (bid_to_add < 0)
                    weak_bid = (current_player["bid"] + bid_to_add <= current_highest_bid) and (not skip)
                    insufficient_token = (bid_to_add > current_player["token"])
                                   
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
               reward = skip_reward[reward_pointer]
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
          next_player_index = starting_player_index
     else:
          if (fleeing): # fleeing but not blanking
               bid_winner_index = current_player_index
          else: # not fleeing
               bid_winner_index = current_highest_bidder_index
               
          bid_winner = players[bid_winner_index]
          cost = bid_winner["bid"]
          bid_winner["bid"] = 0
          score = compute_series_score(central_series, default_deck_value)
          bid_winner["score"] += score

          if (reward > 1):
               placeholder = " tokens."
          else:
               placeholder = " token."

          print("Player " + str(bid_winner_index) + " win the bid of score " +\
                str(score) + " at the cost of " + str(cost) + placeholder)

# Game Over #


          


end = input("END")
