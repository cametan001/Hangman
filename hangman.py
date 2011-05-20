#!/usr/bin/env python
# -*- coding: utf-8 -*-

import game, random, string, sys

## Game
class Hangman(game.Game):
    wordfile = 'hangman.words'          # 同一フォルダ内に置かれているものとする
    def __init__(self):
        game.Game.__init__(self)
        self.GuessType = hmGuess
        self.outcome = 6                # outcomeで挑戦回数をカウントする

    def displayStart(self):
        self.display(6)

    def getTarget(self):
        return hmTarget()

    def getResult(self):
        # 現時点で提示された文字のリストを生成する
        guessed = [g.value() for g in self.guesses if self.guesses]
        # 正解と提示された文字と比較する
        theWord = "".join([c in guessed and c or "_" for c in self.theTarget.getGoal()])
        return theWord

    def display(self, outcome):
        theWord = self.getResult()
        # 正しいかどうかをチェックする
        if '_' in theWord and outcome == 0:
            print "残念、はずれ。正解は「", \
                  self.theTarget.getGoal(), "」でした。"
        elif '_' not in theWord:
            print "正解です。おめでとう!"
            sys.exit()
        else:
            print "当てる言葉は %s\t あと %d 回挑戦出来ます。" \
                  % (theWord, outcome)

## Guess
class hmGuess(game.Guess):
    def __init__(self):
        self.theValue = raw_input("次の文字: ")
        # 入力が適切かどうかをチェックする
        if len(self.theValue) > 1:      # 先頭の文字だけを使う
            self.theValue = self.theValue[0]
        if self.theValue not in string.letters:
            self.theValue = raw_input("文字を入力してください!")

## Target
class hmTarget(game.Target):
    def __init__(self):
        self.outcome = 6
        try:
            wrdFile = open(Hangman.wordfile, "r")
            wordList = wrdFile.readlines()
            wrdFile.close()
            index = int(random.random() * \
                        (len(wordList) - 0.001))
            self.goal = wordList[index][:-1] # \nを除去
        except IOError:
            print 'ファイル %s の読み取りに失敗しました。' \
                  % Hangman.wordfile
            sys.exit()

    # evalは、あと何回間違ってもよいかの回数を返す
    def Eval(self, aGuess):
        if aGuess.value() not in self.goal:
            self.outcome -= 1
        return self.outcome

if __name__ == '__main__':
    hangman = Hangman()
    hangman.play()
