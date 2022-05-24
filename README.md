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

- **What is Pubmed?**

- **The Best Match Algorithm**

## Basic workflow

1] Investigate possible bias/inconsistency in the results returned by Pubmed's `Best Match algorithm` based on features of the article content/metadata

2] Create datasets to understand the distribution of PubMed search results with regard to:
* Abstract type (unstructured, structured, none), 
* Full-text availability (proxy for paywalled articles), and 
* Publication type(s) (Ex: Clinical trial, Review, etc)

3] We will create these distributions for each of the three following citation sets: 
* Total results of the queries (retrieved live during the codeathon), 
* Articles the users click on (from the log sample), and 
* Top 10 results retturned for the queries (from the log sample)

4] To narrow the scope, we will begin by taking the 10 most popular/10 least popular queries in the provided dataset

5] Compare the results and make observations

6] If there is a bias, investigate it using the entire dataset

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
