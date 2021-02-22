import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt


def load_data(path):
    with gzip.open(path, "rb") as f:
        return pickle.load(f)
    return dict()


if __name__ == "__main__":
    pass