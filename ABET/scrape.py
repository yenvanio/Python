from bs4 import BeautifulSoup as soup
from bs4 import Tag, NavigableString
import urllib
import requests

url = 'file:///Users/shiv/Documents/GitHub/Python/ABET/E002-EAC-Self-Study-Questionnaire-08-19-19.html'

r = urllib.urlopen(url)
sauce = soup(r, "lxml")

# Gets the text from a section given the HREF
def getSectionText(href):
    text = ''
    section_link = sauce.find('a', attrs = { 'name' : href })
    section_header = section_link.find_next('h1')
    if section_header is not None :
        first_p = section_header.find_next('p')
        while first_p is not None :
            first_p = first_p.next_element
            if first_p is not None and first_p.name == 'p':
                if isinstance(first_p, Tag):
                    print(first_p.get_text())
    return text

# Generates an Information Modal based on all sections aside from the template
def getInformationModal(headers, links):
    html = '<app-info-modal>'
    count = 0
    while (count < len(headers)):
        html += '<section title = {}>'.format(headers[count].encode('utf-8'))
        html += '<content body = {}>'.format(getSectionText(links[count]))
        html += '</content>'
        html += '</section>'
        count = count + 1
    html += '</app-info-modal>'
    return html

# Gets Headings & Links for all TOC items
def parseTableOfContents(section):
    headers = []
    links = []
    arr_a = section.find_all('a')
    for a in arr_a :
        headers.append(a.find_next('span').get_text())
        links.append(a['href'].replace('#', ''))
    return getInformationModal(headers, links)

# Checks if a WordSection is equivalent to the title
def isSection(section, title):
    # section_sauce = soup(section, "lxml")
    span = section.find("span", string=title)
    if span is None :
        return False
    else :
        return True

count = 1
while (count != -1) :
    section = sauce.find('div', {'class' : 'WordSection' + str(count)});
    if section is None :
        count = -1;
    else:
        # print('WordSection' + str(count))
        section = sauce.find('div', {'class' : 'WordSection' + str(count)})
        if (isSection(section, 'Table of Contents')):
            table_of_contents = parseTableOfContents(section)
            # print(table_of_contents)
        count = count + 1
