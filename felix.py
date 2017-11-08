import random
import ast #ast.literal_eval
import game_recorder # recording decisions

DASHBOARD = {
     "AGENT_MODE": 0,
     # 0: manual
     # 1: random_agent

     "PRINT_MODE": "r",
     # a: All / Always
     # g: Gameplay Title
     # t: Title
     # i: Information
     # o: Agent Output
     # b: Bidding Result
     # r: Game Result
     # d: Debug

     "NUM_OF_GAME_PLAY": 200,
     "AUTO_REPLAY": True
     # 0: continue/stop playing at the end of the game
}

# Console Display Set-up #

fig_unrevealed = "*"
fig_arrow = " <<<"

### Functions ###

# customized print
def printm (text, text_type):
     global DASHBOARD
     print_mode = DASHBOARD["PRINT_MODE"]
     if (text_type == "a") or ("a" in print_mode) or (text_type in print_mode):
          print(text)

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
          if (key in deck_value.keys()):
               aux_list.append(deck_value[key])

     score = sum(aux_list)
     if (has_DOG and has_dog):
          score = 0
     elif (has_DOG):
          score = score - max(aux_list) # DOG eliminates max value
     elif (has_dog):
          score = score - min(aux_list) # dog eliminates min value

     return score

# convert a dictionary <string, bool> to an array of string
# e.g. {"+5":True, "+3":False, "DOG":True} -> ["+5", "DOG"]
def show_deck (deck):
     deck_list = []
     for key in deck.keys():
          if (deck[key] == True):
               deck_list.append(key)
     return deck_list

# convert an array to an array
# e.g. ["+5", "+3", "0", "DOG"] -> ["+5", "+3", "*", "*"] (revealed_length = 2)
def show_series (series, revealed_length):
     series_list = series[0: revealed_length]
     unrevealed_length = len(series) - revealed_length
     for _ in range(unrevealed_length):
          series_list.append(fig_unrevealed)
     return series_list

# output a string containing the rewards information
def  rewards_info (skip_rewards, reward_pointer):
     reward = skip_rewards[reward_pointer]
     output = "Skip Rewards: " + str(skip_rewards) + \
              " Reward Pointer: " + str(reward_pointer) + \
              " Current Reward: " + str(skip_rewards[reward_pointer])
     return output

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

### Agent Functions ###

def handler_manual (agent_input, agent_output):
     current_player = agent_input["players_public"][agent_input["my_index"]]
     stage = agent_input["stage"]
     if (stage == 1):
          # possible conditions
          card_to_sell = input("Please choose a card to sell: ")
          invalid_card = (card_to_sell not in agent_input["my_deck"])
          played_card = (not invalid_card) and (agent_input["my_deck"][card_to_sell] == False)
          while (invalid_card or played_card):
               print("You don't have " + card_to_sell)
               card_to_sell = input("Please choose a card to sell: ")
               # recompute possible conditions
               invalid_card = (card_to_sell not in agent_input["my_deck"])
               played_card = (not invalid_card) and (agent_input["my_deck"][card_to_sell] == False)
          agent_output["card_to_sell"] = card_to_sell
     else:
          bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
          # possible conditions
          numeric = bid_to_add.isnumeric()
          skip = numeric and (int(bid_to_add) == 0)
          negative_input = numeric and (int(bid_to_add) < 0)
          weak_bid = numeric and (current_player["bid"] + int(bid_to_add) <= agent_input["current_highest_bid"]) and (not skip)
          insufficient_token = numeric and (int(bid_to_add) > current_player["token"])
          while ((not numeric) or negative_input or weak_bid or insufficient_token):
               if (not numeric):
                    bid_to_add = input("Please input a number:")
               elif (negative_input):
                    bid_to_add = input("Please input a non-negative number:")
               elif (weak_bid):
                    print("Your bid (" + str(current_player["bid"] + int(bid_to_add)) + \
                          ") cannot beat the highest bid (" + str(agent_input["current_highest_bid"]) + ")")
                    bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
               else: # insufficient_token
                    print("You don't have enough tokens (" + str(current_player["token"]) + ")!")
                    bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
                # recompute possible conditions
               numeric = bid_to_add.isnumeric()
               skip = numeric and (int(bid_to_add) == 0)
               negative_input = numeric and (int(bid_to_add) < 0)
               weak_bid = numeric and (current_player["bid"] + int(bid_to_add) <= agent_input["current_highest_bid"]) and (not skip)
               insufficient_token = numeric and (int(bid_to_add) > current_player["token"])
          agent_output["bid_to_add"]  = int(bid_to_add)

