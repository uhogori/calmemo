# -*- coding: utf-8 -*-
class DialogueState(object):

    #コンストラクタ(内部状態が持ちうる属性を定義)
    def __init__(self):
        self.__state = {'FOOD_NAME':None,
                        'FOOD_CAL':None,
                        'EXERCISE_NAME':None,
                        'EXERCISE_HOUR':None,
                        #'EXERCISE_DIST':None,
                        'AGE':None,
                        'WEIGHT':None,
                        'HEIGHT':None,
                        'GENDER':None,
                        'PAL':None,
                        'MODE':None
                        }

    #内部状態の更新処理
    def update(self,dialogue_act):
        self.__state['FOOD_NAME'] = dialogue_act.get('FOOD_NAME', self.__state['FOOD_NAME'])
        self.__state['FOOD_CAL'] = dialogue_act.get('FOOD_CAL', self.__state['FOOD_CAL'])
        self.__state['EXERCISE_NAME'] = dialogue_act.get('EXERCISE_NAME', self.__state['EXERCISE_NAME'])
        self.__state['EXERCISE_HOUR'] = dialogue_act.get('EXERCISE_HOUR', self.__state['EXERCISE_HOUR'])
        #self.__state['EXERCISE_DIST'] = dialogue_act.get('EXERCISE_DIST', self.__state['EXERCISE_DIST'])
        self.__state['AGE'] = dialogue_act.get('AGE', self.__state['AGE'])
        self.__state['WEIGHT'] = dialogue_act.get('WEIGHT', self.__state['WEIGHT'])
        self.__state['HEIGHT'] = dialogue_act.get('HEIGHT', self.__state['HEIGHT'])
        self.__state['GENDER'] = dialogue_act.get('GENDER', self.__state['GENDER'])
        self.__state['PAL'] = dialogue_act.get('PAL', self.__state['PAL'])
        self.__state['MODE'] = dialogue_act.get('MODE', self.__state['MODE'])
    #引数で属性名を渡し、内部状態が値を持っているか確認するメソッド
    def exist(self, name):
        return self.__state.get(name, None) != None
    
    #食品の名前を取得するメソッド(ゲッター)
    def get_fname(self):
        return self.__state['FOOD_NAME']

    def get_cal(self):
        return self.__state['FOOD_CAL']

    def get_ename(self):
        return self.__state['EXERCISE_NAME']

    def get_hour(self):
        return self.__state['EXERCISE_HOUR']
    
    # def get_dist(self):
    #     return self.__state['EXERCISE_DIST']
    
    def get_age(self):
        return self.__state['AGE']

    def get_weight(self):
        return self.__state['WEIGHT']

    def get_height(self):
        return self.__state['HEIGHT']

    def get_gender(self):
        return self.__state['GENDER']

    def get_pal(self):
        return self.__state['PAL']
    
    def get_mode(self):
        return self.__state['MODE']

    #内部状態を初期化するメソッド
    def clear(self):
        self.__init__()

    def __str__(self):
        import pprint
        return pprint.pformat(self.__state)