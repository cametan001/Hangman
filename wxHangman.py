#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import wx, hangman, string, sys, os.path

keys = [['A', 'B', 'C', 'D'],
        ['E', 'F', 'G', 'H'],
        ['I', 'J', 'K', 'L'],
        ['M', 'N', 'O', 'P'],
        ['Q', 'R', 'S', 'T'],
        ['U', 'V', 'W', 'X'],
        ['Y', 'Z']]

# 値をコンストラクタへの引数として受け取る点以外は
# テキスト版と同じである
class hmGUIGuess(hangman.hmGuess):
    def __init__(self, ch):
        self.theValue = string.lower(ch)

# 多重継承を使う。このゲームクラスは、wxの
# wxFrameオブジェクトの一種であると同時に、
# ハングマンゲームのサブクラスでもあるので、両方を継承する
class hmGUI(wx.Frame, hangman.Hangman):
    def __init__(self, parent, title):
        self.imgpath = 'img'
        self.firstImg = os.path.join(os.path.dirname(__file__), imgpath, 'hm6.jpg')
        self.letters = {}
        hangman.Hangman.__init__(self)
        wx.Frame.__init__(self, None, title = "ハングマン", size = (640, 480))
        self.displayStart()

    # GUI版のゲームでは、GUIとその基盤となる
    # 各種ゲームオブジェクトを繋ぐ部分において、
    # display()関数が多くの責務を持つ
    def display(self, chr):
        lossmsg = 'あなたの負けです! 正解 : \n\t%s'
        playmsg = '当てる言葉 : \n\t %s'
        successmsg = '正解! あなたの勝ちです。\nおめでとう。'

        # 一度提示された文字に印をつけておく
        self.letters[chr].config(state = DISABLED)
        # 推測を作成
        self.guesses.append(hmGUIGuess(chr))

        # 間違っていた場合に、挑戦できる残り回数を減らす
        self.outcome = self.theTarget.eval(self.guesses[-1])
        txt = self.getResult()
        if self.outcome > 0:                # まだプレイ中である
            if '_' not in txt:              # 正解が当てられた
                txt = successmsg
            else: txt = playmsg % self.getResult()
        else:
            txt = losmsg % self.theTarget.getGoal()
        self.status.configure(text = txt)

        # イメージの更新
        thefile = os.path.join(self.imgpath, 'hm' + \
                               str(self.outcome) + '.jpg')
        self.theImg.configure(file = thefile)

        
    
# if __name__ == '__main__':
