#!/usr/bin/env python3

#####################
# Author: Jaber Abbaszadeh 
# Project: Annual report ERI University of Waikato 
# This script takes semantic scholar author IDs and
#   generates a list of publication for ERI annual report

import argparse
import pandas as pd
import requests
from datetime import datetime

startTime = datetime.now()
this_year = startTime.year
last_year = this_year - 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates a table containing a list of authors and publications",
                                     formatter_class=argparse.HelpFormatter)
    parser.add_argument("-i", "--input", type=argparse.FileType(mode='r'), help="Input Path")
    parser.add_argument("-o", "--output", type=argparse.FileType('wb', 0), help="Output Path",
                        default='output.csv')
    parser.add_argument("-sy", "--yearS", type=int, help="Specify start year",
                        metavar='Start Year, default = Last Year',
                        default=last_year)
    parser.add_argument("-ey", "--yearE", type=int, help="Specify end year", metavar='End Year, default = This Year',
                        default=this_year)
    parser.add_argument("-v", "--verbose", action="store_true", help="Turn on verbose output")
    args = parser.parse_args()

    if args.input is None:
        parser.print_help()
        exit(1)

print("Please wait, fetching the data takes a while... \nfor activating interactive parsing mode use -v option")

author_list = pd.read_csv(args.input)
author_ids = author_list['author_id']

def format_author_name(name):
    # Split the author name into words
    words = name.split()
    # Extract the last name
    last_name = words[-1]
    # Extract the initials of other names
    initials = " ".join(word[0].upper() + '.' for word in words[:-1])
    # Format the name as "Last Name, Initials"
    formatted_name = f"{last_name}, {initials}"
    return formatted_name

# Define the base URLs
base_url_author = "https://api.semanticscholar.org/graph/v1/author/{}"
base_url_paper = "https://api.semanticscholar.org/graph/v1/author/{}/papers?fields=url,title,venue,year,authors,externalIds"

# Define the author IDs (you can put multiple author IDs in a list)
author_id_to_name = dict(zip(author_list['author_id'], author_list['Name']))

table = []
for author_id in author_ids:
    # Create the URLs for the author and papers
    url_member = base_url_author.format(author_id)
    url_papers = base_url_paper.format(author_id)

    # Fetch data for the author and papers
    response_member = requests.get(url_member)
    response_paper = requests.get(url_papers)

    if response_member.status_code == 200 and response_paper.status_code == 200:
        json_member = response_member.json()
        json_paper = response_paper.json()

        # Accessing author information
        member = json_member['name']
        member_id = json_member['authorId']

        # Access paper data for the author
        data = json_paper['data']

        publications_added = False  # Flag to check if any publications were added for this author

        for paper in data:
            member = author_id_to_name.get(author_id, "Unknown Author")  # Get the author_name from the dictionary
            author_name= author_list['Name']
            title = paper['title']
            authors = paper['authors']
            author_names = [author['name'] for author in authors]
            journal = paper['venue']
            
            #Some records of Semantic scholar have null year, this makes sure that they dont interrupt the script
            try:
                year = int(paper['year'])
            except (ValueError, TypeError):
                # Skip this paper if the year is not a valid integer
                print(f"Skipping paper with invalid year, Author", member, "title:" ,title, )
                continue

            if args.verbose:
                print("getting data for  ", member, "with author ID ", member_id, "paper title:", title, "year", year)

            # Check if DOI is available
            if 'externalIds' in paper and 'DOI' in paper['externalIds']:
                doi = paper['externalIds']['DOI']
            else:
                doi = " "  # Replace with a space if DOI is not available
            # Filter papers by year (between 2021 and 2022)

            if (last_year <= year <= this_year) or (args.yearS <= year <= args.yearE):
                title = title.replace('\n', ' ').strip()
                # Create a list of formatted author names
                formatted_author_names = [format_author_name(author) for author in author_names]
                # Join the formatted author names into a single string
                author_names_str = ", ".join(formatted_author_names)
                # Print the information for each paper
                biblio = [author_names_str, year, title, journal, doi]
                biblio_frmt = [str(item).strip("[]''") for item in biblio]
                biblio_str = ". ".join(biblio_frmt)

                table.append((member, title, doi, year, journal, biblio_str))
                publications_added = True  # Publications were added

        if not publications_added:
            # If no publications were added for this author, add a row with "No publication"
            table.append((member, "No publication", "No publication", "No publication", "No publication", "No publication"))

    else:
        print(f"Failed to fetch data for author {author_id}")

titles = ['Name', 'Title', 'DOI', 'Year', 'Journal', 'Bibliography']
# df_table.to_csv(args.output, header=titles, sep=',', index=None)
df_table = pd.DataFrame(table)
df_table.to_csv(args.output, header=titles, sep=',', index=None, encoding='utf-8-sig')


print("\n Done... \n The list of ERI members and their publications for requested years is written as provided output table name or output.csv (default). \n Thanks  \n")

# Print the names of authors with no publications
no_publication_authors = [row[0] for row in table if row[1] == "No publication"]
print("Authors with no publications in the specified years:", no_publication_authors)

