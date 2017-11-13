import random
import ast #ast.literal_eval
import game_recorder # recording decisions
import agent

# TO-DOs
# 1. design naive agent

DASHBOARD = {
     "NUM_OF_PLAYER": 4,
     
     "AGENT_MODES": [3, 1, 1, 1], # must be of length NUM_OF_PLAYER
     # 0: manual
     # 1: random_agent
     # 2: naive_agent
     # 3: gen1_agent (svm_agent / nn_agent / nb_agent / dt_agent / lr_agent)

     "AGENT_NAMES": ["svm", "", "", ""], # must be of length NUM_OF_PLAYER
     # when corresponding AGENT_MODE == 3, "svm"/"nn"/"nb"/"dt"/"lr"
     # else, leave it as ""

     "PRINT_MODE": "g",
     # a: All / Always
     # g: Gameplay Title and Winning Statistics
     # t: Title
     # i: Information
     # o: Agent Output
     # b: Bidding Result
     # r: Game Result
     # d: Debug

     "NUM_OF_GAME_PLAY": 100,
     "AUTO_REPLAY": True,
     "HOLD": False, # hold at the end of the agent function,
     "WIN_RATE_COUNT": True,
     "GAME_RECORD": False
}

WIN_COUNTS = []
AGENT_WAREHOUSE = {}

# Console Display Set-up #

FIG_UNREVEALED = "*"
FIG_ARROW = " <<<"

### Functions ###

# customized print
def printm (text, text_type):
     print_mode = DASHBOARD["PRINT_MODE"]
     if (text_type == "a") or ("a" in print_mode) or (text_type in print_mode):
          print(text)

# compute the score of series according to deck_value
def compute_series_score (series, deck_value):
     has_DOG = False
     has_dog = False
     aux_list = [] # array of int
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
          series_list.append(FIG_UNREVEALED)
     return series_list

# output a string containing the rewards information
def  rewards_info (skip_rewards, reward_pointer):
     output = "Skip Rewards: %s Reward Pointer: %d Current Reward: %d" % \
              (str(skip_rewards), reward_pointer, skip_rewards[reward_pointer])
     return output

# output a string containing the public information (excluding bid information) of a player
def player_info (player):
     output = "Score: %d Token: %d Deck: %s" % \
              (player["score"], player["token"], str(player["show_deck_public"]))
     return output

# output a string containing the public information (including bid information) of a player
def player_info_bid (player):
     output = "Score: %d Token: %d Bid: %d Skipped: %s Deck: %s" % \
              (player["score"], player["token"], player["bid"], player["skipped"], str(player["show_deck_public"]))
     return output

# output a string containing the information (excluding bid information) of a player when the game is over
def player_info_game_over (player):
     output = "Score: %d Token: %d Deck: %s" % \
              (player["score"], player["token"], str(show_deck(player["deck"])))
     return output

### Agent Functions ###

def handler (agent_input, agent_output):
     my_index = agent_input["my_index"]
     my_agent_mode = DASHBOARD["AGENT_MODES"][my_index]
     HOLD = DASHBOARD["HOLD"]
     if (my_agent_mode == 0):
          handler_manual (agent_input, agent_output)
     else:
          printm("INPUT DEBUG: ", "d")
          printm(agent_input, "d")
          if (my_agent_mode == 1):
               handler_random_agent (agent_input, agent_output)
          elif (my_agent_mode == 2):
               handler_naive_agent (agent_input, agent_output)
          elif (my_agent_mode == 3):
               handler_gen1_agent (agent_input, agent_output)
          else:
               hold = input("ERROR unknown AGENT_MODE: %d." % my_agent_mode)
               exit()
          if (HOLD):
               hold = input("Press any key to continue...")
          printm("OUTPUT DEBUG: ", "d")
          printm(agent_output, "d")

