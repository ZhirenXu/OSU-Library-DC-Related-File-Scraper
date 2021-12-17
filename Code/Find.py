def findFileName(soup, fileID):
    fileName = ""
    result = soup.find('a', attrs={'href': "/concern/file_sets/"+fileID})
    fileName = result.text
    return fileName

def findWorkID(url):
    result = url.rsplit('/')
    workID = result[-3]

    return workID

def findFileID(url):
    result = url.rsplit('/')
    fileID = result[-1]

    return fileID

def findDepositor(soup):
    result = soup.find('dd', attrs={'itemprop': "accountablePerson"})
    depositor = result.text
    if len(depositor) < 1:
        depositor = "null"
        
    return depositor

def findDateUploaded(soup):
    result = soup.find('dd', attrs={'itemprop': "datePublished"})
    uploadDate = result.text
    if len(uploadDate) < 1:
        uploadDate = "null"
    return uploadDate

def findDateModified(soup):
    result = soup.find('dd', attrs={'itemprop': "dateModified"})
    modifiedDate = result.text
    if len(modifiedDate) < 1:
        modifiedDate = "null"
    return modifiedDate

def findFixity(soup):
    result = soup.find_all('dd')
    fixity = "null"
    for item in result:
        if "Fixity checks" in (item.text):
            fixity = item.text

    return fixity

def findFileFormat(soup):
    result = soup.find_all('div')
    fileFormat = "null"
    for item in result:
        if "File Format" in (item.text):
            fileFormat = item.text[4:len(item.text)-3]
        
    return fileFormat

def findFileTitle(soup):
    result = soup.find_all('div')
    fileTitle = "null"
    for item in result:
        if "File Title" in (item.text):
            fileTitle = item.text[4:len(item.text)-3] 
        
    return fileTitle

def findPageCount(soup):
    result = soup.find_all('div')
    pageCount = "null"
    for item in result:
        if "Page Count" in (item.text):
            pageCount = item.text[4:len(item.text)-3] 

    return pageCount
    
def findCheckSum(soup):
    result = soup.find_all('div')
    checkSum = "null"
    for item in result:
        if "Original Checksum" in (item.text):
            checkSum = item.text[4:len(item.text)-3]

    return checkSum

def findMimeType(soup):
    result = soup.find_all('div')
    mimeType  ="null"
    for item in result:
        if "Mime Type" in (item.text):
            mimeType = item.text[4:len(item.text)-3]

    return mimeType

def findCharacterization(soup):
    characterization = ""
    fileFormat = findFileFormat(soup)
    fileTitle = findFileTitle(soup)
    pageCount = findPageCount(soup)
    checkSum = findCheckSum(soup)
    mimeType = findMimeType(soup)
    
    characterization = fileFormat + '|' + fileTitle + '|' + pageCount + '|' + checkSum + '|' + mimeType

    return characterization
