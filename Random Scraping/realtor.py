from bs4 import BeautifulSoup
import requests
import re

minPrice = '100000'
maxPrice = '800000'

bedRange = '3-0'
bathRange = '3-3'

curPage = '1'

address_id = 'hm_lst_address'
address_class = 'm_gallery_lst_cell_address clickable'

price_id = 'hm_lst_price'
price_class = 'm_gallery_lst_cell_price'

bed_id = 'hm_lst_bed_num'
bath_id = 'hm_lst_bath_num'
bed_bath_class = 'm_gallery_lst_cell_bed_bath' #get spans inside

url  = "https://www.realtor.ca/Residential/Map.aspx#CultureId=1&ApplicationId=1"
url += "&RecordsPerPage=9&MaximumResults=9&PropertySearchTypeId=1&PriceMin=" + minPrice
url += "&PriceMax=" + maxPrice +"&TransactionTypeId=2&StoreyRange=0-0&BuildingTypeId=1"
url += "&ConstructionStyleId=3&BedRange=" + bedRange + "&BathRange=" + bathRange + ""
url += "&LongitudeMin=-79.24541473388672&LongitudeMax=-78.9364242553711&LatitudeMin=43.79563252135698"
url += "&LatitudeMax=43.92930267631971&SortOrder=A&SortBy=1&viewState=g&favouritelistingids=18230582,18292971,18297982"
url += "&Longitude=-79.0747833251953&Latitude=43.8983871698998&ZoomLevel=11&CurrentPage=" + curPage
url += "&PropertyTypeGroupID=1"

r  = requests.get(url)

sauce = r.text

soup = BeautifulSoup(sauce, "html.parser")

print soup

for div in soup.find_all('div', attrs={"class": address_class}):
    print div.text
