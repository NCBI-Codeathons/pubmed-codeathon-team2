# +
# # !/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import Counter
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import numpy as np
import requests
import xmltodict
import json
from .config import SampleQueries
from .pubmed_preprocessing.pubmed import SampleSet
from .pubmed_preprocessing import get_click_data, one_hot_a_column

QUERIES = SampleQueries.BOTTOM_10_QUERIES + SampleQueries.TOP_10_QUERIES

class pubmed_bias2():


    def __init__(self,
                 input_file='pubmed-data.tsv',
                 input_path='/data/', 
                 output_path = '/data/team2/', 
                 filename='processed_pubmed_data',
                 click_data_filename = 'click_data_1'
                 ):
        
        self.input_path = input_path
        self.input_file = input_file
        self.output_path = output_path
        self.filename = filename
        self.click_data_filename = click_data_filename
        
    def load_data(self):
        '''
        Import a .tsv or .csv file
        '''
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
        '''
        Merge a dataframe with metadata with the click data.
        
        Inputs:
        df1: (dataframe) a pandas dataframe that contains the pmid (one per row) in a column named "pmid" and any other columns of metadata.
        click_filename: (str,required) the full path and name of the .tsv file where the counts of clicks per pmid are stored e.g. "/data/team2/click_data_1"
        
        Outputs:
        df1: (dataframe) the two dataframes merged on the PMID
        '''
        
        click_data = pd.read_csv(click_filename, sep='\t')
        click_data.rename(columns={'date':'clicks_date_sort','relevance': 'clicks_relevance_sort'},inplace=True)
        click_data.PMID = click_data.PMID.astype(str)
        
        df1.pmid = df1.pmid.astype(str)
        return df1.merge(click_data, left_on='pmid', right_on='PMID',how='left').drop(columns=['PMID'])
    
    
    def organize_query(df_q, query):
        '''
        Create a new dataframe for the top/bottom 10 query results that gives one PMID per row and populates columns for features.
        Top and bottom 10 dataframes are concatenated to create one dataframe as output.
        INPUTS:
        df_q: (dataframe, required) a pandas dataframe that contains the results of multiple queries. Each row is a query.
        query: (str, required) the query string
        
        OUTPUT:
        a new dataframe that is concatenated for top and bottom results from the query
        '''
        df = pd.DataFrame(df_q.loc[query,'relevance_res'],columns=['PMID'])
        df['query']=query
        df['sort'] = 'relevance_res'
        df['rank'] = df.index+1

        df1 = pd.DataFrame(df_q.loc[query,'date_desc_res'],columns=['PMID'])
        df1['query']=query
        df1['sort'] = 'date_desc_res'
        df1['rank'] = df1.index+1

        return pd.concat([df,df1])

    def merge_query_meta(df1, df2):
        '''
        Concatenate multiple dataframes together for multiple queries. Merge these query results with the metatdata for each pmid. Binarize the fulltext status
        INPUT:
        df1: (dataframe) a dataframe of the query results. one query per row
        df2: (dataframe) the metadata per PMID
        
        OUTPUT:
        dataframe of all the info joined on PMID
        '''

        row=0
        for i in df1.index.to_list():
            if row==0:
                query_meta_df = pubmed_bias2.organize_query(df1, i)
                row +=1
            else:
                query_meta_df = pd.concat([query_meta_df, pubmed_bias2.organize_query(df1, i)])
                row+=1

        query_meta_df.PMID = query_meta_df.PMID.astype(str)
        df2.pmid = df2.pmid.astype(str)
        query_meta_df = query_meta_df.merge(df2, left_on='PMID', right_on='pmid', how='left').drop(columns=['pmid'])
        query_meta_df['fulltext_status'] = query_meta_df['fulltext_status'].astype('category')
        query_meta_df['has_fulltext']= query_meta_df['fulltext_status'].cat.codes
        return query_meta_df

    def save_pubmed(self):
        '''
        Save the results to .csv and .pkl files
        '''
        self.data_full.to_csv(self.output_path + self.filename + "_full.csv")
        self.data_full.to_pickle(self.output_path + self.filename + '_full.pkl')
        
        self.data_query_meta.to_csv(self.output_path + self.filename + "_query_meta.csv")
        self.data_query_meta.to_pickle(self.output_path + self.filename + '_query_meta.pkl')
        
    def run_pipeline(self):
        '''
        Run the full pipeline for analyzing bias from team 2
        '''

        get_click_data(self.input_path, self.input_file, self.output_path, self.click_data_filename)
        self.raw_data = pubmed_bias2.load_data(self)
        print("get PMIDS")
        #self.summary_sort_algo = count_sort_algorithm(self.data_pmid)
        self.samples = SampleSet(QUERIES, testing_only=False)
        self.results = self.samples.results
        self.metadata = self.samples.pmid_metadata
        #print("one-hot encode pubtypes")
        #self.data_one_hot = one_hot_a_column(self.metadata, 'pubtype')
        self.data_full = pubmed_bias2.merge_click_data(self.metadata, self.output_path + self.click_data_filename + '.tsv')
        self.data_query_meta = pubmed_bias2.merge_query_meta(self.results, self.data_full)
        print("save to csv and pkl")
        pubmed_bias2.save_pubmed(self)
        return self
