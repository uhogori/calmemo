# -*- coding: utf-8 -*-
#データベースを操作する色んな処理をまとめたプログラム

import sqlite3
import pandas as pd

con = sqlite3.connect("hist.db", check_same_thread=False, isolation_level=None)#DBに接続
cur = con.cursor()#カーソルの定義

#テーブルのカラムを指定し、検索したいワードを引数で渡す
#一致したレコードを全て返す関数(返り値はDataFrame型)
def search_col(table_name, column_name, sWord):
    if(exists_tabel(table_name)):#テーブル名の指定が正しいか判定
        if(exists_column(table_name, column_name)):#列名リストに指定された列が存在する場合
            #検索ワードにヒットするレコードがあるか検索するSQLクエリを投げる
            cur.execute("SELECT * FROM {} WHERE {}='{}'".format(table_name, column_name, sWord))
            df = pd.DataFrame(cur.fetchall())
            if(df.empty != True):#クエリの出力結果が空(=検索ヒット数0)の場合
                return df#検索にヒットしたレコードを返す

#指定したテーブル+列+検索ワードにヒットするレコードを削除
def delete_record(table_name,column_name,sWord):
    if(exists_tabel(table_name)):#指定されたテーブルが存在する場合
        if(exists_column(column_name)):#指定された列が存在する場合
            if(exists_elements(table_name, column_name)):#指定された要素が存在する場合
                cur.execute('DELETE FROM {} WHERE {}="{}"'.format(table_name,column_name,sWord))#削除実行
                con.commit()

#指定したテーブルの中身をすべて削除()
def delete_all_record(table_name, user_id):
    cur.execute('DELETE FROM {} WHERE user_id = "{}"'.format(table_name, user_id))#DELETE文実行
    con.commit()#commit

#管理しているテーブルの一覧をリストで返す関数
def req_table():
    cur.execute("SELECT name FROM sqlite_master where type='table'")
    tables = []
    for row in cur.fetchall():
        tables.append(row[0])#.fetchall()で取得した要素は全てタプルになっている[(hoge,),(fuga,)]
    return tables#管理しているテーブルの一覧をリストで取得

#指定したテーブルの持つ列名が返される
def req_colname(table_name):
    if(exists_tabel(table_name)):#指定されたテーブルが存在する場合
        cur.execute("SELECT * FROM {}".format(table_name))
        rows=[]
        for row in cur.description:#description属性を用いて、テーブルの列名を取得
            rows.append(row[0])#タプルの先頭に列名が入っている(他は全てNone)
        return rows#列名のリストを返す

#指定されたテーブルが存在するか判定(存在する=True, しない=False)
def exists_tabel(table_name):
    table_list = req_table()#テーブル名の一覧を取得
    if(table_name in table_list):
        return True
    else:
        return False

#指定されたテーブルに指定された列が存在するか判定(存在する=True, しない=False)
def exists_column(table_name, column_name):
    cur.execute("SELECT * FROM {}".format(table_name))
    columns = [description[0] for description in cur.description]#リスト内法表記を用いて列名を取得
    if(column_name in columns):
        return True
    else:
        return False

#指定されたテーブル，列に検索ワードと一致する要素があるか判定(存在する=True, しない=False)
def exists_elements(table_name, column_name, sWord):
    cur.execute("SELECT * FROM {} WHERE {}='{}'".format(table_name, column_name, sWord))
    df = pd.DataFrame(cur.fetchall())
    if(df.empty):#クエリの出力結果が空(=検索ヒット数0)の場合(=True)
        return False #ヒットしなかったのでFalse
    else:
        return True