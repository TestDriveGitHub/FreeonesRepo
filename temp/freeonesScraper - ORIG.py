import csv
import requests
from BeautifulSoup import BeautifulSoup

pornstar = 'Janet Mason'
url = 'http://www.freeones.com/html/' + pornstar[:1] + '_links/bio_' + pornstar.replace(' ','_') + '.php'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)
table = soup.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="biographyTable") 

list_of_rows = []
for row in table.findAll('tr'):
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '').replace(':','')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

outfile = open("./"+pornstar+".csv", "wb")
writer = csv.writer(outfile)
writer.writerows(list_of_rows)