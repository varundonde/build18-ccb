import math
import numpy as np
import sys

def main():
    # extract labels
    dataset = np.genfromtxt(input_file, delimiter="\t", dtype=str)
    data_len = len(dataset)
    labels = dataset[:, -1]

    # get a freq of the labels
    unique_labels, freqs = np.unique(labels, return_counts=True)

    # calculate entropy
    entropy = 0
    for f in freqs:
        entropy -= ((f/data_len) * math.log2(f/data_len))

    # calculate majority vote error rate
    max_freq = max(freqs)
    error_rate = max_freq/data_len

    with open(output_file, 'w') as file:
        file.write(f"entropy: {entropy}\n")
        file.write(f"error: {error_rate}\n")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    main()


