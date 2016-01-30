# -*- coding: utf-8 -*-
import requests
import sys
import download_beauty
from bs4 import BeautifulSoup
from time import time 
from time import  strftime
requests.packages.urllib3.disable_warnings()


rs=requests.session()
    
def getPageNumber(content) :
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex+5 : endIndex]
    return pageNumber

def crawPage(url, article_list, push_rate):
    res=rs.get(url,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')   

    for r_ent in soup.select('div.r-ent'):
        try:
            atag=r_ent.select('div.title')[0].find('a')
            if(atag):
                URL=atag['href']   
                title=r_ent.select('div.title')[0].text.strip()
                URL='https://www.ptt.cc'+URL
                rate = r_ent.select('div.nrec')[0].text
    
                if(rate):       
                   comment_rate = rate          
                   if rate == u'爆':
                     comment_rate = 100
                   if rate[0] == 'X':
                     comment_rate =  -1 * int(rate[1])          
                else:
                   comment_rate = 0

                if int(comment_rate) >= push_rate:
                   article_list.append((int(comment_rate), URL, title))		                            
        except:
            print 'error:',URL
              
   
if __name__ == '__main__':
    start_page, page_term, push_rate = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) 
    ts = time() 
    CrawlerTime= "BeautyPicture_"+strftime("%Y-%m-%d[%H-%M-%S]")
    if start_page < 0:
        res=rs.get('https://www.ptt.cc/bbs/Beauty/index.html',verify=False)
        soup=BeautifulSoup(res.text,'html.parser')    
        ALLpageURL = soup.select('.btn.wide')[1]['href']
        ALLpage = start_page = int(getPageNumber(ALLpageURL))+1      


    print "Analytical download page..."

    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index' + str(page) + '.html'
        crawPage(page_url, article_list, push_rate)

    total = len(article_list)
    count = 0
    for hot_rate, url, title in article_list:
        download_beauty.store_pic(CrawlerTime, url, str(hot_rate),title)
        count += 1
        print "download: " + str(100 * count / total ) + " %."

    print "DONE"
    print('Time {}s'.format(time() - ts)) 




