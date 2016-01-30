# -*- coding: utf-8 -*-
# 使用方法
# 請將要下載的PTT 表特版文章網址放到 input.txt 中
# 在終端機中輸入：python download_beauty.py input.txt
# 下載的圖片會以該表特文章標題作為資料夾名稱
#

import os
import sys
import requests
import shutil
import multiprocessing
from time import time 
from bs4 import BeautifulSoup
from functools import partial
from time import  strftime
requests.packages.urllib3.disable_warnings()

rs=requests.session()

def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value.rstrip();


def store_pic(CrawlerTime, url, rate="", title="" ):
    res=rs.get(url,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')      
    if(title == ""):
       try:
          title= soup.select('.article-meta-value')[2].text
       except:
          title= "no title"

    dir_name = remove(title, '\/:*?"<>|.') + "_"+ rate 
    pic_url_list=[]

    for img in soup.select('img'):
        if (img['src'].find('.jpg')>0 or img['src'].find('.png')>0):
            if (img['src'].find('http')==-1 ):
               link= 'http:'+ img['src'] 
            else:
               link= img['src']    
            pic_url_list.append(link)

    if(len(pic_url_list)!=0):
        relative_path = os.path.join(CrawlerTime,dir_name)
        path= os.path.abspath(relative_path) 
        try:    
           if not os.path.exists(path):                    
              os.makedirs(path)              
        except Exception, e: 
           print 'os.makedirs(path) error'  
  
        pool_size = multiprocessing.cpu_count()*2        
        download = partial(download_link, relative_path)      
        pool = multiprocessing.Pool(processes=pool_size, 
                                    #initializer=start_process, 
                                    #maxtasksperchild=4, 
        ) 
        
        pool_outputs = pool.map(download, pic_url_list) 
        pool.close() 
        pool.join() 
 
def download_link(directory, link): 
    resImg=rs.get(link, stream=True,verify=False)  
    filename= link.split('/')[-1]              
    relative_path = os.path.join(directory,filename)
    path= os.path.abspath(relative_path)
    try:   
        if not os.path.exists(path): 
           with open(path, 'wb') as out_file: 
                shutil.copyfileobj(resImg.raw, out_file) 
           del resImg         
    except Exception, e: 
        print 'shutil.copyfileobj error'     
       
        
def main():
    print "Crawler Parsing...."
    CrawlerTime= "BeautyPicture_"+strftime("%Y-%m-%d[%H-%M-%S]")
    ts = time() 
    beauty_article_urls = []
    # 從檔案中讀入 urls
    total=0
    with open(sys.argv[1]) as fd:
        for url in fd:
            beauty_article_urls.append(url.strip())
            total+=1
            
    count=0
    for article_url in beauty_article_urls:
        # 下載該網頁的圖片
        count+=1
        print "Crawling: " + str(100 * count / total ) + " %."
        store_pic(CrawlerTime,article_url)
        
    print('Time {}s'.format(time() - ts)) 
    print "Crawler End...."

if __name__ == '__main__':
    main()



    