def handler_random_agent (agent_input, agent_output):
     printm("INPUT DEBUG: ", "d")
     printm(agent_input, "d")
     current_player = agent_input["players_public"][agent_input["my_index"]]
     stage = agent_input["stage"]
     if (stage == 1):
          card_to_sell = random.choice(show_deck(agent_input["my_deck"]))
          printm("RANDOM AGENT sells " + card_to_sell, "o")
          agent_output["card_to_sell"] = card_to_sell
     else:
          max_bid_to_add = min(
               [agent_input["current_highest_bid"] - current_player["bid"] + 1, \
                current_player["token"], \
                agent_input["rule_max_bid"]]
          )
          if (max_bid_to_add < 0):
               bid_to_add = 0
          else:
               bid_to_add = random.randrange(max_bid_to_add + 1)
          printm("RANDOM AGENT adds " + str(bid_to_add), "o")
          agent_output["bid_to_add"]  = int(bid_to_add)
     #hold = input("Press any key to continue...")
     printm("OUTPUT DEBUG: ", "d")
     printm(agent_output, "d")

### Game ###

def play ():
     global DASHBOARD
     AGENT_MODE = DASHBOARD["AGENT_MODE"]
     PRINT_MODE = DASHBOARD["PRINT_MODE"]
     NUM_OF_GAME_PLAY = DASHBOARD["NUM_OF_GAME_PLAY"]
     AUTO_REPLAY = DASHBOARD["AUTO_REPLAY"]

     # Game Rules Set-up #

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

     default_deck = {} # dictionary <string, bool>
     for key in list(default_deck_value.keys()):
          default_deck[key] = True

     total_round = 10
     default_score = 0
     default_token = 15
     max_bid = 2
     skip_rewards = [1, 2, 3, 4] # length must not exceed num_of_player
     num_of_player = 4

     # Player Template Set-up #

     player_template = {
          "deck": {}, # dictionary <string, bool>
          "show_deck_public": [],
          "score": default_score,
          "token": default_token,
          "bid": 0,
          "skipped": False
     }

     # Agent Template Set-up #

     agent_input_template = {
          "my_index": -1, # index of current player
          "rule_total_round": total_round,
          "rule_default_deck_value": default_deck_value, # dictionary <string, int>
          "rule_max_bid": max_bid,
          "round": -1,
          "starting_player_index": -1,
          "stage": 0, # 1 for Selling Stage, 2 for Bidding Stage
          "players_public": [],
          "my_deck": {},
          "central_series_public": [],
          "rule_skip_rewards": skip_rewards,
          "reward_pointer": -1,
          "current_highest_bid": -1
     }

     agent_output_template = {
          "card_to_sell": "INITIAL",
          "bid_to_add": -1
     }

     game_result = {
          "winner": -1,
          "total_scores": []
     }

     # Game Loop Start #

     for game_play in range(0, NUM_OF_GAME_PLAY):

          printm("\n###### GAME PLAY " + str(game_play) + " ######", "g")

          # Data Recorder Set-up #
          game_recorder.set_recording()

          # Game Initiation #

          current_round = 0
          starting_player_index = 0
          players = [] # array of dictionary
          for i in range(num_of_player):
               players.append(player_template.copy())
               players[i]["deck"] = default_deck.copy()

          # Game Start #

          printm("\n### GAME START ###", "t")

          while (current_round < total_round):

               current_round += 1

               # prepare agent_input and agent_output
               agent_input = agent_input_template.copy()
               agent_output = agent_output_template.copy()

               printm("\n========", "t")
               printm(" Round " + str(current_round), "t")
               printm("========", "t")
               agent_input["round"] = current_round
               agent_input["starting_player_index"] = starting_player_index

               # Round Initiation #

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

               # Selling Stage #

               printm("\n-----------------", "t")
               printm(" Selling Stage", "t")
               printm("-----------------", "t")
               agent_input["stage"] = 1

               for i in range(num_of_player):

                    current_player_index = (starting_player_index + i) % num_of_player
                    current_player = players[current_player_index]
                    current_deck = current_player["deck"]

                    printm("\n<Player " + str(current_player_index) + "'s Turn>\n", "t")
                    agent_input["my_index"] = current_player_index

                    # information (excluding bid) of all players
                    agent_input["players_public"] = []
                    for i in range(num_of_player):
                         if (i == current_player_index):
                              placeholder = fig_arrow
                         else:
                              placeholder = ""
                         printm("Player " + str(i) + placeholder + "\n" + player_info(players[i]), "i")
                         agent_input["players_public"].append(players[i].copy())
                         del agent_input["players_public"][i]["deck"]

                    printm("\n" + str(show_deck(current_deck)), "i")
                    agent_input["my_deck"] = current_deck

                    if (AGENT_MODE) == 1:
                         handler_random_agent(agent_input, agent_output)
                    else:
                         handler_manual(agent_input, agent_output)
                    card_to_sell = agent_output["card_to_sell"]

                    # Record the selling decision #
                    game_recorder.decision_recorder(agent_input, agent_output)

                    current_deck[card_to_sell] = False
                    central_series.append(card_to_sell)

               # Bidding Stage #

               printm("\n-----------------", "t")
               printm("Bidding Stage", "t")
               printm("-----------------", "t")
               agent_input["stage"] = 2

               current_player_index = starting_player_index - 1

               while ( (reward_pointer < num_of_player - 1) or fleeing):

                    if (fleeing):
                         fleeing_loop_terminator = True

                    current_player_index = (current_player_index + 1) % num_of_player
                    current_player = players[current_player_index]

                    if (current_player["skipped"]):
                         continue

                    printm("\n<Player " + str(current_player_index) + "'s Turn>\n", "t")
                    agent_input["my_index"] = current_player_index
                    agent_input["my_deck"] = current_deck

                    # information (including bid) of all players
                    agent_input["players_public"] = []
                    for i in range(num_of_player):
                         if (i == current_player_index):
                              placeholder = fig_arrow
                         else:
                              placeholder = ""
                         printm("Player " + str(i) + placeholder + "\n" + player_info_bid(players[i]), "i")
                         agent_input["players_public"].append(players[i].copy())
                         del agent_input["players_public"][i]["deck"]

                    printm("\n" + str(show_series(central_series, central_series_revealed_length)), "i")
                    agent_input["central_series_public"] = show_series(central_series, central_series_revealed_length)
                    printm("Starting Player: " + str(starting_player_index), "i")
                    printm(rewards_info(skip_rewards, reward_pointer), "i")
                    agent_input["reward_pointer"] = reward_pointer
                    agent_input["current_highest_bid"] = current_highest_bid

                    skip = False

                    # forced to skip
                    if (current_player["token"] <= current_highest_bid - current_player["bid"]):
                         if (fleeing):
                              blanking = True
                         printm("You are forced to skip since you don't have enough tokens to win the bid.", "o")
                         skip = True

                    # not forced to skip
                    else:
                         if (fleeing):
                              printm("All other players fleed. Now you are the only bidder.", "o")

                         if (AGENT_MODE == 1):
                              handler_random_agent(agent_input, agent_output)
                         else:
                              handler_manual(agent_input, agent_output)
                         bid_to_add = agent_output["bid_to_add"]

                         # Record the bidding decision #
                         game_recorder.decision_recorder(agent_input, agent_output)

                         skip = (bid_to_add == 0)

                         if  (skip):
                              printm("You choose to skip.", "o")
                         else:
                              current_player["token"] -= bid_to_add
                              current_player["bid"] += bid_to_add
                              current_highest_bid = current_player["bid"]
                              current_highest_bidder_index = current_player_index
                              printm("You add your bid to " + str(current_player["bid"]), "o")

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
                         printm("You receive a skip reward of " + str(reward) + placeholder, "o")
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

               printm("\n" + str(show_series(central_series, central_series_revealed_length)), "i")

               if (blanking):
                    printm("All players choose to skip.", "b")
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

                    printm("Player " + str(bid_winner_index) + " win the bid of score " +\
                          str(score) + " at the cost of " + str(cost) + placeholder, "b")

                    starting_player_index = bid_winner_index

          # Game Over #

          printm("\n### GAME OVER ###\n", "t")

          total_scores = []

          for i in range(num_of_player):
               total_scores.append(players[i]["score"] + players[i]["token"])
               printm("Player " + str(i) + "\n" + player_info_game_over(players[i]), "i")

          winner_index = total_scores.index(max(total_scores))

          # for agent
          game_result["winner"] = winner_index
          game_result["total_scores"] = total_scores

          # Record the Result #
          game_recorder.result_recorder(game_result)

          printm("\n--------------", "r")
          printm("Total Score", "r")
          printm("--------------", "r")

          for i in range(num_of_player):
               if (i == winner_index):
                    placeholder = fig_arrow
               else:
                    placeholder = ""
               printm("Player " + str(i) + " " + str(total_scores[i]) + placeholder, "r")

          printm("\nThe winner is Player " + str(winner_index) + "!", "a")

          # Replay #

          if (not AUTO_REPLAY):
               replay = input("\nNext game? (y/n) ")
               if (replay != "y"):
                    break


# Main #

if __name__=="__main__":
     play()
