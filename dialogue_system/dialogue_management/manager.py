# -*- coding: utf-8 -*-
from copy import deepcopy
from dialogue_system.dialogue_management.state import DialogueState
class DialogueManager(object):

    #システムが持ちうる内部状態(state)をメンバ変数として定義
    #ここではstate.pyのDialogueStateクラスのコンストラクタを呼び出している
    def __init__(self):
        self.dialogue_state = DialogueState()

    #システムの内部状態を更新するメソッド
    #dialogue_act = システムが聞くこと
    #sys_act = dialogue_actのコピー(オブジェクト自体のコピー(アドレスも参照先も別))
    #user_act_type = ユーザーが聞いたことの推定
    def update_dialogue_state(self, dialogue_act):
        self.dialogue_state.update(dialogue_act)

    def select_action(self, dialogue_act):
        #オブジェクトに対してcopyメソッドを使用した場合
        #コピーされたオブジェクトの値を変更するとコピー元の値も変更される
        #なのでdeepcopyメソッドを用いている(異なるアドレスを持つ新たなオブジェクトがコピーとして生成される)
        sys_act = deepcopy(dialogue_act)
        if self.dialogue_state.get_mode() is not None:#システムの内部状態で対話モードが選択されている場合
            mode = self.dialogue_state.get_mode()
            if mode == '食事':#対話モードが食事登録の場合
                if not self.dialogue_state.exist('FOOD_NAME'):
                    sys_act['sys_act_type'] = 'REQUEST_FOOD_NAME'
                elif not self.dialogue_state.exist('FOOD_CAL'):
                    sys_act['sys_act_type'] = 'REQUEST_FOOD_CAL'
                else:#食事情報を登録するための内部状態が揃っている場合
                    sys_act['sys_act_type'] = 'REGIST_FOOD'
            elif mode == '運動':#対話モードが運動登録の場合
                if not self.dialogue_state.exist('EXERCISE_NAME'):
                    sys_act['sys_act_type'] = 'REQUEST_EXERCISE_NAME'
                elif not self.dialogue_state.exist('EXERCISE_HOUR'):
                    sys_act['sys_act_type'] = 'REQUEST_EXERCISE_HOUR'
                # elif not self.dialogue_state.exist('EXERCISE_DIST'):
                #     sys_act['sys_act_type'] = 'REQUEST_EXERCISE_DIST'
                else:#運動情報登録のための内部状態が揃っている場合
                    sys_act['sys_act_type'] = 'REGIST_EXERCISE'
            elif mode == '初期登録':
                if not self.dialogue_state.exist('AGE'):
                    sys_act['sys_act_type'] = 'REQUEST_AGE'
                elif not self.dialogue_state.exist('WEIGHT'):
                    sys_act['sys_act_type'] = 'REQUEST_WEIGHT'
                elif not self.dialogue_state.exist('HEIGHT'):
                    sys_act['sys_act_type'] = 'REQUEST_HEIGHT'
                elif not self.dialogue_state.exist('GENDER'):
                    sys_act['sys_act_type'] = 'REQUEST_GENDER'
                elif not self.dialogue_state.exist('PAL'):
                    sys_act['sys_act_type'] = 'REQUEST_PAL'
                else:#個人情報が全て揃った場合
                    sys_act['sys_act_type'] = 'REGIST_INIT_INFO'
            elif sys_act['user_act_type'] == 'OTHER':#ユーザの入力文からどの属性も抽出できなかった場合
                sys_act['sys_act_type'] = 'REQUEST_RETRY'#現在の対話を繰り返す
        else:#対話モードが最初に選択されていない場合
            sys_act['sys_act_type'] = 'REQUEST_MODE'

        return sys_act