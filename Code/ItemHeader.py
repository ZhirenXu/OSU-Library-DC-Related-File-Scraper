##Return a list of item data header we want to put in csv file
# @return   itemHeader
#           The list contain all item header name
def getItemHeader():
    itemHeader = ["Work ID", "File ID", "File Title", "Depositor", "Date Upload",
                  "Date Modified", "Fixity Check", "Characterization"]

    return itemHeader
