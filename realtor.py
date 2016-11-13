from lxml import html
import requests

page = requests.get("http://www.realtor.ca/Residential/Map.aspx#CultureId=1&ApplicationId=1&RecordsPerPage=9&MaximumResults=9&PropertySearchTypeId=1&PriceMax=700000&TransactionTypeId=2&StoreyRange=0-0&BuildingTypeId=1&BedRange=3-0&BathRange=0-0&LongitudeMin=-79.26025805297851&LongitudeMax=-78.84861407104492&LatitudeMin=43.783208667602054&LatitudeMax=43.9356993371907&SortOrder=A&SortBy=1&viewState=l&Longitude=-79.25116&Latitude=43.8366&ZoomLevel=12&CurrentPage=1&PropertyTypeGroupID=1")
tree = html.fromstring(page.content)

address = tree.xpath('//span[@class="list_lst_address"]/text()')
print 'address: ', address
