# pubmed-codeathon-team2

Current Objective:

Evaluate possible bias or inconsistency in the text availability or publication types of articles retrieved for PubMed “best match” searches

Method:

Create datasets to understand the distribution of PubMed search results with regard to
- abstract type (unstructured, structured, none), 
- full-text availability (proxy for paywalled articles), and 
- publication type(s) (assigned via publisher or indexing process)

We will create these distributions for each of the three following citation sets: 
- total results of the queries (retrieved live during the codeathon), 
- articles the users click on (from the log sample), and 
- top 10 results turned for the queries (from the log sample)

To narrow the scope, we will begin by taking the top 10 most common queries and 10 least common queries in the provided dataset. Additionally, we will look at results from best match and reverse-chronological searches only (sort_algorithm column). 

