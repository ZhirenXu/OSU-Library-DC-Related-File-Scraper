import urllib.request
import concurrent.futures
from bs4 import BeautifulSoup
from Code import Find
import requests
from Code import SimpleCSV
from Code import Login
from requests import Session
import sys
import gc

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
def runProcessParallelLogin(session, urlList, outFile):
    categoryValue = []
    listOfFile = []
    # iterator to show program progress
    i = 1
    
    numOfUrl = len(urlList)
    print("There are ", numOfUrl, " records in the input file.\n")
    print("Proceeding......\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 3) as executor:
        future_to_url = {executor.submit(loadUrlSession, session, url): url for url in urlList}
        for future in concurrent.futures.as_completed(future_to_url):
            print("Processing ",i, " / ", numOfUrl, "records.")
            # original url link
            url = future_to_url[future]
            print("Current URL: ", url)
            # opened url
            try:
                html = future.result()
            except:
                httpNoResponse(url)
                break
            if (html.status_code != 404):
                # load target digital collection in html parser
                soup = BeautifulSoup(html.text, 'html.parser')
                # find attributes value
                listOfFile = findFilePage(soup)
                if not (listOfFile == None):
                    getValue(categoryValue, session, listOfFile)
                else:
                    print("This page doesn't have any related file")
                    categoryValue.append([url])
                generateOutput(categoryValue, outFile)
                print("Write into CSV successful.")
                categoryValue = []
                try:
                    nextPageSoup = findNextPage(soup, session)
                    while nextPageSoup != None:
                        listOfFile = findFilePage(nextPageSoup)
                        if listOfFile != None:
                            getValue(categoryValue, session, listOfFile)
                            generateOutput(categoryValue, outFile)
                            print("Write into CSV successful.")
                        else:
                            print("No related file under this url.")
                        listOfFile = []
                        categoryValue = []
                        nextPageSoup = findNextPage(nextPageSoup, session)
                except:
                    findNextPageErr()
            else:
                print("\nCan't open url: 404 page not found. null will be used as filled value")
                print("url: ", url, "\n")
                getNullValue(categoryValue)
                generateOutput(categoryValue, outFile)
            print("All pages processed. No more next page.")
            print("Successfully web-scraped ", i, " / ", numOfUrl, "records.\n")
            urlList.remove(url)
            listOfFile = []
            categoryValue = []
            i = i + 1
            

def httpNoResponse(url):
    print("No response from this url!")
    print("url: ", url)

def findNextPageErr():
    print("\nError happened when finding next page.")
    print("If this kind of error keep happening, save the error message and send to author.")
    print("Press enter to exit. ", end = '')
    input()
    sys.exit()
                    
## call functions to get value for each cell in header
# @param    resultList
#           a list to store results
# @param    session
#           login cookie to access private file record
# @param    fileUrlList
#           a list of url for related files
# @update   resultList
def getValue(resultList, session, fileUrlList):
    fileResult = []
    #intelligent multithreading :)
    numOfFile = len(resultList)
    if numOfFile > 9:
        numOfFile = 9
    if numOfFile < 1:
        numOfFile = 1
        
    with concurrent.futures.ThreadPoolExecutor(max_workers = numOfFile) as executor:
        future_to_url = {executor.submit(loadUrlSession, session, url): url for url in fileUrlList}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            # opened url
            html = future.result()
            # load target digital collection in html parser
            soup = BeautifulSoup(html.text, 'html.parser')
            try:
                fileResult.append(Find.findWorkID(url))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findFileID(url))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findFileName(soup))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findDepositor(soup))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findDateUploaded(soup))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findDateModified(soup))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findFixity(soup))
            except:
                fileResult.append("null")
            try:
                fileResult.append(Find.findCharacterization(soup))
            except:
                fileResult.append("null")
            resultList.append(fileResult)
            fileResult = []
            gc.collect()
            
def getNullValue(resultList):
    fileResult = []
    fileResult.append("null")
    fileResult.append("null")
    fileResult.append("null")
    fileResult.append("null")
    fileResult.append("null")
    fileResult.append("null")
    fileResult.append("null")
    fileResult.append("null")
    resultList.append(fileResult)

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
    result = source.find_all('a', attrs={'rel': 'next'})
    if (result != None and len(result) > 1):
        nextPage = urlPrefix + result[0]['href']
        print("Next page of files is found, processing...")
        html = loadUrlSession(session, nextPage)
        nextPageSoup = BeautifulSoup(html.text, 'html.parser')
        return nextPageSoup
    else:
        return None

## Split a biglist into several small group for better memory management
# @param    urlList
#           the list wait to be splited
# @param    urlGroup
#           a list of list contain url, each small list have 100 url
# @return   totalGroupNum
def splitList(urlList, urlGroup):
    i = 0
    j = 0
    newList = []
    totalLength = len(urlList)
    
    for url in urlList:
        newList.append(url)
        i = i + 1
        j = j + 1
        if i > 999:
            urlGroup.append(newList)
            i = 0
            newList = []
        if ((j == totalLength) and (len(newList) > 0)):
            urlGroup.append(newList)
    totalGroupNum = len(urlGroup)
    print("Total group of url: ", totalGroupNum)

    return totalGroupNum
    
