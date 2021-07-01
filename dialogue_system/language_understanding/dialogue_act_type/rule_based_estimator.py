# -*- coding: utf-8 -*-
#抽出された属性から，ユーザーの入力行動タイプの推定を行うクラス

class RuleBasedDialogueActTypeEstimator(object):
    
    def __init__(self):
        pass

    def estimate(self, attribute):
        if attribute['MODE'] == '食事':
            return 'SELECT_MODE_FOOD'
        elif attribute['MODE'] == '運動':
            return 'SELECT_MODE_EXERCISE'
        elif attribute['MODE'] == '初期登録':
            return 'SELECT_MODE_INIT_REGIST'
        elif attribute['FOOD_NAME'] != '':
            return 'INFORM_FOOD_NAME'
        elif attribute['FOOD_CAL'] != '':
            return 'INFORM_FOOD_CAL'
        if attribute['EXERCISE_NAME'] != '':
            return 'INFORM_EXERCISE_NAME'
        elif attribute['EXERCISE_HOUR'] != '':
            return 'INFORM_EXERCISE_HOUR'
        #elif attribute['EXERCISE_DIST'] != '':
            #return 'INFORM_EXERCISE_DIST'
        elif attribute['AGE'] != '':
            return 'INFORM_AGE'
        elif attribute['WEIGHT'] != '':
            return 'INFORM_WEIGHT'
        elif attribute['HEIGHT'] != '':
            return 'INFROM_HEIGHT'
        elif attribute['GENDER'] != '':
            return 'INFORM_GENDER'
        elif attribute['PAL'] != '':
            return 'INFORM_PAL'
        else:#入力文からどの属性も抽出されなかった場合
            return 'OTHER'
