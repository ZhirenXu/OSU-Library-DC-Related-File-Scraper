##Return a list of file data header we want to put in csv file
# @return   fileHeader
#           The list contain all category name
def getHeader():
    fileHeader = ["Work ID", "File ID", "Depositor", "Date Uploaded", "Date Modified", "Fixity Check",
                    "Characterization"]

    return fileHeader

def getCharacterizationAttribs():
    attribs = ["Height", "Width", "File Format", "Original Checksum", "Mime Type"]

    return attribs
