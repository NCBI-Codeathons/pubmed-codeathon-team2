from sqlite3 import DateFromTicks
import requests
import xmltodict
import json
import time
import pandas as pd
from features import *

def make_pmid_query(ids):
    list_ids = ','.join(ids)
    return "https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={}".format(list_ids)

def make_freetext_query(query, sort_type):
    #parsed = '+AND+'.join(query.split(' '))
    return "https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}+AND+ffrft[Filter]&sort={}&retmax=10000".format(query, sort_type)
    
def make_regular_query(query, sort_type):
    #arsed = '+AND+'.join(query.split(' '))
    return "https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={}&sort={}&retmax=10000".format(query, sort_type)

def request_api(url):
    count = 0
    while count < 15:
        r = requests.get(url)
        if r.status_code == 200:
            break
        else:
            time.sleep(1)
            count += 1
    
    return r.text

## Getting Query results from Pubmed

def get_pmids_by_query(query, sort_type):
   
    try:
        filt_url = make_freetext_query(query, sort_type)
        r = request_api(filt_url)
        filt_pmids = xmltodict.parse(r.text)['eSearchResult']['IdList']['Id']

        reg_url = make_regular_query(query, sort_type)
        r = request_api(reg_url)
        reg_pmids = xmltodict.parse(r.text)['eSearchResult']['IdList']['Id']

        overlap = set(reg_pmids).intersection(filt_pmids)
    
        pmid_dict = {}
        for i in reg_pmids:
            if i in overlap:
                pmid_dict[i] = 'fulltext_available'
            else:
                pmid_dict[i] = "fulltext_unavailable"
        
        return pmid_dict
    
    except Exception as e:
        print(e)
        return {}

def collect_query_results(queries):
    rel_sort = {}
    for i in queries:
        rel_dict = get_pmids_by_query(query=i, sort_type='relevance')
        date_dict = get_pmids_by_query(query=i, sort_type='date_desc')
        rel_sort[i] = {
            "relevance": rel_dict,
            "date_desc": date_dict
        }
    return rel_sort

def make_results_df(mydict, query_type):
    df = pd.DataFrame(mydict).T
    df['relevance_res'] = df['relevance'].apply(lambda x: list(x.keys()))
    df['date_desc_res'] = df['date_desc'].apply(lambda x: list(x.keys()))
    df = df[['relevance_res', 'date_desc_res']]
    df['query_type'] = query_type

    return df

def combine_top_bottom(top, bottom):

    my_pmid_status = {}
    top_results = collect_query_results(top)
    for i in top_results.keys():
        my_pmid_status.update(top_results[i]['relevance'])
        my_pmid_status.update(top_results[i]['date_desc'])

    top_df = make_results_df(top_results)

    bottom_results = collect_query_results(bottom)
    for i in bottom_results.keys():
        my_pmid_status.update(bottom_results[i]['relevance'])
        my_pmid_status.update(bottom_results[i]['date_desc'])

    bottom_df = make_results_df(bottom_results)
    
    results_df = pd.concat([top_df, bottom_df])
    fulltext_df = pd.DataFrame.from_dict(my_pmid_status, orient='index')
    
    return results_df, fulltext_df

## Getting PMID metadata from Pubmed
    
def extract_xml(text):
    parsed = []
    jsonString = json.dumps(xmltodict.parse(text))
    res = json.loads(jsonString)['PubmedArticleSet']['PubmedArticle']
    for i in res:   
        pmid = int(i['MedlineCitation']['PMID']['#text'])
        print(f"\nExtracting {pmid}")
        try:
            abstract, hasStructuredAbstract = get_abstract(i)
            hasAbstract = bool(abstract)
            articleDate = get_articleDate(i)
            date = parse_date(articleDate)
            pubdate = get_pubdate(i)
            record = {
                "pmid": pmid,
                "journal": i['MedlineCitation']['Article']['Journal']['Title'],
                "title": get_title(i),
                "abstract": abstract,
                "hasAbstract": hasAbstract,
                "hasStructuredAbstract": hasStructuredAbstract,
                "articleDate": date,
                "journalPubDate": pubdate,
                "entrezDate": get_entrez_date(i),
                "pubtype": get_pubtype(i)
            }
            parsed.append(record)
        except Exception as e:
            print("** Error extracting XML")
            print(e)
    
    return parsed

def wrapper(ids):
    
    set_range = len(ids) // 10 + 1
    start = 0
    all_parsed = []
    for i in range(set_range):
        print(i)
        try:
            stop = start + 10
            chunk = ids[start:stop]
            url = make_pmid_query(chunk)
            resp = request_api(url)
            parsed = extract_xml(resp)
            all_parsed.extend(parsed)
            start += 10
            time.sleep(0.35)
        except Exception as e:
            print(e)

    df = pd.DataFrame(all_parsed)
    return df