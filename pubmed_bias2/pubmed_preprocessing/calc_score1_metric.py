#!/usr/bin/env python3

import pandas as pd


def calc_score1_metric(query_term, df):
    '''
    Function to calculate the index of the article (where it appeared in the search results).
    Index is calculated by looking at page number and position on the page. For example,
    if Article A is on Page 1, Position 1 (aka the first result), then its index is 1. If
    Article B is on Page 2, Position 1, then its index is 11.
    
    :param: query_term, 
    
    :param: df, pandas dataframe that contains the searches of a specific query.For example,
                if we want to calculate indexes for articles that resulted from "covid-19" query,
                we would filter our original dataset for "covid-19" and apply this function to this
                filtered dataframe.
    :return: pmid_score1_info, dictionary with the key being the PMID and the value being the average index.
    
    '''
    df = df[(df.query_term == query_term)]
    pmid_score1_info = {}
    for i in range(len(df)):
        pmid_list = df['PMID'].iloc[i].split(',')
        for pmid in pmid_list:
            page_num = df['page_num'].iloc[i]
            location_on_page  = pmid_list.index(pmid) + 1
            pmid_index = (page_num - 1)*10 + location_on_page
            if pmid not in pmid_score1_info:
                pmid_score1_info[pmid] = [1, pmid_index]
            else:
                pmid_score1_info[pmid][0] += 1 # [0] is the count
                pmid_score1_info[pmid][1] += pmid_index

    for pmid in pmid_score1_info:
        score = pmid_score1_info[pmid][1]/pmid_score1_info[pmid][0]
        pmid_score1_info[pmid] = score
        
    return pmid_score1_info
