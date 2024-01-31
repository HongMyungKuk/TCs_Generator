
def GetFilename(filepath) : 
    filename = ''
    temp = str(filepath)
    index = temp.rfind('/')

    filename = filepath[index+1:]

    return filename