def handler_manual (agent_input, agent_output):
     current_player = agent_input["players_public"][agent_input["my_index"]]
     stage = agent_input["stage"]
     if (stage == 1): # in Selling Stage
          # possible conditions
          card_to_sell = input("Please choose a card to sell: ")
          invalid_card = (card_to_sell not in agent_input["my_deck"])
          played_card = (not invalid_card) and (agent_input["my_deck"][card_to_sell] == False)
          while (invalid_card or played_card):
               print("You don't have %s." % card_to_sell)
               card_to_sell = input("Please choose a card to sell: ")
               # recompute possible conditions
               invalid_card = (card_to_sell not in agent_input["my_deck"])
               played_card = (not invalid_card) and (agent_input["my_deck"][card_to_sell] == False)
          agent_output["card_to_sell"] = card_to_sell
     else: # in Bidding Stage
          bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
          # possible conditions
          numeric = bid_to_add.isnumeric()
          skip = numeric and (int(bid_to_add) == 0)
          negative_input = numeric and (int(bid_to_add) < 0)
          weak_bid = numeric and (current_player["bid"] + int(bid_to_add) <= agent_input["current_highest_bid"]) and (not skip)
          insufficient_token = numeric and (int(bid_to_add) > current_player["token"])
          while ((not numeric) or negative_input or weak_bid or insufficient_token):
               if (not numeric):
                    bid_to_add = input("Please input a number: ")
               elif (negative_input):
                    bid_to_add = input("Please input a non-negative number: ")
               elif (weak_bid):
                    print("Your bid (%d) cannot beat the highest bid (%d)." % \
                          (current_player["bid"] + int(bid_to_add), agent_input["current_highest_bid"]))
                    bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
               else: # insufficient_token
                    print("You don't have enough tokens (%d)!" % current_player["token"])
                    bid_to_add = input("Please decide the bid to add (input 0 to skip): ")
                # recompute possible conditions
               numeric = bid_to_add.isnumeric()
               skip = numeric and (int(bid_to_add) == 0)
               negative_input = numeric and (int(bid_to_add) < 0)
               weak_bid = numeric and (current_player["bid"] + int(bid_to_add) <= agent_input["current_highest_bid"]) and (not skip)
               insufficient_token = numeric and (int(bid_to_add) > current_player["token"])
          agent_output["bid_to_add"]  = int(bid_to_add)

def handler_random_agent (agent_input, agent_output):
     current_player = agent_input["players_public"][agent_input["my_index"]]
     stage = agent_input["stage"]
     if (stage == 1): # in Selling Stage
          card_to_sell = random.choice(show_deck(agent_input["my_deck"]))
          printm("RANDOM AGENT sells %s." % card_to_sell, "o")
          agent_output["card_to_sell"] = card_to_sell
     else: # in Bidding Stage
          min_bid_to_add = agent_input["current_highest_bid"] - current_player["bid"] + 1
          max_bid_to_add = max(
               [
                    agent_input["current_highest_bid"] - current_player["bid"] + agent_input["rule_max_bid"],
                    current_player["token"]
               ]
          )
          choices = list(range(min_bid_to_add, max_bid_to_add + 1))
          choices.append(0)
          bid_to_add = random.choice(choices)
          placeholder = "s" if (bid_to_add > 1) else ""
          printm("RANDOM AGENT adds %d token%s." % (bid_to_add, placeholder), "o")
          bid_to_exceed = 0 if (bid_to_add == 0) else (bid_to_add + current_player["bid"] - agent_input["current_highest_bid"])
          agent_output["bid_to_add"]  = bid_to_add
          agent_output["bid_to_exceed"] =  bid_to_exceed

# NOT FINISHED!
def handler_naive_agent (agent_input, agent_output):
     current_player = agent_input["players_public"][agent_input["my_index"]]
     stage = agent_input["stage"]
     if (stage == 1): # in Selling Stage
          pass
     else: # in Bidding Stage
          pass

