# Usage:
# python parser.py "https://rentry.org/244wt"

import requests
from bs4 import BeautifulSoup
import pypandoc
import re
import requests
import sys
import os

URL = sys.argv[1] + '/raw'
pagename = URL.split('/')[-2]
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
output = pypandoc.convert_text(soup, 'mediawiki', format='md')
# output = re.sub(r'(https?:\/\/.*\/)', '', output)
source_str = "{{Copycat|" + sys.argv[1] + "}}"
output = output + source_str

pic_links_regex = r"(https?:\/\/.*?\.(?:png|jpg){1})"
pics = re.findall(pic_links_regex, str(soup))

os.makedirs(pagename, exist_ok = True)
os.makedirs(f"{pagename}/img", exist_ok = True)
for lnk in pics:
    r = requests.get(lnk, allow_redirects=True)
    filename = lnk.split('/')[-1]
    print(f"downloading {filename}")
    open(f"{pagename}/img/{filename}", 'wb').write(r.content)

open(f"{pagename}/index.txt", 'wb').write(output.encode())
