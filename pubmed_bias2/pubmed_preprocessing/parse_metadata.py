import requests
import xmltodict
import json
import pandas as pd


def request_pmids(ids):
        '''
        getting metadata for 10 most common
        '''
        list_ids = ','.join(ids)
        url = "https://eutilspreview.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={}".format(list_ids)
        r = requests.get(url)
     
        return json.dumps(xmltodict.parse(r.text))

def get_pubmed_data(self):
        self.pubmed_metadata = request_pmids(self._most_common_ids)
        return self

def extract_xml(jsonString):
        parsed = []
        res = json.loads(jsonString)['PubmedArticleSet']['PubmedArticle']
        for i in res:   
            pmid = int(i['MedlineCitation']['PMID']['#text'])
            print(f"\nExtracting {pmid}")
            try:
                abstract, hasStructuredAbstract = get_abstract(i)
                hasAbstract = bool(abstract)
                record = {
                    "pmid": pmid,
                    "journal": i['MedlineCitation']['Article']['Journal']['Title'],
                    "title": get_title(i),
                    "abstract": abstract,
                    "hasAbstract": hasAbstract,
                    "hasStructuredAbstract": hasStructuredAbstract,
                    "pubtype": get_pubtype(i)
                }
                parsed.append(record)
            except Exception as e:
                print("** Error extracting XML")
                print(e)

        return parsed

# +
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


# -

def parse_save(self):
        
    get_pubmed_data(self)    
    parsed = extract_xml(self.pubmed_metadata)

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

    return pd.DataFrame(plist)
