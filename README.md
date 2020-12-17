# OSU-Library-DC-Related-File-Scaper
## What does it do
   For each generic work item, there will be several related items at the end. This program will find these related item and extract metadata from them. Metadata include "Work ID", "File ID", "Depositor", "Date Uploaded", "Date Modified", "Fixity Check",
"Characterization". The input file is required to be a CSV. The first row can be any kind of header. The CSV file will contain url for generic items. Each url should be put in to first colomn and follow the rule of one url per row. The output file will also be a CSV File. The first row will be the header for metadata. Start from second row it will be metadata for each related item One item per row.

## Prerequisites
   Run in Windows10 environment. 
   
   Must have admin level account in OSU library metadata department. 
   
   Python ver. 3.8 or higher, other version has not been tested. 
   
   Required Package: 
   
      MechanicalSoup 
      
      BeautifulSoup 
      
   If not installed, please type following command in CMD:
   
      pip install MechanicalSoup 
      
      pip install bs4  
      
## Instruction
1. put csv file which contain DC items' url in the same folder as DC item scrapper. 
2. run 'Related File Scraper v1.0.0.py'  
3. follow instructions on display  

## Change:
Fix the issue that when a record doesn't have related file it would cause unexpected exit of freeze.
