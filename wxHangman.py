#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri May 20 21:43:48 2011

import wx, hangman, string, os.path

# begin wxGlade: extracode
# end wxGlade

keys = [['A', 'B', 'C', 'D'],
        ['E', 'F', 'G', 'H'],
        ['I', 'J', 'K', 'L'],
        ['M', 'N', 'O', 'P'],
        ['Q', 'R', 'S', 'T'],
        ['U', 'V', 'W', 'X'],
        ['', 'Y', 'Z', '']]

# 値をコンストラクタへの引数として受け取る点以外は
# テキスト版と同じである
class hmGUIGuess(hangman.hmGuess):
    def __init__(self, ch):
        self.theValue = string.lower(ch)
# end of class hmGUIGuess 

# 多重継承を使う。このゲームクラスは、wxの
# wx.Frameオブジェクトの一種であると同時に、
# ハングマンゲームのサブクラスでもあるので、両方を継承する
class hmGUI(wx.Frame, hangman.Hangman):
    def __init__(self, *args, **kwds):
        self.imgpath = 'img'
        self.firstImg = os.path.join(os.path.dirname(__file__), self.imgpath, 'hm6.jpg')
        self.letters = {}
        hangman.Hangman.__init__(self)
        # begin wxGlade: MyFrame.__init__
        wx.Frame.__init__(self, *args, **kwds)

        self.__set_properties()
        self.displayStart()
        # end wxGlade

    # GUI版のゲームでは、GUIとその基盤となる
    # 各種ゲームオブジェクトを繋ぐ部分において、
    # display()関数が多くの責務を持つ
    def display(self, chr):
        lossmsg = 'あなたの負けです! 正解 : \n\t%s'
        playmsg = '当てる言葉 : \n\t %s'
        successmsg = '正解! あなたの勝ちです。\nおめでとう。'

        # 一度提示された文字に印をつけておく
        self.letters[chr].Disable()
        # 推測を作成
        self.guesses.append(hmGUIGuess(chr))

        # 間違っていた場合に、挑戦できる残り回数を減らす
        self.outcome = self.theTarget.Eval(self.guesses[-1])
        txt = self.getResult()
        if self.outcome > 0:                # まだプレイ中である
            if '_' not in txt:              # 正解が当てられた
                txt = successmsg
            else: txt = playmsg % self.getResult()
        else:
            txt = lossmsg % self.theTarget.getGoal()
        self.status.SetLabel(txt)

        # イメージの更新
        thefile = os.path.join(self.imgpath, 'hm' + \
                               str(self.outcome) + '.jpg')
        self.theImg.SetBitmap(wx.Bitmap(thefile, wx.BITMAP_TYPE_ANY))

    def getTarget(self):
        return hangman.hmTarget()

    def Quit(self, event):
        self.Close(True)

    def reset(self, event):
        # すべての文字に未提示の印をつける
        for l in string.uppercase:
            self.letters[l].Enable()
        # 間違ってもよい回数と推測された文字のリストをセットし、
        # 新しい正解を作成する
        self.outcome = 6
        self.guesses = []
        self.theTarget = self.getTarget()

        # イメージと現在の状態をリセットする
        self.theImg.SetBitmap(wx.Bitmap(self.firstImg, wx.BITMAP_TYPE_ANY))
        txt = "当てる言葉 : \n\t%s" % self.getResult()
        self.status.SetLabel(txt)

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("ハングマン")
        # end wxGlade

    def displayStart(self):
        # Imageオブジェクトを作成
        self.theImg = wx.StaticBitmap(self, -1, wx.Bitmap(self.firstImg, wx.BITMAP_TYPE_ANY))
        
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.GridSizer(7, 4, 0, 0)

        # 文字盤を作成
        for row in keys:
            for ch in row:
                if ch == '':
                    self.letters[ch] = grid_sizer.Add((30, 30), 0, 0, 0)
                else:
                    action = lambda e, x = ch, s = self: s.display(x)
                    self.letters[ch] = wx.Button(self, -1, ch, size = (30, 30))
                    self.Bind(wx.EVT_BUTTON, action, self.letters[ch])
                    grid_sizer.Add(self.letters[ch], 0, wx.EXPAND, 0)

        txt = "当てる言葉 : \n\t%s" % self.getResult()
        self.status = wx.StaticText(self, -1, txt)
        
        self.button_Refresh = wx.Button(self, wx.ID_REFRESH, "リセット")
        self.button_Quit = wx.Button(self, wx.ID_EXIT, "終了")

        self.Bind(wx.EVT_BUTTON, self.reset, self.button_Refresh)
        self.Bind(wx.EVT_BUTTON, self.Quit, self.button_Quit)

        sizer_3.Add(self.theImg, 2, 0, 0)
        sizer_3.Add(grid_sizer, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 6, wx.EXPAND, 0)
        sizer_4.Add(self.status, 2, 0, 0)
        sizer_4.Add(self.button_Refresh, 1, 0, 0)
        sizer_4.Add(self.button_Quit, 1, 0, 0)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

# end of class hmGUI


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame = hmGUI(None, -1, "")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
