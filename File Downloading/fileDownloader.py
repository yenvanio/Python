from bs4 import BeautifulSoup as soup
import urllib
import requests
import os
import shutil

def openLink(ref_url, url):
    r = urllib.urlopen(ref_url + url)
    sauce = soup(r,"lxml")
    items = sauce.find_all('li', {'class' : 'ui-li-has-thumb folder-cell'})

    if items:
        for item in items:
            # Check if File or Folder
            data_type = item['data-item-type']
            if data_type == 'folder':
                # If Folder
                a = item.findNext('a', href=True)
                folder = a.findNext('h3', {'class' : 'files-item-name'})
                folder_name = folder.get_text()
                try:
                    os.chdir(folder_name)
                except:
                    os.mkdir(folder_name)
                    os.chdir(folder_name)
                openLink(ref_url, a['href'])
                os.chdir('..')
            else:
                # If File
                a = item.findNext('a', href=True)
                r = urllib.urlopen(ref_url + a['href'])
                sauce = soup(r,"lxml")
                header = sauce.find('li', {'class' : 'header-title'})
                file_name = header.findNext('h1', {'class' : 'ellipsis'}).get_text()

                # Download Content (Assuming this is a file because no listview items)
                print "Downloading file:%s" % file_name

                # Creating Response Object
                r = requests.get(ref_url + url, stream = True)

                # Download Started
                with open(file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size = 1024*1024):
                        if chunk:
                            f.write(chunk)

                print "%s downloaded!\n" % file_name

if __name__ == '__main__':
    shutil.rmtree('/Users/shiv/documents/github/Python/File Downloading/Output', ignore_errors=True)
    ref_url = 'https://m.box.com'
    url = '/shared_item/https%3A%2F%2Fapp.box.com%2Fs%2Fb0h6tlrwdlglnysa2t2m6i0j3xz7gkd2/browse/3588211957'
    openLink(ref_url, url)