def handler_gen1_agent (agent_input, agent_output):
     my_index = agent_input["my_index"]
     my_agent_name = DASHBOARD["AGENT_NAMES"][my_index]
     current_player = agent_input["players_public"][agent_input["my_index"]]
     stage = agent_input["stage"]
     if (my_agent_name in AGENT_WAREHOUSE):
          if (stage == 1): # in Selling Stage
               card_to_sell = AGENT_WAREHOUSE[my_agent_name]["sell"].predict(agent_input)
               printm("%s AGENT sells %s." % (my_agent_name, card_to_sell), "o")
               agent_output["card_to_sell"] = card_to_sell
          else: # in Bidding Stage
               bid_to_exceed = AGENT_WAREHOUSE[my_agent_name]["bid"].predict(agent_input)
               bid_to_add = 0 if (bid_to_exceed == 0) else (bid_to_exceed + agent_input["current_highest_bid"] - current_player["bid"])
               placeholder = "s" if (bid_to_add > 1) else ""
               printm("%s AGENT adds %d token%s." % (my_agent_name, bid_to_add, placeholder), "o")
               agent_output["bid_to_exceed"] = bid_to_exceed
               agent_output["bid_to_add"] = 0 if (bid_to_exceed == 0) else 0
     else:
          hold = input("ERROR unknown agent name: %s." % my_agent_name)
          exit()

### Game ###

