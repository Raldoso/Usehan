from urllib.request import urlopen
from bs4 import BeautifulSoup
from constanst import DIRPATH
import requests 
import favicon
import os


def relpath(path): #working with relatve paths with current script
    dirpath = os.path.dirname(__file__)
    return os.path.join(dirpath,path)

def url_title(website_url:str) -> str:

    # using the BeaitifulSoup module
    soup = BeautifulSoup(urlopen(website_url),"html.parser")

    # displaying the title
    return soup.title.get_text()

def url_icon(website_url:str):
    icons = favicon.get(website_url)

    #get icon with 32x32 sizes
    for i in icons:
        if i.url.count("32") == 2:
            icon = i.url
            break
    else: #if theres no 32x32 icon pick the first one
        icon = icons[0].url
    
    response = requests.get(icon, stream=True)

    #replace spaces in title for filenames
    title = url_title(website_url)
    table = title.maketrans(" ","_")
    title = title.translate(table)

    #remove forbidden filename characters
    remove_punctuation_map = dict((ord(char), None) for char in r'\/*?:"<>|')
    title = title.translate(remove_punctuation_map)
    
    file_path = os.path.join(DIRPATH,"icons",title+".png")
    file = open(file_path,"wb")
    file.write(response.content)
    file.close()
    return file_path

if __name__ == '__main__':
    url_icon("https://www.frandieguez.dev/posts/how-to-build-a-split-keyboard-lily58-pro/")
