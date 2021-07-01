# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
from dialogue_system.knowledge.reader import read_exercise_name
    
def calc_req_cal(bmr,pal):
    return bmr*pal

def calc_bmr(gender,weight,height,age):#基礎代謝量の計算を行う
    if gender == '男':
        #男性： 13.397×体重kg＋4.799×身長cm−5.677×年齢+88.362
        bmr = (13.397 * float(weight) + 4.799 * float(height) - 5.677 * float(age) + 88.362)
        return bmr
    elif gender == '女':
        #女性： 9.247×体重kg＋3.098×身長cm−4.33×年齢+447.593
        bmr = (9.247 * float(weight) + 3.098 * float(height) - 4.33 * float(age) + 447.593)
        return bmr

def calc_cal(user_id,name,hour):#運動の消費カロリーを計算
    #参照元のyamlファイルを読み込み
    exercise_dict = read_exercise_name()
    #DBから利用者(user_id)の体重を持ってくる処理
    con = sqlite3.connect("hist.db", check_same_thread=False, isolation_level=None)
    df = pd.read_sql_query("SELECT * FROM personal_info WHERE user_id='{}'".format(user_id),con)
    weight = float(df['init_weight'][0])
    #METsを取得する処理
    for dict_key in exercise_dict:
        if name == exercise_dict[dict_key]['name']:
            METs = exercise_dict[dict_key]['METs']
            break
    con.close()
    return METs * weight * hour * 1.05# METs × 体重（kg） × 時間 × 1.05 ＝ 消費カロリー（kcal）