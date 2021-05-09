from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from constanst import DIRPATH
import requests
import favicon
import os
import snoop
from colorthief import ColorThief
import hashlib
from PIL import Image
from io import BytesIO

def relpath(path): #working with relatve paths with current script
    dirpath = os.path.dirname(__file__)
    return os.path.join(dirpath,path)

def hash_title(text):
    return str(hashlib.sha1(bytes(text,"utf-8")).hexdigest())

def url_title(website_url:str) -> str:

    # get webpage data without error 403 with headers
    soup = BeautifulSoup(urlopen(Request(website_url,headers={"User-Agent": "Mozilla/5.0"})),"html.parser")

    # displaying the title
    return soup.title.get_text()

@snoop
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
        if response.status_code == 404:
            print(f"we cannot find availeble icon for url: {website_url}")
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
    urls = ["https://www.solutionsinplastic.com/keycap-manufacturing/",
            "https://www.dataschool.io/how-to-contribute-on-github/",
            "https://nicolasbarral.fr/git-novice/08-collab/",
            "https://docs.github.com/en/github/getting-started-with-github/why-is-git-always-asking-for-my-password",
            "https://boardsource.xyz/store",
            "https://mechboards.co.uk/",
    ]

    [url_icon(url) for url in urls]
    #url_icon("https://docs.github.com/en/github/getting-started-with-github/why-is-git-always-asking-for-my-password")
    #print(url_title(url))
    #color_thief = ColorThief(relpath(r"icons\How_to_build_a_split_keyboard_-_Lily58_Pro__Fran_Dieguez.png"))
    r""" color_thief = ColorThief(relpath(r"icons\Why_is_Git_always_asking_for_my_password_-_GitHub_Docs.png"))
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=20)
    print(list(set(palette))) """
