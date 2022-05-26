import os
from config import SampleQueries
from pubmed_preprocessing.query_api import *

QUERIES = SampleQueries.BOTTOM_10_QUERIES + SampleQueries.TOP_10_QUERIES

def check_filepath(path, fname, ext):
    '''Check if filepath is available before saving, otherwise make new version'''
    
    fullpath = os.path.join(path, fname + ext)
    if os.path.exists(fullpath):
        print("This path already exists, making a new version")
        for x in range(50):
            version = '_v' + str(x)
            fullpath = os.path.join(path, fname + version + ext)
            if os.path.exists(fullpath):
                continue
            else:
                break
    
    if os.path.exists(fullpath):
        print("Need a new filepath name")
    else:
        print(f"Available filepath: {fullpath}")
    
    return fullpath

class SampleSet():

    def __init__(self, queries, testing_only):

        self.testing_only = testing_only
        self.queries = queries
        self.results, self.fulltext_status = organize_query_results(queries)
        self.pmids = self.gather_pmids()
        self.pmid_metadata = self.retrieve_metadata()
        
    def gather_pmids(self):
        pmids = []
        res = self.results['relevance_res'].tolist() + self.results['date_desc_res'].tolist()
        for i in res:
            if type(i) == str:
                list_ids = i.lstrip('[').strip(']').split(', ')
                ids = [i.lstrip("'").strip("'") for i in list_ids] 
            elif type(i) == list:
                ids = i
            pmids.extend(ids)
        
        return pmids
    
    def retrieve_metadata(self):
        
        if self.testing_only:
            set_range = 2
        else:
            set_range = len(self.pmids) // 10 + 1
        start = 0
        all_parsed = []
        for i in range(set_range):
            print(f"{i} / {set_range}")
            try:
                stop = start + 10
                chunk = self.pmids[start:stop]
                url = make_pmid_query(chunk)
                resp = request_api(url)
                parsed = extract_xml(resp)
                all_parsed.extend(parsed)
                start += 10
                time.sleep(0.35)
            except Exception as e:
                print(e)

        df = pd.DataFrame(all_parsed)

        try:
            df['fulltext_status'] = df['pmid'].astype(str).map(self.fulltext_status)
        except Exception as e:
            print(e)
        
        return df
    
if __name__ == "__main__":

    testing_only = False
    queries = QUERIES
    if testing_only:
        queries = queries[:2]
    print(f"Starting pipeline (testing only set to {testing_only}) using queries: {queries}")
    samples = SampleSet(queries, testing_only)
    results = samples.results
    metadata = samples.pmid_metadata
    if not testing_only:
        meta_save_path = check_filepath(path='data/team2', fname='pmid_metadata', ext='.pkl')
        metadata.to_pickle(meta_save_path)
        print("Saved PMID metadata")
        results_save_path = check_filepath(path='data/team2', fname='query_results', ext='.csv')
        results.to_csv(results_save_path)
        print("Saved query results")
    else:
        print(metadata.head())
        print(f"Shape of metadata: {metadata.shape}")