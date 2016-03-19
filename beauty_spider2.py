# -*- coding: utf-8 -*-
import download_beauty
import requests
import sys
import time 
from time import strftime
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

rs = requests.session()
Borad = ''
article_list = []
load = {
'from':'/bbs/'+Borad+'/index.html',
'yes':'yes' 
}
    
def getPageNumber(content) :
    startIndex = content.find('index')
    endIndex = content.find('.html')
    pageNumber = content[startIndex+5 : endIndex]
    return pageNumber

def over18(board):
    res = rs.get('https://www.ptt.cc/bbs/' + board + '/index.html', verify = False)
    #先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if ( res.url.find('over18') > -1 ):
       print u"18禁網頁"
       load = {
           'from':'/bbs/'+board+'/index.html',
           'yes':'yes' 
       }
       res = rs.post('https://www.ptt.cc/ask/over18',verify = False, data = load)
       return  BeautifulSoup(res.text,'html.parser')  
    return BeautifulSoup(res.text,'html.parser')  

def crawPage(url, push_rate):
    res = rs.get(url, verify = False)
    soup = BeautifulSoup(res.text,'html.parser')   
    for r_ent in soup.find_all( class_="r-ent"):
        try:
           #先得到每篇文章的篇url
           link = r_ent.find('a')['href']
           comment_rate = ""
           if ( link ) :
               #確定得到url再去抓 標題 以及 推文數
               title = r_ent.find(class_="title").text.strip()            
               rate = r_ent.find(class_="nrec").text
               URL ='https://www.ptt.cc' + link   
               if(rate):       
                  comment_rate = rate          
                  if rate.find(u'爆') > -1:
                    comment_rate = 100
                  if rate.find('X') > -1:
                    comment_rate =  -1 * int(rate[1])          
               else:
                  comment_rate = 0
               #比對推文數
               if int(comment_rate) >= push_rate:
                  article_list.append( (int(comment_rate), URL, title) )       	                            
        except:
           #print u'crawPage function error:',r_ent.find(class_="title").text.strip() 
           print u'本文已被刪除'
              
   
if __name__ == '__main__':
    #python beauty_spider2.py [版名] [爬蟲起始的頁面] [爬幾頁] [推文多少以上] 
    Borad, start_page, page_term, push_rate = sys.argv[1],int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) 
    start_time = time.time()
    CrawlerTime = "_PttImg_"+strftime("%Y%m%d%H%M%S")
    if start_page == 0:
       print u"請輸入有效數字"
       sys.exit()
    
    # 如為 -1 ,則從最新的一頁開始
    if start_page < 0:
        #檢查看板是否為18禁,有些看板為18禁
        soup = over18(Borad) 
        ALLpageURL = soup.select('.btn.wide')[1]['href']
        ALLpage = start_page = int(getPageNumber(ALLpageURL)) + 1      

    print u"Analytical download page..."
    index_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/' + Borad + '/index' + str(page) + '.html'
        index_list.append(page_url)
    
    #抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get( index, verify = False )
        soup = BeautifulSoup(res.text,'html.parser')   
        #如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if (soup.title.text.find('Service Temporarily') > -1) :
            index_list.append(index)
            #print u'error_URL:',index
            time.sleep(1)
        else : 
            crawPage(index, push_rate)
            #print u'OK_URL:', index 
        time.sleep(0.05)
    
    total = len(article_list)
    count = 0
    #進入每篇文章分析內容
    while article_list:
          article = article_list.pop(0)
          # url = article[1] 
          res = rs.get( article[1], verify = False )
          soup = BeautifulSoup(res.text,'html.parser')
          #如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
          if (soup.title.text.find('Service Temporarily') > -1) :
            article_list.append(article)
            #print u'error_URL:',article[1]
            time.sleep(1)
          else : 
            count += 1
            #print u'OK_URL:', article[1]
            # rate = article[0], url = article[1], title = article[2]
            # store_pic(CrawlerTime, url, rate="", title="" ):
            download_beauty.store_pic(CrawlerTime, article[1], str(article[0]), article[2])
            print u"download: " + str(100 * count / total ) + " %."
          time.sleep(0.05)

    print u"下載完畢..."
    print u"execution time:" + str(time.time() - start_time)+"s"
    
    



