# To run this, you can install BeautifulSoup
# https://pypi.python.org/pypi/beautifulsoup4

# Or download the file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file


from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
html = urlopen(url, context=ctx).read()

# html.parser is the HTML parser included in the standard Python 3 library.
# information on other HTML parsers is here:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
soup = BeautifulSoup(html, "html.parser")
Looping = int(input('Enter count: '))
Position = int(input('Enter position: '))
# Retrieve all of the anchor tags
nextlink=[]


URL = soup('a')
for link in URL:
    nextlink.append(link.get('href', None))
print("Retrieving: " + str(url))    

for number in range(Looping):
    # Look at the parts of a tag
    print("Retrieving: " + str(nextlink[Position-1]))
    webhtml = urlopen(nextlink[Position-1], context=ctx).read()
    nextlink.clear()
    soup = BeautifulSoup(webhtml, "html.parser")
    URL = soup('a')
    for link in URL:
         nextlink.append(link.get('href', None))
    