def play ():

     PRINT_MODE = DASHBOARD["PRINT_MODE"]
     NUM_OF_GAME_PLAY = DASHBOARD["NUM_OF_GAME_PLAY"]
     AUTO_REPLAY = DASHBOARD["AUTO_REPLAY"]
     WIN_RATE_COUNT = DASHBOARD["WIN_RATE_COUNT"]
     GAME_RECORD= DASHBOARD["GAME_RECORD"]
     NUM_OF_PLAYER = DASHBOARD["NUM_OF_PLAYER"]

     # AGENT_WAREHOUSE Set-up #
     
     for agent_name in DASHBOARD["AGENT_NAMES"]:
          if (agent_name == ""):
               continue
          elif (agent_name not in AGENT_WAREHOUSE):
               AGENT_WAREHOUSE[agent_name] = {}
               if (agent_name == "svm"):
                    AGENT_WAREHOUSE[agent_name]["sell"] = agent.SVMAgent(targetType = "sell")
                    AGENT_WAREHOUSE[agent_name]["bid"] = agent.SVMAgent(targetType = "bid")
               elif (agent_name == "nn"):
                    AGENT_WAREHOUSE[agent_name]["sell"] = agent.NNAgent(targetType = "sell")
                    AGENT_WAREHOUSE[agent_name]["bid"] = agent.NNAgent(targetType = "bid")
               elif (agent_name == "nb"):
                    AGENT_WAREHOUSE[agent_name]["sell"] = agent.NBAgent(targetType = "sell")
                    AGENT_WAREHOUSE[agent_name]["bid"] = agent.NBAgent(targetType = "bid")
               elif (agent_name == "dt"):
                    AGENT_WAREHOUSE[agent_name]["sell"] = agent.DTAgent(targetType = "sell")
                    AGENT_WAREHOUSE[agent_name]["bid"] = agent.DTAgent(targetType = "bid")
               elif (agent_name == "lr"):
                    AGENT_WAREHOUSE[agent_name]["sell"] = agent.LRAgent(targetType = "sell")
                    AGENT_WAREHOUSE[agent_name]["bid"] = agent.LRAgent(targetType = "bid")
               else:
                    del AGENT_WAREHOUSE[agent_name]
                    hold = input("ERROR unknown agent name: %s." % agent_name)
               
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
     num_of_player = NUM_OF_PLAYER

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
          "bid_to_add": -1,
          "bid_to_exceed": -1
     }

     game_result = {
          "winner": -1,
          "total_scores": []
     }

     # Game Loop #

     if (WIN_RATE_COUNT):
          for _ in range(num_of_player):
               WIN_COUNTS.append(0)

     for game_play in range(0, NUM_OF_GAME_PLAY):

          printm("\n###### GAME PLAY %d ######" % game_play, "g")

          # Data Recorder Set-up #
          if (GAME_RECORD):
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
               printm(" Round %d" % current_round, "t")
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

                    printm("\n<Player %d's Turn>\n" % current_player_index, "t")
                    agent_input["my_index"] = current_player_index

                    # information (excluding bid) of all players
                    agent_input["players_public"] = []
                    for i in range(num_of_player):
                         placeholder = FIG_ARROW if (i == current_player_index) else ""
                         printm("Player %d%s\n%s" % (i, placeholder, player_info(players[i])), "i")
                         agent_input["players_public"].append(players[i].copy())
                         del agent_input["players_public"][i]["deck"]

                    printm("\n" + str(show_deck(current_deck)), "i")
                    agent_input["my_deck"] = current_deck

                    handler(agent_input, agent_output)
                    card_to_sell = agent_output["card_to_sell"]

                    # Record the selling decision #
                    if (GAME_RECORD):
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

                    printm("\n<Player %d's Turn>\n" % current_player_index, "t")
                    agent_input["my_index"] = current_player_index
                    agent_input["my_deck"] = current_deck

                    # information (including bid) of all players
                    agent_input["players_public"] = []
                    for i in range(num_of_player):
                         placeholder = FIG_ARROW if (i == current_player_index) else ""
                         printm("Player %d%s\n%s" % (i, placeholder, player_info_bid(players[i])), "i")
                         agent_input["players_public"].append(players[i].copy())
                         del agent_input["players_public"][i]["deck"]

                    printm("\n" + str(show_series(central_series, central_series_revealed_length)), "i")
                    agent_input["central_series_public"] = show_series(central_series, central_series_revealed_length)
                    printm("Starting Player: %d" % starting_player_index, "i")
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

                         handler(agent_input, agent_output)
                         bid_to_add = agent_output["bid_to_add"]

                         # Record the bidding decision #
                         if (GAME_RECORD):
                              game_recorder.decision_recorder(agent_input, agent_output)

                         skip = (bid_to_add == 0)

                         if  (skip):
                              printm("You choose to skip.", "o")
                         else:
                              current_player["token"] -= bid_to_add
                              current_player["bid"] += bid_to_add
                              current_highest_bid = current_player["bid"]
                              current_highest_bidder_index = current_player_index
                              printm("You add your bid to %d." % current_player["bid"], "o")

                    if (skip):
                         current_player["skipped"] = True
                         current_player["token"] += current_player["bid"]
                         current_player["bid"] = 0

                         # receive the reward
                         reward = skip_rewards[reward_pointer]
                         current_player["token"] += reward

                         placeholder = "s" if (reward > 1) else ""

                         printm("You receive a skip reward of %d token%s." % (reward, placeholder), "o")
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

                    placeholder = "s" if (reward > 1) else ""

                    printm("Player %d win the bid of score %d at the cost of %d token%s." % \
                           (bid_winner_index, score, cost, placeholder), "b")

                    starting_player_index = bid_winner_index

          # Game Over #

          printm("\n### GAME OVER ###\n", "t")

          total_scores = []

          for i in range(num_of_player):
               total_scores.append(players[i]["score"] + players[i]["token"])
               printm("Player %d\n%s" % (i, player_info_game_over(players[i])), "i")

          winner_index = total_scores.index(max(total_scores))

          # for agent
          game_result["winner"] = winner_index
          game_result["total_scores"] = total_scores

          # Record the Result #
          if (GAME_RECORD):
               game_recorder.result_recorder(game_result)

          printm("\n--------------", "r")
          printm("Total Score", "r")
          printm("--------------", "r")

          for i in range(num_of_player):
               placeholder = FIG_ARROW if (i == winner_index) else ""
               printm("Player %d %d%s" % (i, total_scores[i], placeholder), "r")

          printm("\nThe winner is Player %d!" % winner_index, "r")

          if (WIN_RATE_COUNT):
               WIN_COUNTS[winner_index] += 1

          # Replay #

          if (not AUTO_REPLAY):
               replay = input("\nNext game? (y/n) ")
               if (replay != "y"):
                    break

     if (WIN_RATE_COUNT):
          printm("\n###### WINNING STATISTICS ######", "g")
          total_game_play = game_play + 1
          printm("Total game play: %d" % total_game_play, "g")
          for i in range(num_of_player):
               printm("Player %d Winning: %d Winning Rate: %.2f" % \
                      (i, WIN_COUNTS[i], float(WIN_COUNTS[i]) / float(total_game_play)), "g")

# Main #

if __name__=="__main__":
     play()

