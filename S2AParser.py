#!/usr/bin/env python3
import argparse
import pandas as pd
import json
import requests
import logging
from semanticscholar import SemanticScholar
from datetime import datetime

# Parts of this script was inspired from PHP CrossRef Client

startTime = datetime.now()
print("Please wait, fetching the data takes a while...")
# prerequisits: 1-semanticscholar,

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates a table containing a list of authors and pulications",
                                     formatter_class=argparse.HelpFormatter)
    parser.add_argument("-i", "--input", type=argparse.FileType(mode='r'), help="Input Path")
    parser.add_argument("-o", "--output", type=argparse.FileType('wb', 0), help="Output Path",
                        default='output.csv')
    parser.add_argument("-sy", "--yearS", type=int, help="Specify start year", metavar='Start Year, default = 2020',
                        default=2020)
    parser.add_argument("-ey", "--yearE", type=int, help="Specify end year", metavar='End Year, default = 2022',
                        default=2022)
    parser.add_argument("-t", "--timeout", type=int, help="Specify Timeout", default=30000)
    args = parser.parse_args()


class CrossRefClient(object):
    def __init__(self, accept='text/x-bibliography; style=apa', timeout=args.timeout):
        """
        # Defaults to APA biblio style

        # Usage:
        s = CrossRefClient()
        """
        self.headers = {'accept': accept}
        self.timeout = timeout

    def query(self, doi, q={}):
        if doi.startswith("http://"):
            url = doi
        else:
            url = "http://dx.doi.org/" + doi

        r = requests.get(url, headers=self.headers)
        return r

    def doi2apa(self, doi):
        self.headers['accept'] = 'text/x-bibliography; style=apa'
        return self.query(doi).text

    def doi2json(self, doi):
        self.headers['accept'] = 'application/vnd.citationstyles.csl+json'
        return self.query(doi).json()

author_list = pd.read_csv(args.input)
author_id = author_list['author_id']

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="report.csv", filemode="w+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")

# make an empty list for later, and loop through author ids and find their papers (after 2020)
table = []
for id in author_id:
    sch = SemanticScholar(timeout=1800000)
    author = sch.author(id)
    author_paper = (author['papers'])
    author_name = (author['name'])
    df_papers = pd.DataFrame().append(author_paper, ignore_index=True)
    year_paper = df_papers[((df_papers['year'] >= args.yearS) & (df_papers['year'] <= args.yearE))]

    paper_id = (year_paper['paperId'])

    # first write authors name and then loop through their papers
    # then wirte table which is a extracted list of authour name and publication details from dictionarey.

    for pid in paper_id:
        paper_dic = sch.paper(pid)
        keys = ['title', 'doi', 'year', 'venue']
        # authors_list = [d['name'] for d in mt.collapse(paper_dic.get("authors"), base_type=dict)]
        data = [paper_dic.get(key) for key in keys]
        list_dic = [author_name, data[0], data[1], data[2], data[3]]
        # out = [author_name, [paper_dic.get(key) for key in keys],authors]
        table.append(list_dic)
        df_table = pd.DataFrame(table)

# get the doi number and generate apa format for bibliography


cite = []
for doi in df_table[2]:
    try:
        session = CrossRefClient()
        out = session.doi2json(doi)


        def names(ref):
            name = []
            for _item in ref['author']:
                given_in = _item['given'].split(' ')
                given = ''.join([_name[0] + '.' for _name in given_in])
                name.append(_item['family'] + ', ' + given + ', ')
            return ''.join(name[0:-1]) + 'and ' + name[-1][0:-2]


        authors = names(out)
        year = str(out['created']['date-parts'][0][0])
        title = out['title']
        journal_short = str(out['container-title'])
        # volume = str(out['volume'])
        # pages = str(out['article-number'])
        DOI = out['DOI']
        bib = [authors + ' ' + year + '. ' + title + '. ' + journal_short + '. ' + 'doi:/' + DOI]
        cite.append(bib[0])
        try_index = (len(cite) + 2)
    except (AttributeError, KeyError, json.decoder.JSONDecodeError, NameError) as e:
        # print('Check row', try_index, ' No DOI number was detected for this publication. Edit manually')
        logging.info(', Row %s has no doi number. Edit manually', try_index)
        cite.append('There is no DOI number for this publication. Edit manualy')
        # logging.basicConfig(filename="report.txt", level=logging.DEBUG)
        # logger.error('Check row', try_index ,' No DOI number was detected for this publication. Edit manually')

# Add bibliography to the dataframe and write as csv file:
df_table['Bibliography'] = cite
titles = ['Name', 'Title', 'DOI', 'Year', 'Journal', 'Bibliography']
df_table.to_csv(args.output, header=titles, sep=',', index=None, encoding='utf-8-sig')
# logger.info("this is info level")
no_doi = len(df_table[df_table[2].isnull()])

print(
    "Caution: This list may include articles that don't belong to the author due to S2A errors,"
    " It is recommended to check manually.")
print(no_doi,
      " records lacked doi number and the bibliography should be edited manually. Check report file for more... ")
print(try_index, ' records were extracted for this list of authors')
print('it took', datetime.now() - startTime, 'to fetch requested publications')
