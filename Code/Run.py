import urllib.request
import concurrent.futures
from bs4 import BeautifulSoup
from Code import Find
import requests
from Code import SimpleCSV
from requests import Session

def loadUrl(url):
    html = urllib.request.urlopen(url)
    return html

def loadUrlSession(session, url):
    html = session.get(url)
    return html
            
##main process of the metadata scrapper with login session
# @param    session
#           a session which contain login cookie
# @param    urlList
#           a list contain item url
# @param    outputFile
#           a CSV file for output
def runProcessParallelLogin(session, urlList, outputFile):
    categoryValue = []
    listOfFile = []
    # iterator to show program progress
    i = 1
    ## TODO: finish find file url/find next page url
    numOfUrl = len(urlList)
    print("There are ", numOfUrl, " records in the input file.\n")
    print("Proceeding......\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
        future_to_url = {executor.submit(loadUrlSession, session, url): url for url in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            print("Processing ",i, " / ", numOfUrl, "records.")
            try:
                # original url link
                url = future_to_url[future]
                # opened url
                html = future.result()
                # load target digital collection in html parser
                soup = BeautifulSoup(html.text, 'html.parser')
                # find attributes value
                listOfFile = findFilePage(soup)
                getValue(categoryValue, session, listOfFile)
                generateOutput(categoryValue, outputFile)
                print("Write into CSV successful.")
                categoryValue = []
                nextPageSoup = findNextPage(soup, session)
                while nextPageSoup != None:
                    listOfFile = findFilePage(nextPageSoup)
                    if listOfFile != None:
                        getValue(categoryValue, listOfFile)
                        generateOutput(categoryValue, outputFile)
                        print("Write into CSV successful.")
                    else:
                        print("No related file under this url.")
                    listOfFile = []
                    categoryValue = []
                    nextPageSoup = findNextPage(soup, session)
            except:
                print("Some error happened. Please run it again in case of unstable network.")
                print("If this kind of error keep happening, save the error message and send to author.")
                print("Press enter to exit. ", end = '')
                input()
            listOfFile = []
            categoryValue = []
            print("All pages processed. No more next page.")
            print("Successfully web-scraped ", i, " / ", numOfUrl, "records.\n")
            i = i + 1

## call functions to get value for each cell in header
# @param    resultList
#           a list to store results
# @param    session
#           login cookie to access private file record
# @param    fileUrlList
#           a list of url fot related files
# @update   resultList
def getValue(resultList, session, fileUrlList):
    fileResult = []
    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
        future_to_url = {executor.submit(loadUrlSession, session, url): url for url in fileUrlList}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            # opened url
            html = future.result()
            # load target digital collection in html parser
            soup = BeautifulSoup(html.text, 'html.parser')
            fileResult.append(Find.findFileID(soup))
            fileResult.append(Find.findWorkID(soup))
            fileResult.append(Find.findFileName(soup))
            fileResult.append(Find.findDepositor(soup))
            fileResult.append(Find.findDateUploaded(soup))
            fileResult.append(Find.findDateModified(soup))
            fileResult.append(Find.findFixity(soup))
            fileResult.append(Find.findCharacterization(soup))
            resultList.append(fileResult)
            fileResult = []
    
## add master file name into list and write data into csv file
# @param    rows
#           Expected data by row
# @param    output
#           Output csv file, opened
def generateOutput(rows, output):
    #print(rows)
    for row in rows:
        SimpleCSV.writeCSV(row, output)

## find url lik that points to relative file
# @param    source
#           parsed html of master file(or previous page if there is multiple nextpage)
# @return   fileUrlList
#           a list of related file url
#           Otherwise, return None
def findFilePage(source):
    fileUrlList = []
    hrefList = []
    nextPage = ""
    urlPrefix = "https://library.osu.edu"
    result = source.find_all('td', attrs={'class': 'attribute attribute-filename ensure-wrapped'})
    for td in result:
        url = td.a['href']
        hrefList.append(url)
    if (hrefList != []):
        for href in hrefList:
            fileUrl = urlPrefix + href
            fileUrlList.append(fileUrl)
        print("Page of file has been found, processing...")
        return fileUrlList
    else:
        return None

## if items are more than 9, it will continue in next page.
## find the next page and return the parsed html of next page
# @param    source
#           parsed html of master file(or previous page if there is multiple nextpage)
# @param    session
#           A web cookie object which include login info in order to get private record.
# @return   nextPageSoup
#           if there is a next page, return a parsed html of next page
#           Otherwise, return None
def findNextPage(source, session):
    nextPage = ""
    urlPrefix = "https://library.osu.edu/"
    result = source.find('a', attrs={'rel': 'next'})
    #print(result)
    if (result != None):
        nextPage = urlPrefix + result['href']
        print("Next page of files is founded, processing...")
        html = loadUrlSession(session, nextPage)
        nextPageSoup = BeautifulSoup(html.text, 'html.parser')
        return nextPageSoup
    else:
        return None
