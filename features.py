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

def get_entrez_date(record):
    entrez = ''
    try:
        dates = record['PubmedData']['History']['PubMedPubDate']
        if dates:
            for i in dates:
                if i['@PubStatus']=='entrez':
                    month = ('0' + i['Month'])[-2:]
                    date = ('0' + i['Day'])[-2:]
                    entrez = i['Year'] + '-' + month + '-' + date
                    
    except Exception as e:
        print(e)
    
    return entrez
    
def get_articleDate(record):
    try:
        return record['MedlineCitation']['Article']['ArticleDate']
    except Exception as e:
        print(e)
        return ''

def parse_date(date):
    try:
        return date['Year'] + '-' + date['Month'] + '-' + date['Day']
    except:
        return date

def get_pubdate(record):
    months = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    try:
        date = record['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
        parsed_date = date['Year'] + '-' + months[date['Month']] + '-' + date['Day']
        return parsed_date
    except Exception as e:
        return ''