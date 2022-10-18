# S2AParser
A small script to fetch a list of publication from semanticscholar

## Dependencies:

[SemanticScholar](https://pypi.org/project/semanticscholar/)  
[Pandas](https://pypi.org/project/pandas/)  
[Requests](https://pypi.org/project/requests/)  



## usage
python3 S2AParser.py [-h] [-i, INPUT] [-o, OUTPUT]
             [-sy, Start Year] Default = Last Year
             [-ey, End Year] Default = This Year



## Template
Any csv file that includes these columns: Name, author_id. 

Author_id column for members who don't have a S2A id must be blank.

## The software outputs two files. 
	1- csv file as output
	2- csv file as report 

Currently, the script is using doi number for getting bibliography. so it can't get data for publications without doi.

## Attention
Output list may include articles that don't belong to the author due to S2A errors. It is recommended to check manually.
