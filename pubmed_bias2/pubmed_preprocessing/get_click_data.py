# +

def get_click_data(input_path, input_file, output_path, click_data_filename):
    '''
    Inputs
    :input_path: str, 
    :input_file: str,
    :output_path: str,
    
    Output
    Writes a tab-separated value (tsv) file named "click_data1.tsv" to the specified output path.
    This file contains information on PMIDs that have been clicked by users per query and per sort type
    (Best Match and reverse chronological).
    This file is structured as follows
    <PMID>    <Processed Query>    <# of Clicks for Reverse Chronological Sorting>    <# of Clicks for Best Match>
    '''
    outfile = open(output_path + click_data_filename + ".tsv", "w")
    pmids_with_click = {}
        
    def _create_dict(algorithm):
        for each in click_data_values:
            elm = each.split(",")
            elm[0] = elm[0] + '/' + processed_query
            if elm[0] not in pmids_with_click:
                pmids_with_click[elm[0]] = {}
            if algorithm not in pmids_with_click[elm[0]]:
                pmids_with_click[elm[0]][algorithm] = 1
            else:
                pmids_with_click[elm[0]][algorithm] = pmids_with_click[elm[0]][algorithm] + 1

    with open(input_path + input_file) as tsv:
        for line in tsv:
            line = line.rstrip()
            if line.startswith("search_id"):continue
            cols = line.split("\t")
            #column 7 has PMIDs and column 8 has click_data
            pmid = cols[6]
            click_data = cols[7]
            sort_alg = cols[3]
            processed_query = cols[-1]


            if click_data != "NoClicks":
                click_data_values = click_data.split("*result_click,")
                click_data_values.pop(0)
                if sort_alg == "date":
                    _create_dict("date")
                elif sort_alg == "relevance":
                    _create_dict("relevance")
    outfile.write("PMID\tProcessedQuery\tdate\trelevance\n")

    for pid, alg_counts in pmids_with_click.items():
        date_count = 0
        relevance_count = 0
        if "date" in alg_counts:
            date_count = alg_counts["date"]
        if "relevance" in alg_counts:
            relevance_count = alg_counts["relevance"]
        spl = pid.split('/')
        stext = str(spl[0])+"\t"+str(spl[1])+"\t"+str(date_count)+"\t"+str(relevance_count)+"\n"
        outfile.write(stext)
# -


