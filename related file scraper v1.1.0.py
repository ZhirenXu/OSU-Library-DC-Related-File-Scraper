from Code import Greeting
from Code import SimpleCSV
from Code import Run
import concurrent.futures
from Code import Login
from Code import ItemAttribute
from Code import Header
import gc

def main(*argv):
    itemURL = []
    idList = []
    urlGroup = []
    csvIn = ""
    csvOut = ""
    liTagList = []
    
    Greeting.showInfo()
    logSession = Login.login()
    header = Header.getHeader()
    csvIn = SimpleCSV.getCSVInput()
    csvOut = SimpleCSV.getCSVOutput()
    #now just get first colomn, parent id
    urlList = SimpleCSV.readColomn(csvIn, 0)
    totalGroupNum = Run.splitList(urlList, urlGroup)

    with open(csvOut, 'w', encoding = 'utf8',newline = '') as outFile:
        SimpleCSV.writeCSV(header, outFile)
        for listOfUrl in urlGroup:
            Run.runProcessParallelLogin(logSession, listOfUrl, outFile)
            if totalGroupNum > 1:
                print("\nOne group of works is scanned. Cleaning memory and reauthorizing now.")
                logSession.close()
                gc.collect()
                logSession = Login.reAuth()
                print("Done")
                urlGroup = urlGroup - 1
                print("Remain group number: ", len(urlGroup))
        
    Greeting.sysExit(csvOut)
    
if __name__ == "__main__":
    main()
