from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
import favicon
import hashlib
import snoop
import json
import os

#######CONSTANTS######
path = os.path.normpath(__file__).split(os.sep)
path.pop(-1)
path.pop(-1)
path = "\\".join(path)

DIRPATH = path
DELETE_URL = os.path.join(DIRPATH,r"Images\jokuka.png")
SESSION_SETTINGS = os.path.join(DIRPATH,r"Images\SessionSettings.png")
CHECK_URL = os.path.join(DIRPATH,r"Images\csek3.png")
UNCHECK_URL = os.path.join(DIRPATH,r"Images\uncsek4.png")
WINDOW_ICON = os.path.join(DIRPATH,r"Images\windowicon.png")
LOAD_NO_ICON = os.path.join(DIRPATH,r"Images\noload2.png")
ALL_LINK_TICK = os.path.join(DIRPATH,r"Images\alltick.png")
ALL_LINK_UNTICK = os.path.join(DIRPATH,r"Images\noalltick.png")
DATABASE = os.path.join(DIRPATH,r"links.json")

######FUNCTIONS######
def relpath(path): #working with relatve paths with current script
    return os.path.join(DIRPATH,path)

def hash_title(text):
    return str(hashlib.sha1(bytes(text,"utf-8")).hexdigest())

def url_title(website_url:str) -> str:

    # get webpage data without error 403 with headers
    soup = BeautifulSoup(urlopen(Request(website_url,headers={"User-Agent": "Mozilla/5.0"})),"html.parser")

    # displaying the title
    return soup.title.get_text()

#@snoop
def url_icon(website_url:str) -> None:
    icons = favicon.get(website_url)

    #get all icon urls
    if icons != []:

        #check for PNG format
        for i in icons:
            if ".png" in i.url:
                icon = i.url
                break
            else:
                pass
        else:
            print("No PNG format")
            return

        title = url_title(website_url)
        hashname = hash_title(title)

        response = requests.get(icon, stream=True)
        #catch request reject
        if response.status_code == 404:
            print(f"Request rejected with [404] status for url: {website_url}")
            return
        
        #save icon image
        file_path = os.path.join(DIRPATH,"icons",hashname+".png")
        bytes = BytesIO(response.content)
        img = Image.open(bytes)
        img = img.resize((32,32))
        img.save(file_path)
    else:
        print(f"We cannot find any available icon file for url: {website_url}")

if __name__ == '__main__':
    #handle json
    r""" with open(r"C:\Users\borhe\Downloads\ItWork\Projects\Usehan\Usehan\links.json","r") as file:
        data = json.load(file)
        urls = []
        
        for session in data:
            for element in range(len(data[session])):
                data[session][element]["title"] = url_title(data[session][element]["url"])

    with open(r"C:\Users\borhe\Downloads\ItWork\Projects\Usehan\Usehan\links.json", "w") as write_file:
        json.dump(data, write_file,indent=4) """
    
    print(DIRPATH)
        

