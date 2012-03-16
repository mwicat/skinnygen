'''
Created on Jun 17, 2011

@author: lebleu1
'''


SKINNY_LBL_EMPTY = 0
SKINNY_LBL_REDIAL = 1
SKINNY_LBL_NEWCALL = 2
SKINNY_LBL_HOLD = 3
SKINNY_LBL_TRANSFER = 4
SKINNY_LBL_CFWDALL = 5
SKINNY_LBL_CFWDBUSY = 6
SKINNY_LBL_CFWDNOANSWER = 7
SKINNY_LBL_BACKSPACE = 8
SKINNY_LBL_ENDCALL = 9
SKINNY_LBL_RESUME = 10
SKINNY_LBL_ANSWER = 11

SKINNY_LBL_PARK = 14
SKINNY_LBL_DND = 19


SKINNY_LBL_RINGOUT = 34
SKINNY_LBL_DIAL = 101


SOFT_KEYS_LABELS_TO_EVENT={
                           'Redial' : SKINNY_LBL_REDIAL,
                           'NewCall' : SKINNY_LBL_NEWCALL,
                           'Hold' : SKINNY_LBL_HOLD,
                           'Transfer' :SKINNY_LBL_TRANSFER,
                           'EndCall' : SKINNY_LBL_ENDCALL,
                           'Answer' : SKINNY_LBL_ANSWER 
                           }


