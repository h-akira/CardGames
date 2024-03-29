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

def gen_deck(shuffle=True):
  deck = list(range(52))
  if shuffle:
    shuffled = []
    for i in range(52):
      shuffled.append(deck.pop(random.randint(0,len(deck)-1)))
    return shuffled
  else:
    return deck

def code2num(code):
  if not 0<=code<= 51:
    raise ValueError("'code' must be in the range 0-51")
  return code%13+1

def code2mark(code):
  if not 0<=code<= 51:
    raise ValueError("'code' must be in the range 0-51")
  mark = ['♠','♣','♥','◆']
  return mark[code//13]

def num2str(num):
  if not 1 <= int(num) <= 13:
    raise ValueError("'num' must be in the range 1-13")
  if num == 11:
    return 'J'
  elif num == 12:
    return 'Q'
  elif num == 13:
    return 'K'
  else:
    return str(int(num))

def code2card(code):
  return code2mark(code)+num2str(code2num(code))

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

def num2pmstr(num):
  if num == 0:
    return '±0.0'
  elif num > 0:
    return '+'+str(num)
  else:
    return str(num)

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
  if not yn_inf('プログラムを開始しますか？'):
    sys.exit()
  game = 0
  os.system('clear')
  while True:
    try:
      tip_initial = float(input('チップの初期値: '))
      tip = tip_initial
      break
    except ValueError:
      pass
  try:
    while True:
      bet = float_inf('ベット: ')
      if bet <= 0:
        print('ベット額は0より大きくしてください．')
        continue
      elif bet > tip:
        print('あなたが現在所持しているチップは{}です．'.format(tip))
        print('所持している額より大きな額をベットすることはできません．')
        continue
      tip = bj(tip-bet,bet)
      print('あなたが所持するチップは{}になりました．'.format(tip))
      game += 1
      if tip == 0:
        print('ベットすることができなくなったため終了します．')
        break
      if not yn_inf('継続しますか？'):
        if yn_inf('本当に終了しますか？'):
          break
  except KeyboardInterrupt:
    print('\n中断されました．ゲームが未決着の場合，ベットされていたチップは返却されます．') 
  result = """\
【結果】
プレイ回数　　: {}
チップの初期値: {}
チップの最終値: {}
収支　　　　　: {}""".format(str(game),str(tip_initial),str(tip),num2pmstr(tip-tip_initial))
  print('\n'+'='*35+'\n'+'='*35)
  print(result)

if(__name__ == '__main__'):
  main()
