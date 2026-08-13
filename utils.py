import urllib.request

def saveImage(imageUrl, saveAs):
    urllib.request.urlretrieve(imageUrl, saveAs)
