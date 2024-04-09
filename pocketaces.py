from math import floor
import random
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate, gen_cards
# from pypokerengine.engine.hand_evaluator import HandEvaluator

class CustomPokerPlayer(BasePokerPlayer):

  def __init__(self):
    # put player name here before running game.py
    self.initial_stack = None
    self.is_buff_last_round = None
    self.total_winnings = 0

  def declare_action(self, valid_actions, hole_card, round_state):

    round_count = round_state['round_count']
    street = round_state['street']
    community_card = round_state['community_card']

    pot_amount = round_state['pot']['main']['amount']
        
    raise_action_info = valid_actions[2]['action']
    raise_action_amount = valid_actions[2]['amount']

    max_raise_amount = raise_action_amount['max']
    min_raise_amount = raise_action_amount['min']
    raise_range_amount = max_raise_amount - min_raise_amount

    raise_1 = (round(random.uniform(0.3, 0.5), 2)*raise_range_amount)+min_raise_amount
    raise_1 = floor(raise_1)
    raise_2 = (round(random.uniform(0.2, 0.3), 2)*raise_range_amount)+min_raise_amount
    raise_2 = floor(raise_2)
    
    call_action_info = valid_actions[1]['action']
    call_action_amount = valid_actions[1]['amount']

    fold_action_info = valid_actions[0]['action']
    fold_action_amount = 0
    
    win_rate = estimate_hole_card_win_rate(10000, len(round_state['seats']) , gen_cards(hole_card) , gen_cards(community_card))
    print(win_rate)

    # evaluator = HandEvaluator()
    # hand_info = evaluator.gen_hand_rank_info(hole_card, community_card)
    # print(hand_info)

    # pot_odds = floor(pot_amount / call_action_amount)

    if round_count <= 3 and street == 'preflop':  # Early rounds, focus on strong hands
        if win_rate >= 0.45:
            return raise_action_info, max_raise_amount
        elif 0.3 <= win_rate < 0.5:
          if round(random.random(), 2) < 0.15:
            return raise_action_info, raise_1
          else:
            return raise_action_info, raise_2
        elif 0.2 <= win_rate < 0.3:
          return call_action_info, call_action_amount
        else:
          return fold_action_info, fold_action_amount
    elif round_count > 3 and street == 'preflop':
      if win_rate >= 0.65:
            return raise_action_info, max_raise_amount
      elif 0.35 <= win_rate < 0.5:
        if round(random.random(), 2) < 0.1:
            return raise_action_info, raise_1
        else:
            return raise_action_info, raise_2
      elif 0.15 <= win_rate < 0.35:
          return call_action_info, call_action_amount
      else:
          return fold_action_info, fold_action_amount


    elif street == 'flop':
      if win_rate >= 0.65:
        return raise_action_info, raise_action_amount['max']
      elif 0.35 <= win_rate < 0.65:
        if round(random.random(), 2) < 0.1:
            return raise_action_info, raise_1
        else:
            return raise_action_info, raise_2
      elif 0.2 <= win_rate < 0.35:
        return call_action_info, call_action_amount
      else:
        return fold_action_info, fold_action_amount
      
    elif street in ['turn', 'river']:
      if win_rate >= 0.7:
        return raise_action_info, raise_action_amount['max']
      elif 0.5 <= win_rate < 0.7:
        if round(random.random(), 2) < 0.1:
            return raise_action_info, raise_1
        else:
            return raise_action_info, raise_2
      elif 0.2 <= win_rate < 0.5:
        return call_action_info, call_action_amount
      else:
        return fold_action_info, fold_action_amount

  def receive_game_start_message(self, game_info):
    player_num = game_info['player_num']

    # err_msg = self.__build_err_msg("receive_game_start_message")
    # raise NotImplementedError(err_msg)

  def receive_round_start_message(self, round_count, hole_card, seats):
    round_count = round_count
    hole_card = hole_card

    # Placeholder code
    for player in seats:
      if player.get('name') == '':
        self.my_name == ''
        break

    # Use when p4 not defined in game.py   
    #for player in seats:
    #  if player['name'] == self.name:
    #    self.my_name == player['name']
    #    break
        
    print(f"New round {round_count}! My cards are {hole_card}")

    # err_msg = self.__build_err_msg("receive_round_start_message")
    # raise NotImplementedError(err_msg)

  def receive_street_start_message(self, street, round_state):
    street = round_state['street']
    print(f"Street started: {street}")

    # err_msg = self.__build_err_msg("receive_street_start_message")
    # raise NotImplementedError(err_msg)

  def receive_game_update_message(self, new_action, round_state):
    pass

    # err_msg = self.__build_err_msg("receive_game_update_message")
    # raise NotImplementedError(err_msg)

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass
    # err_msg = self.__build_err_msg("receive_round_result_message")
    # raise NotImplementedError(err_msg)

  def set_uuid(self, uuid):
    self.uuid = uuid

  def respond_to_ask(self, message):
    """Called from Dealer when ask message received from RoundManager"""
    valid_actions, hole_card, round_state = self.__parse_ask_message(message)
    return self.declare_action(valid_actions, hole_card, round_state)

  def receive_notification(self, message):
    """Called from Dealer when notification received from RoundManager"""
    msg_type = message["message_type"]

    if msg_type == "game_start_message":
      info = self.__parse_game_start_message(message)
      self.receive_game_start_message(info)

    elif msg_type == "round_start_message":
      round_count, hole, seats = self.__parse_round_start_message(message)
      self.receive_round_start_message(round_count, hole, seats)

    elif msg_type == "street_start_message":
      street, state = self.__parse_street_start_message(message)
      self.receive_street_start_message(street, state)

    elif msg_type == "game_update_message":
      new_action, round_state = self.__parse_game_update_message(message)
      self.receive_game_update_message(new_action, round_state)

    elif msg_type == "round_result_message":
      winners, hand_info, state = self.__parse_round_result_message(message)
      self.receive_round_result_message(winners, hand_info, state)


  def __build_err_msg(self, msg):
    return "Your client does not implement [ {0} ] method".format(msg)

  def __parse_ask_message(self, message):
    hole_card = message["hole_card"]
    valid_actions = message["valid_actions"]
    round_state = message["round_state"]
    return valid_actions, hole_card, round_state

  def __parse_game_start_message(self, message):
    game_info = message["game_information"]
    return game_info

  def __parse_round_start_message(self, message):
    round_count = message["round_count"]
    seats = message["seats"]
    hole_card = message["hole_card"]
    return round_count, hole_card, seats

  def __parse_street_start_message(self, message):
    street = message["street"]
    round_state = message["round_state"]
    return street, round_state

  def __parse_game_update_message(self, message):
    new_action = message["action"]
    round_state = message["round_state"]
    return new_action, round_state

  def __parse_round_result_message(self, message):
    winners = message["winners"]
    hand_info = message["hand_info"]
    round_state = message["round_state"]
    return winners, hand_info, round_state