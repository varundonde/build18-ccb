import argparse
import numpy as np

class Node:
    '''
    Here is an arbitrary Node class that will form the basis of your decision
    tree. 
    Note:
        - the attributes provided are not exhaustive: you may add and remove
        attributes as needed, and you may allow the Node to take in initial
        arguments as well
        - you may add any methods to the Node class if desired 
    '''
    def __init__(self):
        self.left = None
        self.right = None
        self.attr = None
        self.vote = None
    
def print_tree(Node):
    pass

if __name__ == '__main__':
    # This takes care of command line argument parsing for you!
    # To access a specific argument, simply access args.<argument name>.
    # For example, to get the train_input path, you can use `args.train_input`.
    parser = argparse.ArgumentParser()
    parser.add_argument("train_input", type=str, help='path to training input .tsv file')
    parser.add_argument("test_input", type=str, help='path to the test input .tsv file')
    parser.add_argument("max_depth", type=int, 
                        help='maximum depth to which the tree should be built')
    parser.add_argument("train_out", type=str, 
                        help='path to output .txt file to which the feature extractions on the training data should be written')
    parser.add_argument("test_out", type=str, 
                        help='path to output .txt file to which the feature extractions on the test data should be written')
    parser.add_argument("metrics_out", type=str, 
                        help='path of the output .txt file to which metrics such as train and test error should be written')
    parser.add_argument("print_out", type=str,
                        help='path of the output .txt file to which the printed tree should be written')
    args = parser.parse_args()
    
    #Here's an example of how to use argparse
    print_out = args.print_out

    #Here is a recommended way to print the tree to a file
    # with open(print_out, "w") as file:
    #     print_tree(dTree, file)


# calculate mutual information 
# choose attribute with highest MI
# split dataset on this attribute, recording depth
# if max depth has been reached or it caanot be split further(MI = 0)
# make it a leaf node based on majorityvote
# then call this algo recursively in this split datasey

def mutual_info(data, feature_col_idx):
    data_len = len(data)
    l_neg_f_neg = 0
    l_neg_f_pos = 0
    l_pos_f_neg = 0
    l_pos_f_pos = 0
    l_neg = 0
    l_pos = 0
    f_neg = 0
    f_pos = 0

    for row in data:
        feature_val = row[feature_col_idx]
        label_val = row[-1]
        if feature_val == 0 and label_val == 0:
            l_neg_f_neg +=1
            l_neg += 1
            f_neg += 1
        elif feature_val == 0 and label_val == 1:
            l_neg_f_pos += 1
            l_neg += 1
            f_pos += 1
        elif feature_val == 1 and label_val == 0:
            l_pos_f_neg += 1
            l_pos += 1
            f_neg += 1
        else:
            l_pos_f_pos += 1
            l_pos += 1
            f_pos += 1

    l_entropy = (-(l_neg / data_len) * np.log2(l_neg / data_len) 
                 -(l_pos / data_len) * np.log2(l_pos / data_len))
    
    f0_entropy = (-(l_neg_f_neg / f_neg) * np.log2(l_neg_f_neg / f_neg)
                  -(l_pos_f_neg / f_neg) * np.log2(l_pos_f_neg / f_neg))
    
    f1_entropy = (-(l_neg_f_pos / f_pos) * np.log2(l_neg_f_pos / f_pos)
                  -(l_pos_f_pos / f_pos) * np.log2(l_pos_f_pos / f_pos))
    
    f_entropy = ((f_neg / data_len) * f0_entropy 
                (f_pos / data_len) * f1_entropy)
    
    mi = l_entropy - f_entropy

    return mi


def majority_vote(data,):
    labels = data[:, -1]
    label_values = np.bincount(labels.astype(int))
    return 1 if label_values[1] >= label_values[0] else 0


def train(data, headers, depth, max_depth):

    # if max depth is reached, return leaf node
    if depth >= max_depth:
        leaf = Node()
        leaf.vote = majority_vote(data)
        return leaf
    
    # if all labels are the same, return leaf node
    unique_labels = np.unique(data[:, -1])
    if len(unique_labels) == 1:
        leaf = Node()
        leaf.vote = unique_labels[0]
        return leaf
    
    # number of headers
    num_cols = len(headers)
    print(f"num_cols = {num_cols}")
    
    # find and record feature with max mutual info
    max_MI = -1
    splitting_feature_index = None
    for i in range(num_cols-1):
        MI = mutual_info(data, i)
        if MI > max_MI:
            max_MI = MI
            splitting_feature_index = i

    # if mutual information is 0, return leaf node
    if max_MI == 0:
        leaf = Node()
        leaf.vote = majority_vote(data)
        return leaf

    # split dataset on feature
    D_feature_0 = data[data[:, splitting_feature_index] == 0]
    D_feature_1 = data[data[:, splitting_feature_index] == 1]

    # recursively build left and right trees
    node = Node()
    node.left = train(D_feature_0, depth + 1, max_depth)
    node.right = train(D_feature_1, depth + 1, max_depth)


def main():
    training_data = np.genfromtxt(args.train_input, delimiter="\t", skip_header=1) 
    training_data_headers = np.genfromtxt(args.train_input, delimiter="\t", max_rows=1)
    train(training_data, training_data_headers, 0, 3)
    
    

    



