# -*- coding: utf-8 -*-
import copy

from dialogue_system.language_understanding.attribute_extraction.rule_based_extractor import RuleBasedAttributeExtractor
from dialogue_system.language_understanding.dialogue_act_type.rule_based_estimator import RuleBasedDialogueActTypeEstimator

#attribute_extractor(属性抽出器)とestimator(行動推定器)から，ユーザーの入力文理解を行うクラス
class RuleBasedLanguageUnderstanding(object):

    def __init__(self):
        self.__estimator = RuleBasedDialogueActTypeEstimator()
        self.__extractor = RuleBasedAttributeExtractor()

    def execute(self, sent):
        #ユーザーからの入力文をsentとして受け取り，属性抽出を行う
        attribute = self.__extractor.extract(sent)
        #抽出した属性から，ユーザーの行動を推定する
        act_type = self.__estimator.estimate(attribute)
        dialogue_act = {'user_act_type':act_type}
        attribute_cp = copy.copy(attribute)
        #属性値が入力されている属性以外を削除するfor文
        for keyword, val in attribute_cp.items():
            if val == '':
                del attribute[keyword]
        #属性を指定して，システムの内部状態を更新する処理
        dialogue_act.update(attribute)
        
        return dialogue_act