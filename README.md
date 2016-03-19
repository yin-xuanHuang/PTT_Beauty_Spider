# PTT圖片下載器 (Python) For Windows and Linux 
A crawler picture for web PTT 

## 特色
* 抓取PTT 圖檔(包含推文)
* 可指定要抓取的看板以及推文數多少以上

## 輸出格式
* 資料夾為文章標題加上推文數，資料夾內為圖片
   
## 使用方法
* 方法一(指定看板抓圖)
```
python beauty_spider2.py [板名] [爬蟲起始的頁面] [爬幾頁] [推文多少以上] 
```
* 方法二(指定網址抓圖)
```
python download_beauty.py [輸入內容.txt]
```
如果要從最新頁面開始爬 第一個參數請填 -1 <br>
爬蟲是利用 PTT 網頁版，所以頁面以網頁版為標準。<br>
請參考： <br>
```
https://www.ptt.cc/bbs/AKB48/index.html
```

## 執行範例 
* 範例一(指定看板抓圖)
``` 
python beauty_spider2.py beauty -1 3 10
```
爬PTT beauty板(表特板) 3頁 文章內容，然後只下載 推文數>=10 的文章內容圖片<br>
### 執行畫面 
![alt tag](http://i.imgur.com/EclywBO.jpg)
### 輸出畫面
![alt tag](http://i.imgur.com/CmcheN3.jpg)
![alt tag](http://i.imgur.com/C1E30JX.jpg)

也可以指定其他看板，如下
``` 
python beauty_spider2.py AKB48 -1 3 10
```
* 範例二(指定網址抓圖)
``` 
python download_beauty.py input.txt
```
爬 input.txt 檔案內的PTT文章連結圖片 , input.txt 檔案<br>
![alt tag](http://i.imgur.com/dtcfWUy.jpg)
### 執行畫面 
![alt tag](http://i.imgur.com/fmu5c8v.jpg)
### 輸出畫面
![alt tag](http://i.imgur.com/gtdPFCE.jpg)
![alt tag](http://i.imgur.com/hw9a8j0.jpg)
![alt tag](http://i.imgur.com/lPKRJnJ.jpg)

## 執行環境
* Python 2.7.3

## License
MIT license

