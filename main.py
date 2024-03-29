from bs4 import BeautifulSoup
import requests
import re
import pandas
from datetime import date

sources =  ['https://www.mediamarkt.se/sv/category/_alla-tv-apparater-564040.html?searchParams=%2FSearch.ff%3FfilterTabbedCategory%3Donlineshop%26filterCategoriesROOT%3DTV%25C2%25A7MediaSEsvc510055%26filterCategoriesROOT%252FTV%25C2%25A7MediaSEsvc510055%3DAlla%2BTV-apparater%25C2%25A7MediaSEsvc564040%26filteravailability%3D1%26filtercurrentprice%3D6479%2B-%2B17933%26channel%3Dmmsesv%26productsPerPage%3D24%26followSearch%3D10000%26disableTabbedCategory%3Dtrue%26navigation%3Dtrue%26filterSk%25C3%25A4rmstorlek%3D55%2B-%2B77&sort=price&view=PRODUCTLIST&page=', 'https://www.mediamarkt.se/sv/category/_alla-tv-apparater-564040.html?searchParams=%2FSearch.ff%3FfilterTabbedCategory%3Donlineshop%26filterCategoriesROOT%3DTV%25C2%25A7MediaSEsvc510055%26filterCategoriesROOT%252FTV%25C2%25A7MediaSEsvc510055%3DAlla%2BTV-apparater%25C2%25A7MediaSEsvc564040%26filteravailability%3D1%26filtercurrentprice%3D6479%2B-%2B17933%26channel%3Dmmsesv%26productsPerPage%3D24%26followSearch%3D10000%26disableTabbedCategory%3Dtrue%26navigation%3Dtrue%26filterSk%25C3%25A4rmstorlek%3D55%2B-%2B77&sort=price&view=PRODUCTLIST&page=2', 'https://www.mediamarkt.se/sv/category/_alla-tv-apparater-564040.html?searchParams=%2FSearch.ff%3FfilterTabbedCategory%3Donlineshop%26filterCategoriesROOT%3DTV%25C2%25A7MediaSEsvc510055%26filterCategoriesROOT%252FTV%25C2%25A7MediaSEsvc510055%3DAlla%2BTV-apparater%25C2%25A7MediaSEsvc564040%26filteravailability%3D1%26filtercurrentprice%3D6479%2B-%2B17933%26channel%3Dmmsesv%26productsPerPage%3D24%26followSearch%3D10000%26disableTabbedCategory%3Dtrue%26navigation%3Dtrue%26filterSk%25C3%25A4rmstorlek%3D55%2B-%2B77&sort=price&view=PRODUCTLIST&page=3']
count = 1
files = []

for source in sources:
    get_page = requests.get('%s' % source).text
    with open("mediamarkt_%d.txt" % count, "w") as file_open:
        file_open.write(get_page)
    file = open("mediamarkt_%d.txt" % count, "r")
    files.append(file)
    count += 1

names = []
brands = []
prices = []
dimensions = []

for file in files:
    soup = BeautifulSoup(file, 'lxml')
# print(soup.prettify())
    rows = soup.find_all('script')
    for row in rows:
        if "var product" in row.text:
            #m = re.compile('<script>(.*?)</script>', re.DOTALL).findall(row.text)
            m = re.search('{(.+?)}', row.string)
            #print(m.group(1))
            splittext = m.group(1).split(',')
            for n in splittext:
                if "name" in n:
                    split_name = n.split(':')
                    names.append(split_name[1].strip('\"'))
                if "price" in n:
                    split_price = n.split(':')
                    prices.append(split_price[1].strip('\"'))
                if "dimension10" in n:
                    dimensions.append(n)
                if "brand" in n:
                    split_brand = n.split(':')
                    brands.append(split_brand[1].strip('\"'))


cols = ['Name', 'Brand', 'Price']
export = pandas.DataFrame({'Name': names,
                           'Brand': brands,
                           'Price': prices,
                           })[cols]

export.to_excel('mediamarkt_'+str(date.today())+'.xls')


for file in files:
    file.close()


