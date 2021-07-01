# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import pandas as pd
import sqlite3
import datetime
#from tabulate import tabulate          #dataframeの中身を表のように表示するモジュール
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

sys.path.append(str(Path('__file__').resolve().parent.parent))  #いとこディレクトリ(dialogue_system)にあるBotクラスをインポートするためのPATHを取得

from dialogue_system.dialogue_bot import Bot
from dialogue_system.util.ops_db import *
# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

#SlackBotのトークン
slack_token = ''
#接続先のDBを指定
con = sqlite3.connect("hist.db", check_same_thread=False, isolation_level=None)
#cursorオブジェクトを生成
cur = con.cursor()

#executeメソッドでSQLコマンドの実行（ここではデータベースを生成している）
#生成するテーブル(history_food=食事の記録用,history_exercise=運動の記録用,personal_info)
#history_cal テーブルを生成
cur.execute('''CREATE TABLE IF NOT EXISTS history_cal (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id varchar(100),food_name varchar(100),food_cal float(7,3),date date,delete_flag int(2))''')

#history_exercise テーブルを生成(id, user_id, exercise_name, exercise_cat, exercise_hour, exercise_dist, exercise_times,burned_cal, date, delete_flag)
#cur.execute('''CREATE TABLE IF NOT EXISTS history_exercise (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id varchar(100),exercise_name varchar(100),exercise_hour float(100),exercise_dist float(100),burned_cal float(100),date date,delete_flag int(2))''')
cur.execute('''CREATE TABLE IF NOT EXISTS history_exercise (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id varchar(100),exercise_name varchar(100),exercise_hour float(4,2),burned_cal float(6,2),date date,delete_flag int(2))''')

#personal_info(id,user_id,gender,init_weight,height,bmr,date,delete_flag)
#bmr=Basal metabolic rate(基礎代謝)
cur.execute('''CREATE TABLE IF NOT EXISTS personal_info (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id varchar(100),gender varchar(100),age int(100),init_weight int(100),height int(100),pal float(2,1),bmr float(6,2),req_cal float(6,2),date date,delete_flag int(2))''')

#作成したDBを表示するためのメソッド
@respond_to('表示')
def display_db(message):
    message.react('eyes_panic')#スタンプ
    body = message.body#入力文からbody要素を取得
    user_id = body['user']#bodyからユーザIDを取得
    tables = req_table()#テーブル名の一覧を取得
    tables.remove('sqlite_sequence')
    sent = ''
    for table_name in tables:
        df = pd.read_sql_query("SELECT * FROM {} WHERE user_id='{}'".format(table_name,user_id),con)
        sent += "テーブル名：{}の中身を表示\n".format(table_name)
        #sent += "{}\n\n".format(tabulate(df.drop(['id','delete_flag'],axis=1),tablefmt="grid"))
        sent += "{}\n\n".format(str(df.drop(['id','delete_flag'],axis=1)))
        #print(tabulate(df.drop(['id','delete_flag'],axis=1),tablefmt="grid"))
    message.reply(sent)

#どのように入力すればよいかわからない時用
@respond_to('help')
def help_func(message):
    message.reply('[対話機能]\n食事：食事の記録(摂取カロリーを記録)\n運動：運動の記録(消費カロリーを記録)\n初期登録：個人の情報を記録\n[標準機能]\n猶予：あとどれくらい摂取してよいのか?を教えてくれる。\n表示：各種記録を全て表示。\nhelp：このシステムに実装されている機能の一覧と概要を表示。')

@respond_to('猶予')
def remain_cal(message):
    sent = ''
    body = message.body#入力文からbody要素を取得
    user_id = body['user']#bodyからユーザIDを取得
    #personal_infoテーブルに要素が存在するか確認
    if not exists_elements('personal_info','user_id',user_id):#初期情報が登録されていない場合
        sent += '初期情報が登録されていません。初期登録と入力して初期情報の登録を済ませてください'
    else:#初期情報が存在している場合
        date= datetime.date.today()
        #摂取カロリーの合計を取得=sum_food_cal
        df = pd.read_sql_query('SELECT * FROM history_cal WHERE user_id="{0}" AND date BETWEEN "{1} 00:00:00" AND "{1} 23:59:59"'.format(user_id,date),con)
        if df.empty:#何も選択されない=何も食べていない場合
            sum_food_cal = 0.0
        else:
            sum_food_cal = df['food_cal'].sum()
        #消費カロリーの合計を取得=sum_exer_cal
        df = pd.read_sql_query('SELECT * FROM history_exercise WHERE user_id="{0}" AND date BETWEEN "{1} 00:00:00" AND "{1} 23:59:59"'.format(user_id,date),con)
        if df.empty:
            sum_exer_cal = 0.0
        else:
            sum_exer_cal = df['burned_cal'].sum()
        #個人の１日に必要な総カロリーを取得=req_cal
        df = pd.read_sql_query('SELECT * FROM personal_info WHERE user_id="{}"'.format(user_id),con)
        req_cal = df['req_cal']
        #猶予カロリーを計算(req_cal - sum_food_cal + sum_exer_cal)
        remain_cal = req_cal - sum_food_cal + sum_exer_cal
        sent += '今日の猶予カロリーは{}kcalです。\n'.format(round(remain_cal))
    message.reply(sent)


#対話システム用---------------

bots = {}#作られたbotを格納するためのリスト

def create_or_read(user_id):#ユーザIDを引数として受け取り，ユーザ毎にBotを作成するメソッド
    return bots[user_id] if user_id in bots else Bot()#botが既に作られていたらそのbotオブジェクトを返し，そうでなければ新たに作成

def save_bot(bot, user_id):
    bots[user_id] = bot

@respond_to('^(?!.*(表示|猶予|help)).+$')
def dialogue_system(message,some):#someは内部的に使用
    body = message.body#入力文からbody要素を取得
    text, user_id = body['text'], body['user']#bodyから，入力文が入ったtextとユーザIDを取得
    bot = create_or_read(user_id)#user_id毎にSlack Bot(対話)を生成
    reply_message = bot.reply(text,user_id)#ユーザの入力文を引数として渡し，botからの返答文を貰う
    save_bot(bot, user_id)#生成したbotを保存
    message.reply(reply_message)#botからの返答文をreply


#対話システム用はここまで---------------