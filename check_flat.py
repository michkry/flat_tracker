#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from requests_file import FileAdapter # FOR TESTING ONLY

#headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0" }
#url = "https://www.idealista.com/alquiler-viviendas/valencia-valencia/con-precio-hasta_600,metros-cuadrados-mas-de_40/?ordenado-por=precios-asc"
#page = requests.get(url, headers=headers)
#pageBs = BeautifulSoup(page.content, "html.parser")
#ex = pageBs.find(id="main-content").string

###### FOR TESTING ONLY #######################
url = "file:///home/hiciak/Dropbox/Programacion/python/scripts/idealista/pagina_prueba/val.html"
s = requests.Session()
s.mount("file://", FileAdapter())
r = s.get(url)
###### FOR TESTING ONLY #######################

pageBs = BeautifulSoup(r.content, "html.parser")
ex = pageBs.find(attrs={"data-adid": 83548190})
print(ex)
