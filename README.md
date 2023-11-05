# S2AParser
A small script to fetch a list of publications from Semantic Scholar

## Dependencies:

[Pandas](https://pypi.org/project/pandas/)  
[Requests](https://pypi.org/project/requests/)  



## usage
usage: S2A_json_parser.py [-h] [-i INPUT] [-o OUTPUT] [--yearS Start Year, default = Last Year] [--yearE End Year, default = This Year] [-v].

optional arguments:.
  -h, --help            show this help message and exit.

  -i INPUT, --input INPUT.
                          Input Path
  -o OUTPUT, --output OUTPUT
                        Output Path
  --yearS Start Year, default = Last Year
                        Specify start year
  --yearE End Year, default = This Year
                        Specify end year
  -v, --verbose         Turn on verbose output
 



## Template
Any csv file that includes these columns: Name, author_id. 

Remove members without author_id. 

## Attention
Output list may include articles that don't belong to the author due to S2A errors. It is recommended to check manually.
