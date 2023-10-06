import pandas as pd
import numpy as np
import warnings


class Split:
    """
    Helper class for trees; stores info about the split
    """
    def __init__(self, variable: str, equation: str):
        self.var = variable
        self.equation = equation

    def send(self, data_point):
        return "left" if eval(f"{data_point[self.var]} {self.equation}") else "right"
    

class TreeNode:
    def __init__(self, parent = None, is_leaf: bool = False) -> None:
        # note that this method expects parent to be of type TreeNode
        self.parent = parent
        self.is_leaf = is_leaf

    def set_split(self, split: Split, left, right) -> None:
        # Note that this method expects left and right to be of type TreeNode as well
        if not self.is_leaf:
            self.split = split
            self.left = left
            self.right = right
        else:
            warnings.warn("Trying to set a split when the node is a leaf")

    def set_category(self, category):
        if self.is_leaf:
            self.category = category
        else:
            warnings.warn("Trying to set the category of a node when it's not a leaf")

    def traverse(self, data_point):
        """
        Return the relevant node, depending on how the data is split
        """
        return eval(f"self.{self.split.send(data_point)}")
