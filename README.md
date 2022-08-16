# S2AParser
A small script to fetch a list of publication from semanticscholar

## Dependencies:
[semanticscholar](https://pypi.org/project/semanticscholar/))

semanticscholar: https://pypi.org/project/semanticscholar/

## usage
S2AParser.py [-h] [-i INPUT] [-o OUTPUT]
                    [-sy Start Year, default = 2020]
                    [-ey End Year, default = 2022] [-t TIMEOUT]



## Template
Any csv file that includes these columns: Name, author_id. 

Author_id column for members who don't have a S2A id must be blank.

## The software outputs two files. 
		1- csv file as output
		2- csv file as report 

Currently, the script is using doi number for getting bibliography column. so it can't get data for publications without doi.

## Attention
Output list may include articles that don't belong to the author due to S2A errors. It is recommended to check manually.
