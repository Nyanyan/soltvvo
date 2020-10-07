# Soltvvo

**日本語は下部にあります**

## Introduction

Soltvvos are robots that solve 2x2x2 rubik’s cubes.

![Soltvvo3](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo3.jpg)

### Videos

Click the image and see on YouTube please.

Promotion Video: 

[![Soltvvo PV](http://img.youtube.com/vi/Fok7bAn-NSs/0.jpg)](http://www.youtube.com/watch?v=Fok7bAn-NSs)

[![Soltvvo PV](http://img.youtube.com/vi/76N6BOrEjSo/0.jpg)](http://www.youtube.com/watch?v=76N6BOrEjSo)

Demonstration with English subs:

[![Soltvvo PV](http://img.youtube.com/vi/irRzZQLlo04/0.jpg)](http://www.youtube.com/watch?v=irRzZQLlo04)

## Directories and Files

### Soltvvo1

![Soltvvo1](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo1.png)

There are programs of Soltvvo1, the first robot. The program is not efficient.

#### legacy

Test code and legacy program

#### soltvvo_arduino

The program for ATMEGA328P

#### coX.csv, cpX.csv

Files for pruning

#### soltvvo_IDAs_class.py

Main program

#### soltvvo_pre.py

A program which makes coX.csv and cpX.csv



### Soltvvo2

![Soltvvo2](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo2.jpg)

There are files of Soltvvo2, the second robot.

#### human

This program is a legacy, which is re-written of Soltvvo1’s program.

#### legacy

Test code and legacy program

#### one_phase

The latest code, explores a solution fast and the solution is the fastest.

#### soltvvo2_arduino

The program for ATMEGA328P

#### two_phase

This code uses two phase algorithm, so the solution is not the fastest.

### Soltvvo3

![Soltvvo3](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo3.jpg)

The latest version

#### soltvvo3_arduino

The program for ATMEGA328P

#### co.csv, co_cost.csv, cp.csv, cp_cost.csv, solved.csv, solved_solution.csv

CSV files used in Python program

#### log.txt

Log

#### soltvvo3.py

Main program

#### soltvvo3_display.py

This program is executed on PC, which shows the time to solve a cube

#### soltvvo3_pre.py

This must be executed before executing the main program.

## Want to learn more?

There are posts and playlist in Japanese: 

https://qiita.com/Nyanyan_Cube/items/a1b6e6bc7e4ac832b3d0

[![ルービックキューブを解くロボットを作ろう！](http://img.youtube.com/vi/xl9qaEfAsIs/0.jpg)](http://www.youtube.com/watch?v=9wuyo1KsjrM&list=PLwkf5JRsfk8OEn085444C6q4WWcrxCFgA)

If you would like to learn in English, please contact me.

Twitter: https://twitter.com/Nyanyan_Cube

Facebook: https://www.facebook.com/people/Takuto-Yamana/100011203000448





## イントロダクション

Soltvvo(ソルヴォ)は2x2x2ルービックキューブを自動で解くロボットです。

![Soltvvo3](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo3.jpg)

## 動画

画像をクリックしてください(YouTubeに飛びます)。

プロモーションビデオ: 

[![Soltvvo PV](http://img.youtube.com/vi/Fok7bAn-NSs/0.jpg)](http://www.youtube.com/watch?v=Fok7bAn-NSs)

[![Soltvvo PV](http://img.youtube.com/vi/76N6BOrEjSo/0.jpg)](http://www.youtube.com/watch?v=76N6BOrEjSo)

デモンストレーション: 

[![Soltvvo PV](http://img.youtube.com/vi/irRzZQLlo04/0.jpg)](http://www.youtube.com/watch?v=irRzZQLlo04)



## ディレクトリとファイル

### Soltvvo1

![Soltvvo1](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo1.png)

初号機、Soltvvo1のプログラムが入っています。

#### legacy

過去の産物

#### soltvvo_arduino

ATMEGA328P向けのプログラム

#### coX.csv, cpX.csv

枝刈りに使用

#### soltvvo_IDAs_class.py

メインプログラム

#### soltvvo_pre.py

枝刈り用のファイルを作成



### Soltvvo2

![Soltvvo2](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo2.jpg)

2つ目のロボットです。

#### human

Soltvvo1のプログラムの書き換え版(レガシー)

#### legacy

過去の産物

#### one_phase

最新のプログラム。高速に最も効率的な解を探索できます。

##### legacy

過去の産物

##### co.csv, cp.csv

枝刈りに使用

##### log.txt

ログ

##### soltvvo2_one_phase.py

メインプログラム

##### soltvvo2_one_phase_pre.py

前計算を行うプログラム。co.csv, cp.csv, solved.csv, solved_solution.csvを作成

##### solved.csv

5手以内に揃うスクランブルの状態を列挙

##### solved_solution.csv

5手以内に揃うスクランブルの解法を列挙

#### soltvvo2_arduino

ATMEGA328P用のプログラム

#### two_phase

2フェーズアルゴリズムを使ったプログラム。高速に解を探索しますが出力される解は最適ではありません。

### Soltvvo3

![Soltvvo3](https://github.com/Nyanyan/soltvvo/blob/master/img/soltvvo3.jpg)

最新のロボットです。

#### soltvvo3_arduino

ATMEGA328Pで動かすプログラム

#### co.csv, co_cost.csv, cp.csv, cp_cost.csv, solved.csv, solved_solution.csv

Pythonのプログラムで使うCSVファイル

#### log.txt

ログ

#### soltvvo3.py

メインプログラム

#### soltvvo3_display.py

PCで実行してタイムを表示するためのプログラム

#### soltvvo3_pre.py

前計算を行うプログラム。メインプログラム実行前に実行する。

## もっと詳しく

詳細を書いた記事と動画があります。: 

https://qiita.com/Nyanyan_Cube/items/a1b6e6bc7e4ac832b3d0

[![ルービックキューブを解くロボットを作ろう！](http://img.youtube.com/vi/xl9qaEfAsIs/0.jpg)](http://www.youtube.com/watch?v=9wuyo1KsjrM&list=PLwkf5JRsfk8OEn085444C6q4WWcrxCFgA)

もっと知りたい方はSNSで連絡をください。

Twitter: https://twitter.com/Nyanyan_Cube

Facebook: https://www.facebook.com/people/Takuto-Yamana/100011203000448
