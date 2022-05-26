import os
from config import SampleQueries
from pubmed_preprocessing.pubmed import SampleSet

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