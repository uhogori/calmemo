# -*- coding: utf-8 -*-

from dialogue_system.knowledge.reader import read_exercise_name_list

class LanguageGenerator(object):

    #コンストラクタ
    def __init__(self):
        pass

    #応答文の生成メソッド
    def generate_reply(self, dialogue_act):
        sent = ''#返答する文章の定義
        #ユーザの入力に対する返答文を生成
        if 'FOOD_NAME' in dialogue_act:
            sent += '{}を食べたのですね。\n'.format(dialogue_act['FOOD_NAME'])
        if 'FOOD_CAL' in dialogue_act:
            sent += 'カロリーは{0}kcalですね。\n'.format(dialogue_act['FOOD_CAL'])
        if 'EXERCISE_NAME' in dialogue_act:
            sent += '運動名は{}ですね。\n'.format(dialogue_act['EXERCISE_NAME'])
        if 'EXERCISE_HOUR' in dialogue_act:
            sent += '運動時間は{}時間ですね。\n'.format(dialogue_act['EXERCISE_HOUR'])
        #if 'EXERCISE_DIST' in dialogue_act:
            #sent += '運動距離は{}kmですね。\n'.format(dialogue_act['EXERCISE_DIST'])
        if 'AGE' in dialogue_act:
            sent += '年齢は{}歳ですね。\n'.format(dialogue_act['AGE'])
        if 'WEIGHT' in dialogue_act:
            sent += '体重は{}kgですね。\n'.format(dialogue_act['WEIGHT'])
        if 'HEIGHT' in dialogue_act:
            sent += '身長は{}cmですね。\n'.format(dialogue_act['HEIGHT'])
        if 'GENDER' in dialogue_act:
            sent += '性別は{}ですね。\n'.format(dialogue_act['GENDER'])
        if 'PAL' in dialogue_act:
            sent += '身体活動レベルは{}ですね。\n'.format(dialogue_act['PAL'])
        
        #対話行為タイプに応じて処理を変えるための変数
        sys_act_type = dialogue_act['sys_act_type']
        #システムの対話行為タイプに合わせた文章を生成する条件分岐
        if sys_act_type == 'REGIST_FOOD':#食事の登録を行う
            sent += '食事の登録を行います。'
        elif sys_act_type == 'REGIST_EXERCISE':#運動の登録を行う
            sent += '運動の登録を行います。'
        elif sys_act_type == 'REGIST_INIT_INFO':
            sent += '初期情報の登録を行います。\n'
        elif sys_act_type == 'REQUEST_FOOD_NAME':
            sent += '何を食べましたか?\n対応メニュー[ラーメン","チャーハン","バナナ","リンゴ]'  
        elif sys_act_type == 'REQUEST_FOOD_CAL':
            sent += 'カロリーはいくらでしたか？'
        elif sys_act_type == 'REQUEST_EXERCISE_NAME':
            exercise_name_list = read_exercise_name_list()
            sent += '運動名を教えてください。\n対応メニュー{}'.format(exercise_name_list)
        elif sys_act_type == 'REQUEST_EXERCISE_HOUR':
            sent += '時間はどれくらいでしたか？\n(単位:時間,分が使えます)'
        #elif sys_act_type == 'REQUEST_EXERCISE_DIST':
            #sent += 'どのくらいの距離を走りましたか？(単位:km,m)\n距離が存在しない運動の場合は0を入力してください。'
        elif sys_act_type == 'REQUEST_AGE':
            sent += '年齢を入力してください。(単位は歳)\n'
        elif sys_act_type == 'REQUEST_WEIGHT':
            sent += '体重を入力してください。(単位はkg)\n'
        elif sys_act_type == 'REQUEST_HEIGHT':
            sent += '身長を入力してください。(単位はcm)\n'
        elif sys_act_type == 'REQUEST_GENDER':
            sent += '性別を入力してください。(男、女)\n'
        elif sys_act_type == 'REQUEST_PAL':
            sent += '身体活動レベルを以下の選択肢から入力してください。(選択肢の番号または数値)\n\n１：1.50(生活の大部分を座って過ごし、静的な活動が中心の場合)\n ２：1.75(主に座って行う仕事。オフィス内の移動や軽いスポーツをする人を含む)\n ３：2.00(移動や立って行うことが多い仕事の従事者。あるいは、活発な運動習慣を持っている場合)\n'
        elif sys_act_type == 'REQUEST_RETRY':#sys_act_type='OTHERの時'
            sent += 'もう一度入力してください。'
        elif sys_act_type == 'REQUEST_MODE_INIT_REGIST':
            sent += '初期情報が登録されていません。\n初期登録と入力して登録対話を行ってください。'
        elif sys_act_type == 'REGISTED_INIT_INFO':
            sent += '既に登録されています。'
        elif sys_act_type == 'REQUEST_MODE':
            sent += '対話モードを以下の選択肢から入力してください。\n選択肢[食事登録:食事 運動登録:運動 初期情報登録:初期登録]'
        
        return sent