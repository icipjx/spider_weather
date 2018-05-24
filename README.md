# spider_weather
爬取全国各个城市的历史天气数据，网站[链接](https://www.aqistudy.cn/historydata/), 此网站为动态网站。                  

1.对照自己的chrome浏览器版本，对照[浏览器与驱动对比](https://blog.csdn.net/huilan_same/article/details/51896672)的博客，下载对应版本的chrome驱动；               
2.下载你完成后，分别在程序的44和93行改为自己的chrome驱动路径；                
3.该程序支持多个地区的顺序爬虫，输入格式如：成都、北京、广州....         
4.程序能够提示没有天气数据的输入地区,所以放心大胆输入各种地区；        
5程序支持自动构建以地区拼音（如成都：cheng-du.csv）命名的csv文件。       
