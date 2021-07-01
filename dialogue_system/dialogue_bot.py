# -*- coding: utf-8 -*-
from dialogue_system.dialogue_management.manager import DialogueManager
from dialogue_system.language_generation.language_generate import LanguageGenerator
from dialogue_system.language_understanding.language_understanding import RuleBasedLanguageUnderstanding
from dialogue_system.util.calc import *#消費カロリーなど計算に関するメソッドをimport
from dialogue_system.util.ops_db import *#DB操作に関するメソッドをimport
import sqlite3
import datetime
#attribute_extractor(属性抽出器)とestimator(行動推定器)から，ユーザーの入力文理解を行うクラス
class Bot(object):

    def __init__(self):#対話システムが持つ属性(言語生成，言語理解，行動管理部のオブジェクト)
        self.generator = LanguageGenerator()
        self.language_understanding = RuleBasedLanguageUnderstanding()
        self.manager = DialogueManager()

    def reply(self, sent,user_id):
        #ユーザからの入力文を渡して属性を抽出
        dialogue_act = self.language_understanding.execute(sent)
        #内部状態の更新(ここの部分に抽出した属性が既に存在しているかを判定させる処理を記述。存在していたらusr_act_type='OTHER'にさせる。存在していなかったら内部状態の更新処理を行う)
        self.manager.update_dialogue_state(dialogue_act)
        #システムが取るべき行動を選択
        sys_act_type = self.manager.select_action(dialogue_act)
        #初期登録以外のモードが選択されている場合
        if self.manager.dialogue_state.get_mode() != '初期登録':
            if not exists_elements('personal_info','user_id',user_id):#個人情報が存在しない場合
                self.manager.dialogue_state.clear()#リセットするので内部状態をクリア
                sys_act_type['sys_act_type'] = 'REQUEST_MODE_INIT_REGIST'#初期登録モードを選択するように促す
        else:#初期登録モードが選択されている場合
            if exists_elements('personal_info','user_id',user_id):#個人情報が既に登録されている場合
                self.manager.dialogue_state.clear()#初期登録対話から受けるので内部状態をクリア
                sys_act_type['sys_act_type'] = 'REGISTED_INIT_INFO'#すでに登録されていると通達する

        #返信文の生成
        sent = self.generator.generate_reply(sys_act_type)
        #各モードに合わせた内部状態をDBへ登録
        if sys_act_type['sys_act_type'] == 'REGIST_FOOD':#食事登録の場合，内部状態をhistory_calテーブルに登録
            con = sqlite3.connect("hist.db", check_same_thread=False, isolation_level=None)#DBに接続
            cur = con.cursor()#カーソルの定義
            food_name = self.manager.dialogue_state.get_fname()#食品名を取得
            food_cal = self.manager.dialogue_state.get_cal()#食品のカロリーを取得
            add_dt = datetime.datetime.now().replace(microsecond=0)#現在時刻の取得
            #内部状態をDBに登録
            cur.execute("INSERT INTO history_cal(user_id, food_name, food_cal, date, delete_flag) VALUES (?,?,?,?,0)",[user_id, food_name, food_cal, add_dt])
            con.commit()#INSERTを行ったのでcommit
            cur.close()
            con.close()#commitしたのでDBから切断
            self.manager.dialogue_state.clear()#内部状態の初期化
        elif sys_act_type['sys_act_type'] == 'REGIST_EXERCISE':
            #内部状態をDBに登録
            add_dt = datetime.datetime.now().replace(microsecond=0)#現在時刻の取得
            exercise_name = self.manager.dialogue_state.get_ename() #運動名
            exercise_hour = self.manager.dialogue_state.get_hour()  #運動時間
            #exercise_dist = self.manager.dialogue_state.get_dist()  #運動距離
            burned_cal = 0      #初期化(DBに登録するため)
            #消費カロリーを計算する処理
            burned_cal = calc_cal(user_id,exercise_name,exercise_hour)
            con = sqlite3.connect("hist.db", check_same_thread=False, isolation_level=None)#DBに接続
            cur = con.cursor()#カーソルの定義
            #cur.execute("INSERT INTO history_exercise (user_id, exercise_name, exercise_hour, exercise_dist, burned_cal, date, delete_flag) VALUES (?,?,?,?,?,?,0)",[user_id, exercise_name, exercise_hour, exercise_dist, burned_cal, add_dt])
            cur.execute("INSERT INTO history_exercise (user_id, exercise_name, exercise_hour, burned_cal, date, delete_flag) VALUES (?,?,?,?,?,0)",[user_id, exercise_name, exercise_hour, burned_cal, add_dt])
            con.commit()#INSERTを行ったのでcommit
            cur.close()
            con.close()#commitしたのでDBから切断
            self.manager.dialogue_state.clear()#内部状態の初期化
        elif sys_act_type['sys_act_type'] == 'REGIST_INIT_INFO':#初期情報の登録を行う
            add_dt = datetime.datetime.now().replace(microsecond=0)#現在時刻の取得
        #体重と身長をpersonal_infoに挿入
            # if exists_elements('personal_info','user_id',user_id):#既に登録されているか判定
            #     sent += '既に登録されています。'
            # else:#登録されていない場合
            con = sqlite3.connect("hist.db", check_same_thread=False, isolation_level=None)#DBに接続
            cur = con.cursor()#カーソルの定義
            gender = self.manager.dialogue_state.get_gender()
            age = self.manager.dialogue_state.get_age()
            weight = self.manager.dialogue_state.get_weight()
            height = self.manager.dialogue_state.get_height()
            pal = self.manager.dialogue_state.get_pal()
            bmr = calc_bmr(gender,weight,height,age)
            req_cal = calc_req_cal(bmr,pal)
            cur.execute("INSERT INTO personal_info(user_id,gender,age,init_weight,height,pal,bmr,req_cal,date,delete_flag) VALUES (?,?,?,?,?,?,?,?,?,0)",[user_id, gender, age, weight, height, pal, bmr, req_cal, add_dt])
            con.commit()#INSERTを行ったのでcommit
            cur.close()
            con.close()#commitしたのでDBから切断
            self.manager.dialogue_state.clear()#内部状態の初期化
            sent += '初期情報の登録が完了しました'

        return sent