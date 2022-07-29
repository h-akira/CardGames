#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jul, 06, 2022 15:56:04 by Hiroto Akira

import random
import os
import sys

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

class Baccarat_Hand:
  def __init__(self,name=None):
    self.name=name
    self.cards = []
    self.score = 0
    self.num = 0
  def draw(self,deck,i=0):
    card = deck.draw(i)
    self.cards.append(card)
    card_score = min(card.num,10) % 10
    self.score = (self.score + card_score) % 10  # 1の位だけのため
    self.num += 1
    if self.num == 3:
      self.three = card_score
  def show_all(self):
    return ' '.join([card.show for card in self.cards])

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
  def __init__(self,initial_tip,name='あなた'):
    if initial_tip<=0:
      raise ValueRangeError("'initial_tip' must be greater than 0.")
    self.initial_tip = initial_tip
    self.own_tip = initial_tip
    self.bet_tip = 0
    self.game_counter = 0
    self.miss_counter = 0
    self.hit_counter = 0
    self.name = name
  def bet(self,tip):
    if not 0 < tip <= self.own_tip:
      raise ValueRangeError("'tip' must be greater than 0 and less than or equal 'self.tip'.")
    else:
      self.own_tip -= tip
      self.bet_tip += tip
  def dividend(self,ratio=0,counter_add=True):
    self.own_tip += self.bet_tip*ratio
    self.bet_tip = 0
    if counter_add:
      self.game_counter += 1
      if ratio==0:
        self.miss_counter += 1
      else:
        self.hit_counter += 1

class Baccarat_Predict:
  predict = {1:'プレイヤーの勝利',
2:'バンカーの勝利',
3:'引き分け'}
  choice_text ="""\
【選択肢】
1: {}(1.95倍)
2: {}(2倍)
3: {}(9倍)\
""".format(predict[1],predict[2],predict[3])
  def __init__(self,predict_key,name='あなた'):
    self.key = predict_key
    self.value = __class__.predict[self.key]
    self.name = name
  def result(self,result_key,money):
    if self.name !=money.name:
      raise NameDifferentError
    # チップの処理
    hit_text = '{}の予想は当たったため，'.format(self.name)+'ベットしていたチップは{}倍になって返却されます．'
    if self.key!=result_key:
      print('あなたの予想は外れたため，ベットしていたチップは没収されます．')
      money.dividend() 
    elif result_key == 1:
      print(hit_text.format('1.95'))
      money.dividend(ratio=1.95)
    elif result_key == 2:
      print(hit_text.format('2'))
      money.dividend(ratio=2)
    elif result_key == 3:
      print(hit_text.format('9'))
      money.dividend(ratio=9)
    print('{}の所持チップ額は{}になります.'.format(self.name,money.own_tip))

def yn_inf(text,sep=' '):
  while True:
    ans = input(text+sep+'(y/n): ')
    if ans == 'y':
      return True
    elif ans == 'n':
      return False

def clear_print_head(player_money,predict=None,game_counter_add=True):
  os.system('clear')
  print('='*35)
  if game_counter_add:
    game_counter = player_money.game_counter + 1
  else:
    game_counter = player_money.game_counter
  print('【{}ゲーム目】'.format(str(game_counter)))
  print('所持チップ: {}  ベット: {}'.format(player_money.own_tip,player_money.bet_tip))
  if predict!=None:
    print('あなたの予想: {}'.format(predict.value))
  print('='*35)

def view(deck,player,banker,player_money,predict):
  clear_print_head(player_money,predict)
  print('山札の残り枚数: {}'.format(str(deck.num)))
  print('{}の手札: {} ({})'.format(player.name,player.show_all(),player.score))
  print('{}の手札: {} ({})'.format(banker.name,banker.show_all(),banker.score))
  print('='*35)

