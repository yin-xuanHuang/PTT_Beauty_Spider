# -*- coding: utf-8 -*-

import os
import sys
import requests
import shutil
import multiprocessing
import time 
from time import  strftime
from bs4 import BeautifulSoup
from functools import partial
requests.packages.urllib3.disable_warnings()

rs = requests.session()
#移除特殊字元（移除Windows上無法作為資料夾的字元）
def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value.rstrip();

#符合圖片格式的網址
def isImageFormat(link):
    if(link.find('.jpg') > -1 or link.find('.png') > -1 or link.find('.gif') > -1 or link.find('.jpeg') > -1):
       return True;
    return False;

def store_pic(CrawlerTime, url, rate="", title="" ):
    #檢查看板是否為18禁,有些看板為18禁
    soup = over18(url)  
    CrawlerTime = url.split('/')[-2] + CrawlerTime
    #避免有些文章會被使用者自行刪除標題列  
    if(title == ""):
       try:
          title = soup.select('.article-meta-value')[2].text
       except:
          title = "no title"
    
    dir_name = remove(title, '\/:*?"<>|.') + "_"+ rate 
    pic_url_list = []

    #抓取圖片URL(img tag )
    for img in soup.select('img'):
        if ( isImageFormat(img['src']) ):
            if (img['src'].find('http') == -1 ):
               link = 'http:'+ img['src'] 
            else:
               link = img['src']    
            pic_url_list.append(link)

    #開始建立資料夾,使用文章標題做為資料夾的名稱
    if( len(pic_url_list) != 0):
        relative_path = os.path.join(CrawlerTime,dir_name)
        path = os.path.abspath(relative_path) 
        try:    
           if not os.path.exists(path):                    
              os.makedirs(path)              
        except Exception, e: 
           print u'os.makedirs(path) error'  
  
        pool_size = multiprocessing.cpu_count() * 2        
        download = partial(download_link, relative_path)      
        pool = multiprocessing.Pool(processes = pool_size, 

        ) 
        
        pool_outputs = pool.map(download, pic_url_list) 
        pool.close() 
        pool.join() 
 
def download_link(directory, link): 
    resImg = rs.get(link, stream = True,verify = False) 
    #使用網址的最後一個字串設為圖片檔案名稱 
    filename = link.split('/')[-1]              
    relative_path = os.path.join(directory,filename)
    path = os.path.abspath(relative_path)
    try:   
        if not os.path.exists(path): 
           with open(path, 'wb') as out_file: 
                shutil.copyfileobj(resImg.raw, out_file) 
           del resImg         
    except Exception, e: 
        print u'shutil.copyfileobj error'     
   
def over18(url):
    res = rs.get(url, verify = False)
    #先檢查網址是否包含'over18'字串 ,如有則為18禁網站
    if ( res.url.find('over18') > -1 ):
       print u"18禁網頁"
       #從網址獲得版名
       Board = url.split('/')[-2]
       load = {
           'from':'/bbs/'+Board+'/index.html',
           'yes':'yes' 
       }
       res = rs.post('https://www.ptt.cc/ask/over18',verify = False, data = load)
       return  BeautifulSoup(res.text,'html.parser')  
    return BeautifulSoup(res.text,'html.parser')  
        
def main():
    print u"Analytical download page..."
    CrawlerTime = "_PttImg_"+strftime("%Y%m%d%H%M%S")
    start_time = time.time()
    beauty_article_urls = []
    # 從.txt檔案中讀取 urls
    total = 0
    with open(sys.argv[1]) as fd:
        for url in fd:
            if( url.strip().find("www.ptt.cc") > -1 ):
               beauty_article_urls.append(url.strip())
               total += 1
            
    count = 0
    while beauty_article_urls :
          URL = beauty_article_urls.pop(0)
          #檢查看板是否為18禁,有些看板為18禁
          soup = over18(URL)
          #如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
          if (soup.title.text.find('Service Temporarily') > -1) :
              beauty_article_urls.append(URL);
              #print u'error_URL:',URL
              time.sleep(1)
          else : 
              #print u'OK_URL:', URL 
              # 下載該網頁的圖片
              count += 1       
              store_pic(CrawlerTime, URL)
              print u"Crawling: " + str(100 * count / total ) + " %."
          time.sleep(0.05)
          
    print u"下載完畢..."
    print u"execution time:" + str(time.time() - start_time)+"s"

if __name__ == '__main__':
    main()






    
