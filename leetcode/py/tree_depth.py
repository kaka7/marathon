# -*- coding:utf-8 -*-
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def TreeDepth(self, pRoot):
        depth = 0
        if (pRoot):
            depth = depth + 1
            d1 = 0
            d2 = 0
            if (pRoot.left): d1 = self.TreeDepth(pRoot.left)
            if (pRoot.right): d2 = self.TreeDepth(pRoot.right)
            if d1 > d2:
                return d1 + depth
            else:
                return d2 + depth
        else:
            pass

        return depth

        # write code here