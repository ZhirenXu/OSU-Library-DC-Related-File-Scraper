import urllib.request
from bs4 import BeautifulSoup

def main(): 
  url = "https://library.osu.edu/dc/concern/parent/41687p77w/file_sets/k643b679z"
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
  result = soup.find_all('div')
  fileFormat = "null"
  for item in result:
    if "File Format" in (item.text):
      fileFormat = item.text
  print(fileFormat)

if __name__ == "__main__":
    main()
