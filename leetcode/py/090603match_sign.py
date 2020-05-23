#encoding=utf-8
"""
-------------------------------------------------
   File Name：     match_sign
   Description :
   Author :       naruto
   date：          6/3/19
-------------------------------------------------
   Change Activity:
                   6/3/19:
-------------------------------------------------
"""
__author__ = 'naruto'

import os

def isValid(s):
    stack=[] #最终的ｓｔａｃｋ是否为空判断是否匹配，为空就匹配
    sign_map={")":"(","}":"{","]":"["}#如果匹配一定是等到反括号，巧妙
    for i in s:#不能用ｗｈｉｌｅ　ｓｔａｃｋ　is not None
        if i not in sign_map:#开始时入ｓｔａｃｋ
            stack.append(i)
        else :#碰到反括号
            if sign_map[i]!=stack.pop():#和最近的比较是否匹配
                return False
            # else:stack.pop()　上一次判断已经ｐｏｐ，由于这里一定是严格匹配，所以ｐｏｐ后对下面的判断无影响
    if stack:
        return False
    else:
        return True
print(isValid("{[()]}"))


