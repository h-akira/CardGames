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


class Deck:
  def __init__(self):
    deck = list(range(52))
    self.deck = []
    for i in range(52):
      self.deck.append(deck.pop(random.randint(0,len(deck)-1)))
    self.num = 52
  def draw(self,i=0):
    self.num -= 1
    return self.deck.pop(i)

class Cards:
  mark_list = ['♠','♣','♥','◆']
  def __init__(self):
    self.code = []
    self.mark = []
    self.num = []
    self.card = []
  def draw(self,code):
    self.code.append(code)
    self.mark.append(self.mark_list[code//13])
    self.num.append(code%13+1)
    self.card.append(self.mark[-1]+str(self.num[-1]))
    point = 0
    A_count = 0
    for num in map(code2num,hand):
      if num >= 10:
        point += 10
      elif num == 1:
        A_count += 1
        point += 1
      else:
        point += num
    if point>21:
      return 0
    else:
      while A_count>0:
        if point+10 <=21:
          point += 10
          A_count -= 1
        else:
          break
    self.point = point
    


  def all_text(self):
    return 


class Card:
  def __init__(self,code):
    self.code = code
    self.num = code%13+1
    self.mark 

    def code2num(code):
  if not 0<=code<= 51:
    raise ValueError("'code' must be in the range 0-51")
  return code%13+1

def code2mark(code):
  if not 0<=code<= 51:
    raise ValueError("'code' must be in the range 0-51")
  mark = ['♠','♣','♥','◆']
  return mark[code//13]

def code2card(code):
  return code2mark(code)+str(code2num(code))

def hand2point(hand):
  point = 0
  A_count = 0
  for num in map(code2num,hand):
    if num >= 10:
      point += 10
    elif num == 1:
      A_count += 1
      point += 1
    else:
      point += num
  if point>21:
    return 0
  else:
    while A_count>0:
      if point+10 <=21:
        point += 10
        A_count -= 1
      else:
        break
    return point

def draw(deck,hand):
  if len(deck)==0:
    raise ValueError("'deck' requires one or more elements")
  else:
    hand.append(deck.pop(0))

def hand2str(hand,hole=False):
  if hole:
    return '{} ??'.format(code2card(hand[0]))
  else:
    return ' '.join(map(code2card,hand))

def yn_inf(text,sep=' '):
  while True:
    ans = input(text+sep+'(y/n): ')
    if ans == 'y':
      return True
    elif ans == 'n':
      return False

def float_inf(text):
  while True:
    try:
      return float(input(text))
    except:
      pass

def view(deck,player,dealer,hole,tip=0,bet=0):
  os.system('clear')
  if tip or bet:
    print('所持チップ: {}  ベット: {}'.format(tip,bet))
  print('='*35)
  print('山札の残り枚数: {}'.format(str(len(deck))))
  print('プレイヤーの手札: {} ({})'.format(hand2str(player),str(hand2point(player))))
  if hole:
    print('ディーラーの手札: {} ({})'.format(hand2str(dealer,hole=hole),'??'))
  else:
    print('ディーラーの手札: {} ({})'.format(hand2str(dealer,hole=hole),str(hand2point(dealer))))
  print('='*35)

def bj(tip=0,bet=0):
  deck = gen_deck()
  player = []
  dealer = []
  draw(deck,player)
  draw(deck,player)
  draw(deck,dealer)
  draw(deck,dealer)
  view(deck,player,dealer,True,tip,bet)
  if hand2point(player) == 21:
    natural = True
  else:
    natural = False
    while True:
      if yn_inf('hitしますか？'):
        draw(deck,player)
        view(deck,player,dealer,True,tip,bet)
        if hand2point(player)==21 or hand2point(player)==0:
          break
      else:
        view(deck,player,dealer,True,tip,bet)
        break
  if hand2point(player) == 0:
    print('プレイヤーの負けです．')
    return tip
  input('ディーラーのターンに入ります．(enter)')
  view(deck,player,dealer,False,tip,bet)
  if hand2point(dealer)==21 and hand2point(player)==21:
    if natural:
      print('双方ナチュラル21のため引き分けです．')
      return tip + bet
    else:
      print('同点ですがディーラーのみがナチュラル21のため，プレイヤーの負けです．')
      return tip
  while 0 < hand2point(dealer) <17:
    input('ディーラーがカードを引きます．(enter)')
    draw(deck,dealer)
    view(deck,player,dealer,False,tip,bet)
  if hand2point(dealer)<21 and natural:
    print('プレイヤーの勝ちです．ナチュラル21のため，ベットしたチップが2.5倍になります．')
    return tip + 2.5*bet
  if hand2point(player) > hand2point(dealer):
    print('プレイヤーの勝ちです．')
    return tip + 2*bet
  elif hand2point(player) < hand2point(dealer):
    print('プレイヤーの負けです．')
    return tip
  else:
    print('引き分けです．')
    return tip + bet

def main():
  if not yn_inf('ブラックジャックを開始しますか？'):
    sys.exit()
  os.system('clear')
  while True:
    try:
      tip = float(input('チップの初期値: '))
      break
    except:
      pass
  while True:
    bet = float_inf('ベット: ')
    if bet <= 0:
      print('ベット額は0より大きくしてください．')
      continue
    elif bet > tip:
      print('あなたが現在所持しているチップは{}です．'.format(tip))
      print('所持している額より大きな額をベットすることはできません．')
      continue
    tip -= bet
    tip = bj(tip,bet)
    print('あなたが所持するチップは{}になりました．'.format(tip))
    if tip == 0:
      print('ベットすることができなくなったため終了します．')
      break
    if not yn_inf('継続しますか？'):
      if yn_inf('本当に終了しますか？'):
        break

if(__name__ == '__main__'):
  main()
