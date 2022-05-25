outfile = open("click_data.tsv", "w")
pmids_with_click = {}
with open("pubmed-data.tsv") as tsv:
    for line in tsv:
        line = line.rstrip()
        if line.startswith("search_id"):continue
        cols = line.split("\t")
        #column 7 has PMIDs and column 8 has click_data
        pmid = cols[6]
        click_data = cols[7]
        if click_data != "NoClicks":
            # *result_click,33395478,2022-03-16T20:51:46,1,False*result_click,24095074,2022-03-16T20:35:17,1,False
            click_data_values = click_data.split("*result_click,")
            click_data_values.pop(0)
            for each in click_data_values:
                elm = each.split(",")
                if elm[0] in pmids_with_click:
                    pmids_with_click[elm[0]] = pmids_with_click[elm[0]]+1
                else:
                    pmids_with_click[elm[0]] = 1
sorted_cd = sorted(pmids_with_click.items(), key=lambda item: item[1], reverse=True)
sorted_dict = {k: v for k, v in sorted_cd}
for key1 in sorted_dict:
    outfile.write(str(key1)+"\t"+str(sorted_dict[key1])+"\n")
