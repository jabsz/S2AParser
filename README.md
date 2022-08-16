# S2AParser
A small script to fetch a list of publication from semanticscholar

usage: S2AParser.py [-h] [-i INPUT] [-o OUTPUT]
                    [-sy Start Year, default = 2020]
                    [-ey End Year, default = 2022] [-t TIMEOUT]



Template: Any csv file that includes these columns: Name, author_id. 

author_id column for members who don't have a S2A id must be blank.

The software outputs two files. 
		1- csv file as output
		2- csv file as report 

Currently, the script is using doi number for getting bibliography column. so it can't get data for publications without doi.
 
