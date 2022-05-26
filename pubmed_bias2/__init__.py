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
                self.raw_data = pd.read_csv(self.input_path + self.input_file, sep='\t')
                print("reading in " + self.input_path + self.input_file + ". Output file = " + self.output_path + self.filename)
                
            elif  self.input_file.split('.')[1] == 'csv':
                self.raw_data = pd.read_csv(self.input_path + self.input_file)
                print("reading in " +  self.input_path + self.input_file + ". Output file = " + self.output_path + self.filename)
            else:
                print("unsupported format")
                
        except IndexError:
                print("unsupported format")
               
        except AttributeError:
                print("unsupported format")
        return self
    
    def get_pmids(self):
        '''
        extract the pmid information and add to data frame.
        INPUT: data
        OUTPUT: data with an added column
        '''
        data = self.raw_data
        pmids = data['PMID'].tolist()
        pmid_list = []
        for i in pmids:
            pmid_list.extend(i.split(','))

        print("Total number of PMIDs: {}".format(len(pmid_list)))
        print("Unique number of PMIDs: {}".format(len(set(pmid_list))))

        self._most_common = Counter(pmid_list).most_common()[:10]
        self._most_common_ids = [i[0] for i in self._most_common]
        print("most common ids ")
        print(self._most_common_ids)

        most_common_dict = {}
        for i in self._most_common:
            key = i[0]
            val = i[1]
            most_common_dict[key] = val
        self.most_common_dict = most_common_dict
        pmids = data['PMID'].tolist()
        pmid_list = []
        nums = []
        for i in pmids:
            nums.append(len(i))
            pmid_list.extend(i.split(',')[:10])
        data['num_results'] = nums
        self.data_pmid = data
        return self
    
    def count_sort_algorithm(self):
        '''
        Summary of statistics
        '''
        data=self.data_pmid
        print(f"Median number of search results: {data['num_results'].median()}")
        plt.hist(data['num_results'])
        plt.title("Number of results (all searches)");
        data['sort_algorithm'].value_counts().to_dict()
        self.data_count_sort = data
        return self
    
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
        :return: .pmid_score1_info, dictionary with the key being the PMID and the value being the average index.

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
        pmid_score1_info = pmid_score1_info
        
        return pmid_score1_info

    def request_pmids(ids):
        '''
        getting metadata for 10 most common
        '''
        list_ids = ','.join(ids)
        url = "https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={}".format(list_ids)
        r = requests.get(url)
     
        return json.dumps(xmltodict.parse(r.text))
    
    def get_pubmed_data(self):
        self.pubmed_metadata = pubmed_bias2.request_pmids(self._most_common_ids)
        return self
    
    def get_abstract(record):
    
        abstract = ''
        hasStructuredAbstract=False
        try: 
            if record['MedlineCitation']['Article']['Abstract']:
                if record['MedlineCitation']['Article']['Abstract']['AbstractText']:
                    abstract = record['MedlineCitation']['Article']['Abstract']['AbstractText']
                    if type(abstract)==dict:
                        try:
                            abstract = abstract['#text']
                        except:
                            pass
                    elif type(abstract)==list:
                        hasStructuredAbstract=True

        except Exception as e:
            pass

        if abstract == '':
            print("Did not retrieve an abstract")

        return abstract, hasStructuredAbstract

    def get_pubtype(record):
        pubs = []
        try:
            if record['MedlineCitation']['Article']['PublicationTypeList']['PublicationType']:
                if type(record['MedlineCitation']['Article']['PublicationTypeList']['PublicationType'])==list:
                    for i in record['MedlineCitation']['Article']['PublicationTypeList']['PublicationType']:
                        pubs.append(i['#text'])
                else:
                    pubs.append(record['MedlineCitation']['Article']['PublicationTypeList']['PublicationType']['#text'])
        except Exception as e:
            print("** Error retrieving pubtype")
            print(e)

        return pubs

    def get_title(record):
        try:
            return record['MedlineCitation']['Article']['ArticleTitle']['#text']
        except Exception as e:
            return record['MedlineCitation']['Article']['ArticleTitle']
        
    def extract_xml(jsonString):
        parsed = []
        res = json.loads(jsonString)['PubmedArticleSet']['PubmedArticle']
        for i in res:   
            pmid = int(i['MedlineCitation']['PMID']['#text'])
            print(f"\nExtracting {pmid}")
            try:
                abstract, hasStructuredAbstract = pubmed_bias2.get_abstract(i)
                hasAbstract = bool(abstract)
                record = {
                    "pmid": pmid,
                    "journal": i['MedlineCitation']['Article']['Journal']['Title'],
                    "title": pubmed_bias2.get_title(i),
                    "abstract": abstract,
                    "hasAbstract": hasAbstract,
                    "hasStructuredAbstract": hasStructuredAbstract,
                    "pubtype": pubmed_bias2.get_pubtype(i)
                }
                parsed.append(record)
            except Exception as e:
                print("** Error extracting XML")
                print(e)

        return parsed
    
    def parse_save(self):
        
        pubmed_bias2.get_pubmed_data(self)    
        parsed = pubmed_bias2.extract_xml(self.pubmed_metadata)

        plist = []
        for i in parsed:
            r = {
                "pmid": i['pmid'],
                "title": i['title'],
                "journal": i['journal'],
                "pubtype": i['pubtype'],
                "hasAbstract": i['hasAbstract'],
                "hasStructuredAbstract": i['hasStructuredAbstract'],
                "appears_in_results": self.most_common_dict[str(i['pmid'])]
            }
            plist.append(r)

        self.parsed_data = pd.DataFrame(plist)
        
    def one_hot_pubtype(self):
        '''
        One-hot encode the pubtype for feature creation.
        INPUT: df = a pandas dataframe that includes the column 'pubtype' in which each cell contains a list of pubtypes.
        OUTPUT: .data_one_hot = a dataframe with the additional columns that are one-hot encoded and begin with the prefix 'pubtype_'
        '''
        df = self.parsed_data
        #change from column of lists to string
        df['pubtype'] = df['pubtype'].apply(', '.join).astype(str)
        # replace commas with a double underscore
        df['pubtype'] = df['pubtype'].apply(lambda x: x.replace(', ','__'))
        #replace spaces with single underscore
        df['pubtype'] = df['pubtype'].apply(lambda x: x.replace(' ','_'))
        #create dummies and join to the original data frame with new features prepended with 'pubtype'
        df = df.join(pd.get_dummies(df.pubtype, prefix='pubtype'))
        df.drop(columns=['pubtype'],inplace=True)
        self.data_one_hot = df
        return self
    
    def save_pubmed(self):
        self.data_one_hot.to_csv(self.output_path + self.filename + ".csv")
        self.data_one_hot.to_pickle(self.output_path + self.filename + '.pkl')
        
    def run_pipeline(self):
        '''
        Run the full pipeline for analyzing bias from team 2
        '''
        print("load data")
        pubmed_bias2.load_data(self)
        print("get PMIDS")
        pubmed_bias2.get_pmids(self)
        pubmed_bias2.count_sort_algorithm(self)
        pubmed_bias2.parse_save(self)
        print("one-hot encode pubtypes")
        pubmed_bias2.one_hot_pubtype(self)
        print("save to csv and pkl")
        pubmed_bias2.save_pubmed(self)
        return self
    
#if __name__ == '__main__':
  #  main()       
    
        
        

