def get_click_data(self):
        outfile = open(self.output_path + "click_data1.tsv", "w")
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

        with open(self.input_path + self.input_file) as tsv:
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
