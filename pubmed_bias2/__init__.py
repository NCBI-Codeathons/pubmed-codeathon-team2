# +
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
from collections import Counter
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import requests
import xmltodict
import json
from .pubmed_preprocessing import get_click_data, get_pmids, parse_save, count_sort_algorithm, one_hot_a_column
class pubmed_bias2():
    def __init__(self,
                 input_file='pubmed-data.tsv',
                 input_path='/data/', 
                 output_path = '/data/team2/', 
                 filename='processed_pubmed_data'
                 ):
        
        self.input_path = input_path
        self.input_file = input_file
        self.output_path = output_path
        self.filename = filename
        
    def load_data(self):
        try:
            if  self.input_file.split('.')[1] == 'tsv':
                raw_data = pd.read_csv(self.input_path + self.input_file, sep='\t')
                print("reading in " + self.input_path + self.input_file + ". Output file = " + self.output_path + self.filename)
                
            elif  self.input_file.split('.')[1] == 'csv':
                raw_data = pd.read_csv(self.input_path + self.input_file)
                print("reading in " +  self.input_path + self.input_file + ". Output file = " + self.output_path + self.filename)
            else:
                print("unsupported format")
                
        except IndexError:
                print("unsupported format")
               
        except AttributeError:
                print("unsupported format")
        return raw_data
    
    def merge_click_data(df1, click_filename):
        click_data = pd.read_csv(click_filename, sep='\t')
        click_data.rename(columns={'date':'clicks_date_sort','relevance': 'clicks_relevance_sort'},inplace=True)
        click_data.PMID = click_data.PMID.astype(str)
        
        df1.pmid = df1.pmid.astype(str)
        return df1.merge(click_data, left_on='pmid', right_on='PMID',how='left')
    
    def save_pubmed(self):
        self.data_one_hot.to_csv(self.output_path + self.filename + ".csv")
        self.data_one_hot.to_pickle(self.output_path + self.filename + '.pkl')
        
    def run_pipeline(self):
        '''
        Run the full pipeline for analyzing bias from team 2
        '''

        get_click_data(self)
        self.raw_data = pubmed_bias2.load_data(self)
        print("get PMIDS")
        self.data_pmid, self._most_common, self._most_common_ids, self.most_common_dict = get_pmids(self.raw_data)
        self.summary_sort_algo = count_sort_algorithm(self.data_pmid)
        self.data_parsed = parse_save(self)
        print("one-hot encode pubtypes")
        self.data_one_hot = one_hot_a_column(self.data_parsed, 'pubtype')
        self.data_full = pubmed_bias2.merge_click_data(self.data_one_hot, self.output_path + 'click_data1.tsv')
        print("save to csv and pkl")
        pubmed_bias2.save_pubmed(self)
        return self
    
#if __name__ == '__main__':
  #  main()       
    
        
        

