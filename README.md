## Pubmed-codeathon-team2

- [Introduction](#Introduction)
- [Basic workflow](#Basic-workflow)
- [Results](#Results)
- [Dependencies]((#Dependencies))
- [Team](#Team)
- [License](#License)

## Introduction

- **What is Pubmed?**

- **The Best Match Algorithm**

## Basic workflow

- Investigate possible bias/inconsistency in the results returned by Pubmed's `Best Match algorithm` based on features of the article content/metadata

    1] Create datasets to understand the distribution of PubMed search results with regard to:
    * Abstract type (unstructured, structured, none), 
    * Full-text availability (proxy for paywalled articles), and 
    * Publication type(s) (Ex: Clinical trial, Review, etc)

    2] We will create these distributions for each of the three following citation sets: 
    * Total results of the queries (retrieved live during the codeathon), 
    * Articles the users click on (from the log sample), and 
    * Top 10 results retturned for the queries (from the log sample)

    3] To narrow the scope, we will begin by taking the 10 most popular/10 least popular queries in the provided dataset.

## Team 
- Avena Cheng
- Kate Dowdy
- Leo Meister
- Lydia Jones
- Manoj M Wagle
- Melanie Huston
- Savita Shrivastava
- Summer Rankin
test
## License
Licensed under MIT License - Copyright (c) 2022 NCBI-Codeathons (Refer LICENSE file for more details)
