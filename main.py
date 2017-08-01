import urllib3
http = urllib3.PoolManager()
response = http.request('POST',
'https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec?TRM=U&term_in=201709&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=&sel_crse=3__0&sel_title=&sel_schd=&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&begin_hh=0&begin_mi=0&begin_ap=p&end_hh=0&end_mi=0&end_ap=a')

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.data)
