# -*- coding: utf-8 -*-
#ユーザーの入力文から属性を抽出するクラス
from dialogue_system.knowledge.reader import read_exercise_name_list

class RuleBasedAttributeExtractor(object):

    def __init__(self):
        self.__exercise_name = read_exercise_name_list()#事前に定義された運動名のリスト

    def extract(self, text):
        attribute = {'FOOD_NAME':self.__extract_food_name(text),
                     'FOOD_CAL':self.__extract_food_cal(text),
                     'EXERCISE_NAME':self.__extract_exercise_name(text),
                     'EXERCISE_HOUR':self.__extract_exercise_hour(text),
                     #'EXERCISE_DIST':self.__extract_exercise_dist(text),
                     'AGE':self.__extract_age(text),
                     'WEIGHT':self.__extract_weight(text),
                     'HEIGHT':self.__extract_height(text),
                     'GENDER':self.__extract_gender(text),
                     'PAL':self.__extract_pal(text),
                     'MODE':self.__extract_ask_mode(text)}#対話モードの管理を行う内部状態(属性値：'食事'or'運動')
        return attribute
    
    def __extract_food_name(self, text):
        text = str(text)
        food_name_list = {"ラーメン","チャーハン","バナナ","リンゴ"}#入力可能な食事の名前をここに定義
        food_name = ''#返り値用の変数
        for f in food_name_list:
            if f == text:#入力された文章と要素が一致した場合
                food_name = f
                return food_name#一致した食事名を返す
        if food_name == '':#何も一致せず初期値のままの場合
            return food_name#空を返す

    #食事のカロリーの属性を抽出する関数
    #DBにはkcalの形式で格納する予定(1cal = 0.001kcal)
    #なので，food_calのカラムはFLOAT型で定義
    def __extract_food_cal(self, text):
        text = str(text)
        food_cal = ''
        if text.endswith('kcal') and text[0].isdigit():
            text = text.replace('kcal','')
            if text.isdecimal() and text.isascii():
                food_cal = float(text)
                return round(food_cal,1)
            else:
                return ''
        elif text.endswith('cal') and text[0].isdigit():
            text = text.replace('cal','')
            if text.isdecimal() and text.isascii():
                food_cal = float(text) / 1000
                return round(food_cal,4)
            else:
                return ''
        else:
            return ''

    def __extract_exercise_name(self, text):
        text = str(text)
        exercise_name = ''
        for name in self.__exercise_name:
            if name == text:#入力された文字と登録されている運動名が一致した場合
                exercise_name = name
                return exercise_name
        if exercise_name == '':#どの運動名とも一致しなかった場合
            return exercise_name

    def __extract_exercise_hour(self, text):#属性値は分に変換して返す(例：1時間=60分)
        text = str(text)
        if all(map(text.__contains__, ('時間','分'))) and text.endswith('分') and text[0].isdigit():#入力形式が「1時間30分」のような場合
            text = text.replace('時間', ' ').replace('分', ' ')#"時間", "分"を置換
            hour = text.split()[0]#正しくreplaceされた場合，text=[1 30]のような空白文字で区切られた文字列になるので，空白文字で時間と分に分割
            minute = text.split()[1]
            if hour.isdecimal and minute.isdecimal and hour.isascii() and minute.isascii():#半角数字かつ数字のみで構成されている場合
                exercise_hour = float(hour) + float(minute)/60.0
                return round(exercise_hour,2)#運動時間を返す
            else:
                return ''
        elif text.endswith('時間') and text[0].isdigit():#入力形式が「１時間」のような場合
            text = text.replace('時間', ' ')
            exercise_hour = text.split(' ')[0]
            if exercise_hour.isdecimal() and exercise_hour.isascii():
                return round(float(exercise_hour),2)
            else:
                return ''
        elif text.endswith('分') and text[0].isdigit():
            text = text.replace('分', ' ')
            exercise_hour = text.split(' ')[0]
            if exercise_hour.isdecimal() and exercise_hour.isascii():
                return round((float(exercise_hour)/60.0),2)
            else:
                return ''
        else:
            return ''

    # def __extract_exercise_dist(self, text):#単位はkm,m
    #     text = str(text)
    #     text = text.lower()
    #     if text.endswith('km') and text[0].isdigit():
    #         text = text.replace('km', ' ')
    #         dist = text.split(' ')[0]
    #         if dist.isdecimal() and dist.isascii():
    #             return float(dist)
    #         else:
    #             return ''
    #     elif text.endswith('m') and text[0].isdigit() and not text.endswith('cm'):
    #         text = text.replace('m', ' ')
    #         dist = text.split(' ')[0]
    #         if dist.isdecimal() and dist.isascii():
    #             dist = float(dist)/1000#km単位に変換
    #             return dist
    #         else:
    #             return ''
    #     else:#入力形式が違う場合
    #         return ''

    def __extract_age(self,text):#年齢属性の抽出
        text = str(text)
        if text.endswith('歳') and text[0].isdigit():
            text = text.replace('歳',' ')
            age = text.split(' ')[0]
            if age.isdecimal() and age.isascii():
                return age
            else:
                return ''#全角で入力されていた場合は受け付けない
        else:#入力形式が違う
            return ''

    def __extract_weight(self,text):#体重属性の抽出
        text = str(text)
        text = text.lower()
        if text.endswith('kg') and text[0].isdigit():
            text = text.replace('kg',' ')
            weight = text.split(' ')[0]
            if weight.isdecimal() and weight.isascii():
                return weight
            else:
                return ''
        else:
            return ''

    def __extract_height(self,text):#身長属性の抽出
        text = str(text)
        text = text.lower()
        if text.endswith('cm') and text[0].isdigit():
            text = text.replace('cm',' ')
            height = text.split(' ')[0]
            if height.isdecimal() and height.isascii():
                return height
            else:
                return ''
        else:
            return ''

    def __extract_gender(self,text):#性別属性の抽出
        text = str(text)
        if text == '男':
            return '男'
        elif text == '女':
            return '女'
        else:
            return ''

    def __extract_pal(self,text):#身体活動レベルの抽出
        text = str(text)
        if text == '1' or text == 1.50:#選択肢形式の方が入力しやすいか?(1:1.50,2:1.75,3:2.00)
            return 1.50
        elif text == '2' or text == 1.75:
            return 1.75
        elif text == '3' or text == 2.00:
            return 2.00
        else:
            return ''

    #入力された文章が｢食事｣or｢運動｣の場合(対話開始のトリガー)
    def __extract_ask_mode(self, text):
        text = str(text)
        if text == '食事':
            return '食事'
        elif text == '運動':
            return '運動'
        elif text == '初期登録':
            return '初期登録'
        else:
            return ''