def input_draw_view(deck,player,banker,player_money,predict,player_draw=True,check_draw=True):
  # playerがカード引く場合はplayer_draw=True．
  # bankerがカード引く場合はplayer_draw=False．
  if player_draw:
    if check_draw:
      input('{}がカードを引きます．(enter)'.format(player.name))
    player.draw(deck)
    view(deck,player,banker,player_money,predict)
  else:
    if check_draw:
      input('{}がカードを引きます．(enter)'.format(banker.name))
    banker.draw(deck)
    view(deck,player,banker,player_money,predict)

def baccarat(player_money,check_draw=True):
  clear_print_head(player_money)
  # 予想する
  while True:
    try:
      print(Baccarat_Predict.choice_text)
      predict = Baccarat_Predict(int(input('予想: ')))
      break
    except (KeyError,ValueError) :
      print('1,2,3の中から選択して入力してください．')
  print('='*35)
  # ベットする
  while True:
    try:
      player_money.bet(float(input('ベット額: ')))
      break
    except ValueError:
      print('数値を入力してください.')
    except ValueRangeError:
      print('0より大きくて所持チップ額({})より小さい数値を入力してください．'.format(str(player_money.own_tip)))
  
  # ゲームスタート
  deck = Deck()
  player = Baccarat_Hand('プレイヤー')
  banker = Baccarat_Hand('バンカー')
  view(deck,player,banker,player_money,predict)
  if check_draw:
    input('カードを配ります．(enter)')
  player.draw(deck)
  player.draw(deck)
  banker.draw(deck)
  banker.draw(deck)
  view(deck,player,banker,player_money,predict)

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
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False,check_draw=check_draw)
    # プレイヤーが三枚目を引く条件及びその場合
    else:
      input_draw_view(deck,player,banker,player_money,predict,player_draw=True,check_draw=check_draw)
      # バンカーのターン
      if banker.score<=2:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False,check_draw=check_draw)
      elif banker.score==3 and (0<=player.three<=7 or player.three==9):
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False,check_draw=check_draw)
      elif banker.score==4 and 2<=player.three<=7:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False,check_draw=check_draw)
      elif banker.score==5 and 4<=player.three<=7:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False,check_draw=check_draw)
      elif banker.score==6 and 6<=player.three<=7:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False,check_draw=check_draw)

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

  predict.result(result_key,player_money)


def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\
バカラを行う．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-i", "--initial-tip", metavar="tip", type=float, default=10000, help="初期所持チップ")
  parser.add_argument("-s", "--check-start", action="store_false", help="開始時の確認をしない")
  parser.add_argument("-d", "--check-draw", action="store_false", help="カードを引くときに確認しない")
  options = parser.parse_args()

  player_money = Money(options.initial_tip)
 
  if options.check_start:
    if not yn_inf('バカラを開始しますか？'):
      sys.exit()
  
  while True:
    try:
      baccarat(player_money,options.check_draw)
    except KeyboardInterrupt:
      input('中断されました．ベットされたチップは返却されます．(enter)')
      player_money.dividend(ratio=1,counter_add=False)
      break
    if player_money.own_tip == 0:
      input('ベットすることができなくなったため終了します．(enter)')
      break
    if not yn_inf('継続しますか？'):
      if yn_inf('本当に終了しますか？'):
        break
  
  delta = player_money.own_tip-player_money.initial_tip
  os.system('clear')
  print('【結果】')
  print('ゲーム数: {}'.format(str(player_money.game_counter)))
  print('的中    : {}'.format(str(player_money.hit_counter)))
  print('外れ    : {}'.format(str(player_money.miss_counter)))
  print('  最終チップ: {}'.format(str(player_money.own_tip)))
  print('- 初期チップ: {}'.format(str(player_money.initial_tip)))
  print('-'*(14+max(len(str(player_money.own_tip)),len(str(player_money.initial_tip)),len(str(delta)))))
  print('  収支　　　: {}'.format(str(delta)))

if(__name__ == '__main__'):
  main()
