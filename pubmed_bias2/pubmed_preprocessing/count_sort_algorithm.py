#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def count_sort_algorithm(data):
    print(f"Median number of search results: {data['num_results'].median()}")
    plt.hist(data['num_results'])
    plt.title("Number of results (all searches)");
    
    return data['sort_algorithm'].value_counts().to_dict()
