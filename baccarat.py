#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jul, 06, 2022 15:56:04 by Hiroto Akira

import random
import os
import sys
from operator import attrgetter


class ValueRangeError(Exception):
  pass

class NameDifferentError(Exception):
  pass

class Deck:
  def __init__(self):
    code_all = list(range(52))
    self.cards = []
    for i in range(52):
      self.cards.append(Card(code_all.pop(random.randint(0,len(code_all)-1))))
    self.num = 52
  def draw(self,i=0):
    self.num -= 1
    return self.cards.pop(i)

class Hand:
  def __init__(self,name=None):
    self.name = name
    self.cards = []
    self.num = 0
  def draw(self,deck,i=0):
    self.latest_card = deck.draw(i)
    self.cards.append(self.latest_card)
    self.num += 1
  def show_all(self):
    return ' '.join([card.show for card in self.cards])

class Baccarat_Hand(Hand):
  def __init__(self,name=None):
    super().__init__(name)
    self.score = 0
    self.three = None
  def draw(self,deck,i=0):
    super().draw(deck,i)
    card_score = min(self.latest_card.num,10) % 10
    self.score = (self.score + card_score) % 10  # 1の位だけのため
    if self.num == 3:
      self.three = card_score

class Card:
  mark_list = ['♠','♣','♥','◆']
  def __init__(self,code):
    if not 0<=code<= 51:
      raise ValueRangeError("'code' must be in the range 0-51")
    self.code = code
    self.num = code%13+1
    self.mark = __class__.mark_list[code//13]
    if self.num == 1:
      self.show = self.mark+'A'
    elif self.num == 11:
      self.show = self.mark+'J'
    elif self.num == 12:
      self.show = self.mark+'Q'
    elif self.num == 13:
      self.show = self.mark+'K'
    else:
      self.show = self.mark+str(self.num)
 
class Money:
  def __init__(self,initial_tip,name='あなた',debt=False,play=True):
    if initial_tip<=0:
      raise ValueRangeError("'initial_tip' must be greater than 0.")
    self.initial_tip = initial_tip
    self.own_tip = initial_tip
    self.bet_tip = None
    self.game_counter = 0
    self.miss_counter = 0
    self.hit_counter = 0
    self.name = name
    self.debt = debt
    self.play = play
  def bet(self,tip,debt=False):
    if not self.debt and not 0 < tip <= self.own_tip:
      raise ValueRangeError("'tip' must be greater than 0 and less than or equal 'self.tip'.")
    else:
      self.own_tip -= tip
      if self.bet_tip==None:
        self.bet_tip = tip
      else:
        self.bet_tip += tip
  def dividend(self,ratio=0,counter_add=True):
    if self.bet == None:
      raise TypeError("'self.bet' must be numerical value")
    else:
      self.own_tip += self.bet_tip*ratio
      self.bet_tip = None
      if counter_add:  # ゲーム中にそのゲーム数を表示するときなど
        self.game_counter += 1
        if ratio==0:
          self.miss_counter += 1
        else:
          self.hit_counter += 1

class Baccarat_Money(Money):
  predict_dic = {1:'プレイヤーの勝利',
2:'バンカーの勝利',
3:'引き分け'}
  choice_text ="""\
1: {}(1.95倍)
2: {}(2倍)
3: {}(9倍)\
""".format(predict_dic[1],predict_dic[2],predict_dic[3])
  def __init__(self,initial_tip,name='あなた'):
    super().__init__(initial_tip,name)
    self.predict_key = None
    self.predict_value = None
  def predict(self,predict_key):
    self.predict_key = predict_key
    self.predict_value = __class__.predict_dic[self.predict_key]
  def result(self,result_key):
    # チップの処理
    hit_text = '{0}の予想は当たりました！\n{0}がベットしていたチップは'.format(self.name)+ '{}倍になって返却されます．'
    if self.predict_key!=result_key:
      print('{0}の予想は外れました...\n{0}がベットしていたチップは没収されます．'.format(self.name))
      self.dividend() 
    elif result_key == 1:
      print(hit_text.format('1.95'))
      self.dividend(ratio=1.95)
    elif result_key == 2:
      print(hit_text.format('2'))
      self.dividend(ratio=2)
    elif result_key == 3:
      print(hit_text.format('9'))
      self.dividend(ratio=9)
    print('{}の所持チップ額は  {}  になります.'.format(self.name,self.own_tip))
    self.predict_key = None
    self.predict_value = None

class Moneys(list):
  def get_play_moneys(self):
    return [money for money in self if money.play]
  def notip_end(self):
    name_list = []
    for money in self:
      if money.play and money.own_tip <= 0:
        money.play = False
        name_list.append(money.name)
    return name_list
  def get_play_num(self):
    return sum(money.play for money in self)
  def sort_moneys(self,reverse=False):
    self.sort(key=attrgetter('game_counter'),reverse=not reverse)
    self.sort(key=attrgetter('own_tip'),reverse=not reverse)

class Baccarat_Moneys(Moneys):
  def view(self,clear=True):
    if clear:
      os.system('clear')
    print('='*line_length)
    for money in self:
      delta = money.own_tip-money.initial_tip
      print('【{}の結果】'.format(money.name))
      print('ゲーム数: {}'.format(str(money.game_counter)))
      print('的中    : {}'.format(str(money.hit_counter)))
      print('外れ    : {}'.format(str(money.miss_counter)))
      print('  最終チップ: {}'.format(str(money.own_tip)))
      print('- 初期チップ: {}'.format(str(money.initial_tip)))
      print('-'*(14+max(len(str(money.own_tip)),len(str(money.initial_tip)),len(str(abs(delta)))+1)))
      if delta > 0:
        sign = '+'
      elif delta<0:
        sign = '-'
      else:
        sign = '±'
      print('  収支　　　: {}'.format(sign+str(abs(delta))))
      print('='*line_length)

def yn_inf(text,sep=' '):
  while True:
    ans = input(text+sep+'(y/n): ')
    if ans == 'y':
      return True
    elif ans == 'n':
      return False

def clear_print_head(players_money,game_counter_add=True):
  os.system('clear')
  print('='*line_length)
  if game_counter_add:
    game_counter = players_money[0].game_counter + 1
  else:
    game_counter = players_money[0].game_counter
  print('【{}ゲーム目】'.format(str(game_counter)))
  for player_money in players_money:
    print('[{}]  所持チップ: {}  ベット: {}  予想: {}'.format(player_money.name,player_money.own_tip,player_money.bet_tip,player_money.predict_value))
  print('='*line_length)

def view(deck,player,banker,players_money):
  clear_print_head(players_money)
  print('山札の残り枚数: {}'.format(str(deck.num)))
  print('{}の手札: {} ({})'.format(player.name,player.show_all(),player.score))
  print('{}の手札: {} ({})'.format(banker.name,banker.show_all(),banker.score))
  print('='*line_length)

def input_draw_view(deck,player,banker,players_money,player_draw=True,check_draw=True):
  # playerがカード引く場合はplayer_draw=True．
  # bankerがカード引く場合はplayer_draw=False．
  if player_draw:
    if check_draw:
      input('{}がカードを引きます．(enter)'.format(player.name))
    player.draw(deck)
    view(deck,player,banker,players_money)
  else:
    if check_draw:
      input('{}がカードを引きます．(enter)'.format(banker.name))
    banker.draw(deck)
    view(deck,player,banker,players_money)

def baccarat(players_money,check_draw=True):
  clear_print_head(players_money)
  # 予想する
  for player_money in players_money:
    print(Baccarat_Money.choice_text)
    while True:
      try:
        player_money.predict(int(input('{}の予想: '.format(player_money.name))))
        break
      except (KeyError,ValueError) :
        print('1,2,3の中から選択して入力してください．')
    clear_print_head(players_money)
    # ベットする
    while True:
      try:
        player_money.bet(float(input('{}のベット額: '.format(player_money.name))))
        break
      except ValueError:
        print('数値を入力してください.')
      except ValueRangeError:
        print('0より大きくて所持チップ額({})より小さい数値を入力してください．'.format(str(player_money.own_tip)))
    clear_print_head(players_money)
  
  # ゲームスタート
  deck = Deck()
  player = Baccarat_Hand('プレイヤー')
  banker = Baccarat_Hand('バンカー')
  view(deck,player,banker,players_money)
  if check_draw:
    input('カードを配ります．(enter)')
  player.draw(deck)
  player.draw(deck)
  banker.draw(deck)
  banker.draw(deck)
  view(deck,player,banker,players_money)

  # ナチュラルとそうでない場合で分ける.
  # ナチュラルの場合
  if player.score >= 8 or banker.score >=8:
    pass
  # ナチュラルでない場合
  else:
    # プレイヤーが二枚目で終了する条件及びその場合
    if player.score>=6:
      # バンカーのターン
      if banker.score<=5:
        input_draw_view(deck,player,banker,players_money,player_draw=False,check_draw=check_draw)
    # プレイヤーが三枚目を引く条件及びその場合
    else:
      input_draw_view(deck,player,banker,players_money,player_draw=True,check_draw=check_draw)
      # バンカーのターン
      if banker.score<=2:
        input_draw_view(deck,player,banker,players_money,player_draw=False,check_draw=check_draw)
      elif banker.score==3 and (0<=player.three<=7 or player.three==9):
        input_draw_view(deck,player,banker,players_money,player_draw=False,check_draw=check_draw)
      elif banker.score==4 and 2<=player.three<=7:
        input_draw_view(deck,player,banker,players_money,player_draw=False,check_draw=check_draw)
      elif banker.score==5 and 4<=player.three<=7:
        input_draw_view(deck,player,banker,players_money,player_draw=False,check_draw=check_draw)
      elif banker.score==6 and 6<=player.three<=7:
        input_draw_view(deck,player,banker,players_money,player_draw=False,check_draw=check_draw)

  # 結果を判定
  if player.score > banker.score:
    print('プレイヤーの勝ちです．')
    result_key = 1
  elif player.score < banker.score:
    print('バンカーの勝ちです．')
    result_key = 2
  else:
    print('引き分けです．')
    result_key = 3

  # 結果に基づきお金を処理する
  for player_money in players_money:
    player_money.result(result_key)

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
バカラを行う．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-i", "--initial-tip", metavar="tip", type=float, default=10000, help="初期所持チップ")
  parser.add_argument("-d", "--check-draw", action="store_false", help="カードを引くときに確認しない")
  parser.add_argument("-p", "--players", metavar="名前", nargs='*', default=['あなた'], help="名前（敬称含む）")
  parser.add_argument("-l", "--line-lengh", metavar="長さ", type=int, default=70, help="画面を区切る線（-）の長さ（個数）")
  parser.add_argument("-s", "--result-sort", action="store_true", help="最終結果を表示するときにソートする")
  options = parser.parse_args()

  global line_length
  line_length = options.line_lengh
  
  try:
    if not yn_inf('バカラを開始しますか？'):
      sys.exit()
  except (KeyboardInterrupt,BaseException):
    print('\nバカラを開始せず終了します．')
    sys.exit()

  players_money = Baccarat_Moneys()
  for player in options.players:
    players_money.append(Baccarat_Money(options.initial_tip,player))
 
  # バカラを無限に行う
  while True:
    try:
      baccarat(players_money.get_play_moneys(),options.check_draw)
      end_name_list = players_money.notip_end()
      if len(end_name_list):
        input('{}はベットすることができなくなったためゲームから除外されます．(enter)'.format('と'.join(end_name_list)))
      if not players_money.get_play_num():
        input('参加者がいなくなったためゲームを終了します．(enter)')
        break
      if not yn_inf('継続しますか？'):
        if yn_inf('本当に終了しますか？'):
          break
    except KeyboardInterrupt:
      try:
        input('\n中断されました．ベットされていたチップは返却されます．(enter)')
      except KeyboardInterrupt:
        pass
      for player_money in players_money:
        try:
          player_money.dividend(ratio=1,counter_add=False)
        except TypeError:
          pass
      break
  
  # 最終結果を表示
  if options.result_sort:
    players_money.sort_moneys()
  players_money.view(clear=True)

if(__name__ == '__main__'):
  main()
