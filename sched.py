import requests
from bs4 import BeautifulSoup
import json

term = '201709'
d = 'dummy'
subj = ''
crse = '_____'

class prep(object):
    def __init__(self):
        self.search_request = {
            'TRM': 'U'
            ,'term_in':term
            ,'sel_subj':d,'sel_day':d,'sel_schd':d,'sel_insm':d,'sel_camp':d,'sel_levl':d,'sel_sess':d,'sel_instr':d,'sel_ptrm':d,'sel_attr':d
            ,'sel_subj':subj
            ,'sel_crse':crse
            ,'sel_title':""
            ,'sel_schd':""
            ,'sel_insm':"%25"
            ,'sel_from_cred':""
            ,'sel_to_cred':""
            ,'sel_camp':"%25"
            ,'begin_hh':0
            ,'begin_mi':0
            ,'end_hh':0
            ,'end_mi':0
            ,'end_ap':0
        }

        self.headers = {'Referer': 'https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec'}

def scrape(self):
            payload = json.dumps(self.search_request)
            r = requests.post('https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec', data=payload ,headers=self.headers)
            s = BeautifulSoup(r.text)
            print(s)

#Table Header Class ="ddheader"/> is used for each of the class names
#Find Next Table Class = "bordertable" and Summary = "This table lists the scheduled meeting times and assigned instructors for this class"
#Or Next Caption (class = captiontext) = "Scheduled Meeting Times"
#find next TD class="dbdefault" while next is dbdefault, if dddefault then stop
    #Week (If empty then every week)
    #Time
    #Day
    #Location (If ONLINE or N/A then dont include)
    #Date Range (Gives Start and End, For Labs gives which dates Labs Are)
    #Type of Class

if __name__ == '__main__':
    scraper = prep()
    scraper.scrape()
