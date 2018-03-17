"""
Contains logic for creating an icon for the input folder.
"""
import os
import json
import random
import io

import urllib.request as urllib2
from bs4 import BeautifulSoup
from PIL import Image

# https://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden 
# Filled using instructions at : 
# https://www.mkyong.com/computer-tips/how-to-view-http-headers-in-google-chrome/
REQUEST_HEADER = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                  (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp\
                  ,image/apng,*/*;q=0.8',
                  'Accept-Language': 'en-US,en;q=0.9',
                  'Connection': 'keep-alive'}

IMAGE_DOWNLOAD_LIMIT = 10

def find_and_convert(root, srch_str):
    """
    Searches google images for the srch_str provided, selects one at random, 
    converts it into .ico format, saves it to the appropriate directory
    and returns the file.
    """
    query_str = '+'.join(srch_str.split())
    url = "https://www.google.co.in/search?q=" + query_str + \
          "&source=lnt&tbm=isch&tbs=isz:ex,iszw:256,iszh:256"
    req = urllib2.Request(url, headers=REQUEST_HEADER)
    soup = BeautifulSoup(urllib2.urlopen(req, timeout=200).read(), 'html.parser')
    
    img_arr = []
    for a_tag in soup.find_all("div", {"class":"rg_meta"}):
        img_link = json.loads(a_tag.text)["ou"] 
        try:
            opener = urllib2.URLopener()
            opener.addheaders = [('User-Agent', REQUEST_HEADER['User-Agent']), 
                                 ('Accept', REQUEST_HEADER['Accept']), 
                                 ('Accept-Language', REQUEST_HEADER['Accept-Language']), 
                                 ('Connection', REQUEST_HEADER['Connection'])]
            opener.retrieve(img_link)
        except urllib2.HTTPError:
            # urllib2.HTTPError: HTTP Error 403: Forbidden 
            continue
        
        img_arr.append(img_link)
        if len(img_arr) == IMAGE_DOWNLOAD_LIMIT:
            break
        
    img_choice = random.choice(img_arr) if(len(img_arr) != 0) else None
    if not img_choice:
        return ""
    
    req = urllib2.Request(img_choice, headers=REQUEST_HEADER)
    img = Image.open(io.BytesIO(urllib2.urlopen(req, timeout=200).read()))
    img = img.convert("RGB")
    ico_file_name = os.path.join(os.path.join(root, srch_str), srch_str + ".ico")
    img.save(ico_file_name)
    return ico_file_name
