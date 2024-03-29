import sys

## print program info
def showInfo():
    print("*************************************")
    print("*     DC related File Scrapper      *")
    print("*        Author: Zhiren Xu          *")
    print("*     published data: 12/17/21      *")
    print("*************************************")

## print exit message
# @param    fileOut
#           name of output file
def sysExit(fileOut):
    print("\nThe program is finished. The output file is: ", fileOut, " . It is located in the same folder with your DC Item Scrapper program. Press enter to exit.")
    key = input()
    sys.exit()
