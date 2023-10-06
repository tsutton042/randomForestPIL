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


def gini_coeff(target: pd.Series, categories: list[object]):
    props = [(target[target == cat].shape[0]/target.shape[0])**2 for cat in categories]
    return 1 - sum(props)


def get_best_split(data: pd.Series) -> tuple[Split, float]:
    pass


def CART(data: pd.DataFrame, target: pd.Series, current_node: TreeNode, categories = None, thresh: float = 0.95):
    """
    Implemtents the CART algorithm using recursion and side-effects
    Not the greatest fan of this for readability reasons, but easier to write
    """
    # in the first call, obtain the categories
    if categories is None:
        categories = np.unique(target)
    # evaluate stopping criterion (base case)
    props = [target[target == cat].shape[0]/target.shape[0] for cat in categories]
    pos = np.argmax(props)
    if props[pos] < thresh:
        current_node.is_leaf = True
        current_node.set_category(categories[pos])
    else:
        # get the "best" split of the input features
        candidate_splits = [get_best_split(data[col]) for col in data.columns]
        # get the best of the "best" splits
        best_idx = np.argmax(score for _, score in candidate_splits)
        split = candidate_splits[best_idx][0]
        # perform the split (ie break the data into halves based on 
        # how it performs against the split and create a node for each portion of the data)
        send_to_left = (split.send(data) == "left")
        left_data = data[send_to_left]
        right_data = data[~send_to_left]
        left_target = target[send_to_left]
        right_target = target[~send_to_left]
        left = TreeNode(parent=current_node)
        right = TreeNode(parent=current_node)
        current_node.set_split(split, left, right)
        # do the same for the new nodes
        CART(left_data, left_target, left)
        CART(right_data, right_target, right)