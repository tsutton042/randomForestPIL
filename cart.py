import pandas as pd
import numpy as np
from tree import TreeNode, Split

def gini_coeff(target: pd.Series, categories: list[object]):
    """
    Basic implementation of the Gini coefficient
    """
    props = [(target[target == cat].shape[0]/target.shape[0])**2 for cat in categories]
    return 1 - sum(props)


def get_best_split(column: pd.Series) -> tuple[Split, float]:
    pass


def CART(data: pd.DataFrame, target: pd.Series, current_node: TreeNode, categories = None, thresh: float = 0.95):
    """
    Basic implemtentation of the CART algorithm using recursion and side-effects
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