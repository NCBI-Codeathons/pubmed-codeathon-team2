#!/usr/bin/env python3

import pandas as pd
from collections import Counter



def get_pmids(data):
        '''
        explode the pmid information and add to data frame.
        INPUT: pandas dataframe with a 'PMID' column.
        OUTPUT: data with an added column of the number of PMIDS
        '''
        
        pmids = data['PMID'].tolist()
        pmid_list = []
        for i in pmids:
            pmid_list.extend(i.split(','))

        print("Total number of PMIDs: {}".format(len(pmid_list)))
        print("Unique number of PMIDs: {}".format(len(set(pmid_list))))

        _most_common = Counter(pmid_list).most_common()[:10]
        _most_common_ids = [i[0] for i in _most_common]
        print("most common ids ")
        print(_most_common_ids)

        most_common_dict = {}
        for i in _most_common:
            key = i[0]
            val = i[1]
            most_common_dict[key] = val
        most_common_dict = most_common_dict
        pmids = data['PMID'].tolist()
        pmid_list = []
        nums = []
        for i in pmids:
            nums.append(len(i))
            pmid_list.extend(i.split(',')[:10])
        data['num_results'] = nums
        return data, _most_common, _most_common_ids, most_common_dict
