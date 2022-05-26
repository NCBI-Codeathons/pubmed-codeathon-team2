# +


outfile = open("/data/team2/click_data1.tsv", "w")
pmids_with_click = {}
def _create_dict(algorithm):
    for each in click_data_values:
        elm = each.split(",")
        if elm[0] not in pmids_with_click:
            pmids_with_click[elm[0]] = {}
        if algorithm not in pmids_with_click[elm[0]]:
            pmids_with_click[elm[0]][algorithm] = 1
        else:
            pmids_with_click[elm[0]][algorithm] = pmids_with_click[elm[0]][algorithm] + 1

with open("/data/pubmed-data.tsv") as tsv:
    for line in tsv:
        line = line.rstrip()
        if line.startswith("search_id"):continue
        cols = line.split("\t")
        #column 7 has PMIDs and column 8 has click_data
        pmid = cols[6]
        click_data = cols[7]
        sort_alg = cols[3]

        if click_data != "NoClicks":
            click_data_values = click_data.split("*result_click,")
            click_data_values.pop(0)
            if sort_alg == "date":
                _create_dict("date")
            elif sort_alg == "relevance":
                _create_dict("relevance")
outfile.write("PMID\tdate\trelevance\n")
for pid, alg_counts in pmids_with_click.items():
    date_count = 0
    relevance_count = 0
    if "date" in alg_counts:
        date_count = alg_counts["date"]
    if "relevance" in alg_counts:
        relevance_count = alg_counts["relevance"]
    stext = str(pid)+"\t"+str(date_count)+"\t"+str(relevance_count)+"\n"
    outfile.write(stext)
print("Done")
# -
stext

# +
import pandas as pd

df = pd.read_csv('/data/team2/click_data.tsv', sep='\t')
df
# -


fpath = '/data/pubmed-data.tsv'
data = pd.read_csv(fpath, sep='\t')

# +
cancer_df = pd.read_csv('/data/team2/top10data/cancer.csv')
cancer_df['PMID'] = cancer_df['PMID'].apply(lambda x: x.split(','))
exploded_df = cancer_df.explode('PMID')
exploded_df = exploded_df.drop_duplicates('PMID')


top_10_query_PMIDs = pd.read_csv('/data/team2/top_10_query_PMIDs_v2.csv').drop('Unnamed: 0', axis=1)
top_10_query_PMIDs['PMID'] = top_10_query_PMIDs['pmid'].astype(str)

# adding hasAbstract, hasStructuredAbstract, pubtype
merged_df = exploded_df.merge(top_10_query_PMIDs, how='left', on = 'PMID')

# adding one-hot encoded publication types
merged_df1 = merged_df.join(pd.get_dummies(merged_df.pubtype, prefix='pubtype'))
# -

len(data)

 dff = data.merge(df, on=)
