#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Jul, 06, 2022 15:56:04 by Hiroto Akira
# $Author: $
# $Date: $
# $URL: $
__giturl__ = "$URL: $"

import random
import os
import sys

class ValueRangeError(Exception):
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
      raise ValueError("'code' must be in the range 0-51")
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
  def __init__(self,initial_tip):
    if initial_tip<=0:
      raise ValueRangeError("'initial_tip' must be greater than 0.")
    self.initial = initial_tip
    self.own_tip = initial_tip
    self.bet_tip = 0
  def bet(self,tip):
    if not 0 < tip <= self.own_tip:
      raise ValueRangeError("'tip' must be greater than 0 and less than or equal 'self.tip'.")
    else:
      self.own_tip -= tip
      self.bet_tip += tip
  def dividend(self,ratio=0):
    self.own_tip += self.bet_tip*ratio
    self.bet_tip = 0

class Baccarat_Predict:
  predict = {1:'プレイヤーの勝利',
2:'バンカーの勝利',
3:'引き分け'}
  def __init__(self):
    while True:
      print("""\
1: {}(1.95倍)
2: {}(2倍)
3: {}(9倍)\
""".format(__class__.predict[1],__class__.predict[2],__class__.predict[3]))
      try:
        self.key = int(input('予想: '))
        self.value = __class__.predict[self.key]
        break
      except (KeyError,ValueError) :
        print('1,2,3から選択してください.')

def yn_inf(text,sep=' '):
  while True:
    ans = input(text+sep+'(y/n): ')
    if ans == 'y':
      return True
    elif ans == 'n':
      return False

def clear_print_head(player_money,predict=None):
  os.system('clear')
  print('='*35)
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

def input_draw_view(deck,player,banker,player_money,predict,player_draw=True):
  # playerがカード引く場合はplayer_draw=True．
  # bankerがカード引く場合はplayer_draw=False．
  if player_draw:
    input('{}がカードを引きます．(enter)'.format(player.name))
    player.draw(deck)
    view(deck,player,banker,player_money,predict)
  else:
    input('{}がカードを引きます．(enter)'.format(banker.name))
    banker.draw(deck)
    view(deck,player,banker,player_money,predict)

def baccarat(player_money):
  clear_print_head(player_money)
  # 予想する
  predict = Baccarat_Predict()
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
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False)
    # プレイヤーが三枚目を引く条件及びその場合
    else:
      input_draw_view(deck,player,banker,player_money,predict,player_draw=True)
      # バンカーのターン
      if banker.score<=2:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False)
      elif banker.score==3 and (0<=player.three<=7 or player.three==9):
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False)
      elif banker.score==4 and 2<=player.three<=7:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False)
      elif banker.score==5 and 4<=player.three<=7:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False)
      elif banker.score==6 and 6<=player.three<=7:
        input_draw_view(deck,player,banker,player_money,predict,player_draw=False)

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

  # チップの処理
  hit_text = 'あなたの予想は当たったため，チップは{}倍になって返却されます．'
  if predict.key!=result_key:
    print('あなたの予想は外れたためチップは没収されます．')
    player_money.dividend() 
  elif result_key == 1:
    print(hit_text.format('1.95'))
    player_money.dividend(ratio=1.95)
  elif result_key == 2:
    print(hit_text.format('2'))
    player_money.dividend(ratio=2)
  elif result_key == 3:
    print(hit_text.format('9'))
    player_money.dividend(ratio=9)

  print('あなたの所持チップ額は{}になりました.'.format(player_money.own_tip))

def main():
  if not yn_inf('バカラを開始しますか？'):
    sys.exit()
  while True:
    try:
      player_money = Money(float(input('初期所持チップ: ')))
      break
    except ValueError:
      print('数値を入力してください.')
    except ValueRangeError:
      print('0より大きい数値を入力してください．')
  while True:
    baccarat(player_money)
    if player_money.own_tip == 0:
      print('ベットすることができなくなったため終了します．')
      break
    if not yn_inf('継続しますか？'):
      if yn_inf('本当に終了しますか？'):
        break

if(__name__ == '__main__'):
  main()
