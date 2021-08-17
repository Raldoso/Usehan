from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
import favicon
import hashlib
import webbrowser
import snoop
import json
import os

#######APP ICON PATHS######
path = os.path.normpath(__file__).split(os.sep)
path.pop(-1)
path.pop(-1)
path = "\\".join(path)

DIRPATH = path
DELETE_URL = os.path.join(DIRPATH,r"Images\jokuka.png")
RESTORE_TITLE = os.path.join(DIRPATH,r"Images\refresh2.png")
SETTINGS = os.path.join(DIRPATH,r"Images\settings3.png")
SETTINGS_HOVER = os.path.join(DIRPATH,r"Images\settings3hover.png")
CHECK_URL = os.path.join(DIRPATH,r"Images\csek3.png")
UNCHECK_URL = os.path.join(DIRPATH,r"Images\uncsek4.png")
WINDOW_ICON = os.path.join(DIRPATH,r"Images\windowicon.png")
LOAD_NO_ICON = os.path.join(DIRPATH,r"Images\noload2.png")
LAUNCH_LINK = os.path.join(DIRPATH,r"Images\alltick.png")
NOT_LAUNCH_LINK = os.path.join(DIRPATH,r"Images\noalltick.png")
LAUNCH_LINK_HOVER = os.path.join(DIRPATH,r"Images\tikboxhover.png")
NOT_LAUNCH_LINK_HOVER = os.path.join(DIRPATH,r"Images\notikboxhover.png")
DATABASE = os.path.join(DIRPATH,r"links.json")
ICON_DATABASE = os.path.join(DIRPATH,r"icons")

######GLOBAL APP FUNCTIONS######
def relpath(path): #working with relatve paths with current script
    return os.path.join(DIRPATH,path)

def hash_url(text): #return hashed string
    return str(hashlib.sha1(bytes(text,"utf-8")).hexdigest())

def get_url_title(website_url:str) -> str: #Returns websites titles in string format with URL path

    # get webpage data without error 403 with headers
    soup = BeautifulSoup(urlopen(Request(website_url,headers={"User-Agent": "Mozilla/5.0"})),"html.parser")

    # displaying the title
    return soup.title.get_text()

def download_url_icon(website_url:str) -> None: #DOWLOAD LINK ICON WITH URL AND SAVE WITH HASHED NAME

    icons = favicon.get(website_url)

    #get all icon urls
    if icons != []:

        #check for PNG or ICO format
        for i in icons:
            if ".png" in i.url or ".ico" in i.url:
                icon = i.url
                break
            else:
                pass
        else:
            print("No PNG or ICO format")
            return

        hashname = hash_url(website_url)

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

def donwload_link(url:str,session=str,database=dict) -> None: #DOWNLOAD ICON AND PARSE DATA INTO DATABASE

    download_url_icon(url)
    title = get_url_title(url)

    link = {
        "url": url,
        "title": title
    }

    database[session].append(link)

    #save link to global database
    with open(DATABASE,"w") as file:
        json.dump(database, file, indent=4)

def delete_link(url:str,session:str,database=dict) -> None: #DELETE LINK, SAVE DATABSE, DELETE ICON

    for link in database[session]:
        if link["url"] == url:
            database[session].remove(link)

    json.dump(database, open(DATABASE,"w"),indent=4)

    if os.path.exists(os.path.join(ICON_DATABASE,f"{hash_url(url)}.png")):
        os.remove(os.path.join(ICON_DATABASE,f"{hash_url(url)}.png"))

def modify_url(oldurl:str, newurl:str,session:str, database=dict) -> None: #CHANGE STORED URL AND SAVE
    
    for i in range(database[session]):
        if database[session][i]["url"] == oldurl:
            database[session][i]["url"] = newurl

    #link icon needs to be renamed to the new title
    if os.path.exists(os.path.join(ICON_DATABASE,f"{hash_url(oldurl)}.png")):
        os.rename(
            os.path.join(ICON_DATABASE,f"{hash_url(oldurl)}.png"),
            os.path.join(ICON_DATABASE, f"{hash_url(newurl)}.png"))

    json.dump(database, open(DATABASE,"w"),indent=4)

def modify_title(oldtitle:str, newtitle:str, session:str, database=dict) -> None: #CHANGE STORED TITLE AND SAVE

    for i in range(len(database[session])):
        if database[session][i]["title"] == oldtitle:
            database[session][i]["title"] = newtitle

    json.dump(database, open(DATABASE,"w"),indent=4)



if __name__ == '__main__':
    database = json.load(open(DATABASE,"r"))
    #print(database)
    #delete_link("https://realpython.com/pyinstaller-python/","Embedd Python",database)
    donwload_link("https://boardsource.xyz/store","Buy keyboard",database)






    


    
    
        

