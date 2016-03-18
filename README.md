# PTT 表特版爬蟲圖片下載器
A crawler picture for web PTT Beauty 

## 特色
* 抓取PTT 文章內容圖片(包含推文)

## 輸出格式
* 資料夾為標題加上推文數，資料夾內為圖片
   
## 使用方法
方法一:
```
$ python beauty_spider2.py [爬蟲起始的頁面] [爬幾頁] [推文多少以上] 
```
* [Demo Video](https://www.youtube.com/watch?v=jfvvUeuQPN4) - Windows
* [Demo Video](https://www.youtube.com/watch?v=2nGdhs7TJKw) - Linux

方法二:
```
$ python download_beauty.py [輸入內容]
```
* [Demo Video](https://www.youtube.com/watch?v=whxjScB1W4A) - Windows
* [Demo Video](https://www.youtube.com/watch?v=DdZCf65wKsQ) - Linux

如果要從最新頁面開始爬 第一個參數請填 -1 <br>
爬蟲是利用 PTT 網頁版，所以頁面以網頁版為標準。<br>
請參考： <br>
```
https://www.ptt.cc/bbs/Beauty/index.html
```

## 執行範例 
範例一:
``` 
$ python beauty_spider2.py -1 5 10
```
爬PTT 表特(beauty)版 5頁 文章內容，然後只下載推文數>=10的文章

範例二:
``` 
$ python download_beauty.py input.txt
```
爬 input.txt 檔案內的PTT文章連結圖片

## 執行環境
* Python 2.7.3

## License
MIT license

