## DC Related File Scrapper v1.0.0
Author: Zhiren Xu  
Publish data: 8/5/20

Requirement:
	Run in Windows environment
	
	Required Package:
		MechanicalSoup
		BeautifulSoup
	If not installed, please type following command in CMD:
		pip install MechanicalSoup
		pip install bs4
		
	Input csv file should have first row as header, then with urls in following rows. The program will only read from first column.
	There is an example csv as templete.
	
	Output csv file will have "Work ID	Title	File Title	Date Uploaded	Visibility" as header, data will be written in rows below.

Instruction: 
	1. put csv file which contain DC items' url in the same folder as DC item scrapper. 
	3. run 'Related File Scraper v1.0.0.py'  
	4. follow instructions on display  
