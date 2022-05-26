## Pubmed-codeathon-team2

## Table of Contents
- [Introduction](#Introduction)
- [Basic workflow](#Basic-workflow)
- [Example Usage](#Example-Usage)
- [Results](#Results)
- [Dependencies](#Dependencies)
- [Team](#Team)
- [License](#License)

## Introduction

We investigated possible bias/inconsistency in the results returned by Pubmed's "Best Match" search algorithm. We compared the distributions of selected article content/metadata features for the articles returned by high-frequency versus low-frequency health condition queries.

- **The PubMed database** contains more than 34 million citations and abstracts of biomedical literature. PubMed does not include full text journal articles; however, links to the full text are often available from other sources, such as the publisher's website or the PubMed Central (PMC) repository.

- **The Best Match Algorithm** analyzes each PubMed article citation returned for a search query. The calculated citation "weight" depends on how many search terms are found and in which fields. Recently-published articles get a somewhat higher weight. Then, the top articles returned by the weighted term frequency algorithm are re-ranked for better relevance by a machine-learning algorithm. Best Match is not designed for comprehensive or systematic searches. <a href="https://support.nlm.nih.gov/knowledgebase/article/KA-03719/en-us">See more information on Best Match</a>.

## Basic workflow

1] Create datasets to understand the distribution of PubMed search results with regard to:
* Abstract type (unstructured, structured, none), 
* Full-text availability (proxy for paywalled articles), and 
* Publication type(s) (Ex: Clinical trial, Review, etc)

2] To narrow the scope, we restrict our focus to 10 most popular/10 least popular informational health condition queries in the provided dataset
* Top 10 queries: breast cancer, alzheimer's disease, covid 19, cancer, lung cancer, obesity, multiple sclerosis, diabetes mellitus, gastric cancer, ferroptosis
* Bottom 10 queries: allergies, cardiac ischemia, neurodegenerative disease, depression in older adults, adverse drug reactions, neuroinflammation, vasculitis, hypoxia, acute kidney injury, pulmonary embolism

3] Create these distributions for each of the three following citation sets: 
* Total results of the queries (retrieved live during the codeathon), 
* Articles the users click on (from the log sample), and 
* The first page results = the top 10 results returned for the queries (from the log sample)

4] Compare the results and make observations

5] If there is a bias, investigate it using the entire dataset

## Dependencies
- Python version >= 3
- Required modules:
    * pandas 
    * numpy
    * xmltodict
    * requests
    * matplotlib
    * sklearn
- You can easily install these with pip (Ex: pip install pandas)
- Most other standard core modules should already be available on your system

## Team 
- Avena Cheng
- Kate Dowdy
- Leo Meister
- Lydia Jones
- Manoj M Wagle
- Melanie Huston
- Savita Shrivastava
- Summer Rankin

## License
Licensed under MIT License - Copyright (c) 2022 NCBI-Codeathons (Refer LICENSE file for more details)

## Import & Save
To import the data in jupyter hub see the notebook [import_save.ipynb](import_save.ipynb)

## Preprocess
[retrieving-PMID-data.ipynb](retrieving-PMID-data.ipynb)

### One-hot encode pubtype
[one-hot-encode.ipynb](one-hot-encode.ipynb)

