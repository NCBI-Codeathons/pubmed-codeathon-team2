## Pubmed-codeathon-team2

## Table of Contents
- [Introduction](#Introduction)
- [Basic workflow](#Basic-workflow)
- [Final Dataset](#Final-Dataset)
- [Results](#Results)
- [Dependencies](#Dependencies)
- [Team](#Team)
- [Acknowledgment](#Acknowledgment)
- [License](#License)

## Introduction

We investigated possible bias/inconsistency in the results returned by Pubmed's "Best Match" search algorithm. We compared the distributions of selected article content/metadata features returned by high-frequency versus low-frequency health condition queries.

- **The PubMed database** contains more than 34 million citations and abstracts of biomedical literature. PubMed does not include full text journal articles; however, links to the full text are often available from other sources, such as the publisher's website or the PubMed Central (PMC) repository.

- **The Best Match Algorithm** analyzes each PubMed article citation returned for a search query. The calculated citation "weight" depends on how many search terms are found and in which fields. Recently-published articles get a somewhat higher weight. Then, the top articles returned by the weighted term frequency algorithm are re-ranked for better relevance by a machine-learning algorithm. Best Match is not designed for comprehensive or systematic searches. <a href="https://support.nlm.nih.gov/knowledgebase/article/KA-03719/en-us">See more information on Best Match</a>.

## Basic workflow

**1] Query Selection**
- To narrow our scope, we selected twenty health-related informational (as opposed to navigational) processed search queries from the provided PubMed log data sample. 
- The search queries met these criteria:
    * Each result received ≥ 1 user click
    * No interface filters applied by user
    * No PubMed field tag 
    * No number sign 
        * Ex: #1 AND #2
    * No orthographic variants 
        * Ex: covid 19; covid-19
    * No synonyms 
        * covid 19; covid
- Additionally, the top ten queries met the following criteria:
    * Run on ≥ 7 unique dates
    * Associated with ≥ 38 user ids
- While the bottom ten queries met the following criteria:
    * Had exactly two occurrences
    * Associated with ≥ 2 user IDs
    * Returned ≥ 100 results on average across different sample dates

**2] Retrieval of Article Features (using the PubMed beta API - May 2022)**
- Following feature were extracted for each article:
    * `Abstract type` 
        * Unstructured
        * Structured
        * No abstract
    * `Full-text availability` 
        * Proxy for paywalled articles
    * `Publication type(s)` 
        * Ex: Clinical trial, Review, etc
    * `Sort type` 
        * Best match vs Reverse chronological date
    * `Article Title`
    * `Journal` 
    * `Entrez Date`
- Additionally, the count of user clicks of each PMIDs displayed on the first page of search was extracted from the pubmed log file (for each algorithm)

**3] Creating distributions for the following 3 datasets:**
- Total results of the queries (retrieved live during the codeathon), 
- Articles the users click on (from the log sample), and 
- The top 10 results returned for the queries (from the log sample)

**4] Integration into a single pipeline**

**5] Performing a `Chi-squared test` to compare above distributions to the baseline distributions**
## Final Dataset
- The provided search history file contained approximately `7 million` unique PMIDs
- The ten most popular queries retrieved included:
    * breast cancer, alzheimer's disease, covid 19, cancer, lung cancer, obesity, multiple sclerosis, diabetes mellitus, gastric cancer, 
- The bottom ten queries (chosen from approximately 600 candidates) included:
    * allergies, cardiac ischemia, neurodegenerative disease, depression in older adults, adverse drug reactions, neuroinflammation, vasculitis, hypoxia, acute kidney injury, pulmonary embolism
- For each algorithm, we retieved and analyzed first 100 results 

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
## Acknowledgment
- We would like to thank the `NIH National Library of Medicine/National Center for Biotechnology Information` for providing all the required computational resources during the codeathon.

## License
Licensed under MIT License - Copyright (c) 2022 NCBI-Codeathons (Refer LICENSE file for more details)
